import os
import random
import requests
from pymongo import MongoClient
from pyrogram import Client, filters, idle
from pokebase import pokemon
from uuid import uuid4
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import pokemon_database  

# Connect to MongoDB
client = MongoClient('mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority')
db = client['pokemon_bot']
collection = db['pokedex']

# Global variables to track the group message count and the currently announced Pokémon
message_count = 0
announced_pokemon = None

# Create a Pyrogram client
api_id = 16743442
api_hash = '12bbd720f4097ba7713c5e40a11dfd2a'
bot_token = '5827224610:AAGftR84QtQ6rMr7_r2a7zPPjg1SrG755yA'
app = Client("pokemon_bot", api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(_, message):
    # Send an image with a caption
    pokemon_name = random.choice(pokemon_database)["name"]
    pokemon_info = pokemon(pokemon_name.lower())

    image_url = pokemon_info.sprites.front_default
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("pokemon_image.jpg", "wb") as file:
            file.write(response.content)

    caption = f"You just encountered a wild {pokemon_name}!\nUse /help for the help menu!"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Join Channel", url="https://t.me/BotGeniusHub"),
                InlineKeyboardButton("Add me to a Group", url="https://t.me/PokemonCatcherXBot?startgroup=new")
            ]
        ]
    )

    app.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/58ca90f1f28d86419205e.jpg",
        caption=caption,
        reply_to_message_id=message.message_id,
        reply_markup=keyboard,
    )


@app.on_message(filters.command("help"))
def help_command(client, message):
    
    image_path = "IMG_20230622_003312_519.jpg"  
    with open(image_path, "rb") as image_file:
        caption = f"Welcome to the Pokémon Catching Bot!\nCommands:\n/start - Start the bot and encounter a wild Pokémon\n/catch - Attempt to catch the encountered Pokémon\n/help - Display this help menu\n/pokedex - View your Pokémon\n/guess - Guess the pokemon\n/ball - To get the guessed pokemon\n\nYou have any issues with bot join our channel and said us what issues you face..Thank you ❤"
                       
        client.send_photo(chat_id=message.chat.id, photo=image_file, caption=caption, reply_to_message_id=message.message_id)


#-----------------------

#-----------------------

# Handler function for /pokedex command
@app.on_message(filters.command("pokedex"))
def view_pokedex(client, message):
    user_id = message.from_user.id
    pokedex_data = collection.find_one({"user_id": user_id})
    if pokedex_data:
        pokedex_list = ""
        for i, pokemon_name in enumerate(pokedex_data['pokedex'], start=1):
            pokedex_list += "{}. {}\n".format(i, pokemon_name)
        pokemon_count = len(pokedex_data['pokedex'])
        client.send_message(message.chat.id, "** [{}](tg://user?id={}) 's Pokedex:**\n{}\n**Total Pokémon Caught:** {}".format(message.from_user.first_name, message.from_user.id, pokedex_list, pokemon_count),parse_mode="Markdown", reply_to_message_id=message.message_id)
    else:
        client.send_message(message.chat.id, "Your Pokedex is empty.", reply_to_message_id=message.message_id)

# Function to get the user's name using Pyrogram's get_chat_member method
def get_user_name(user_id):
    chat_member = app.get_chat_member(chat_id="your_chat_id", user_id=user_id)  # Replace "your_chat_id" with your chat ID
    return chat_member.user.first_name if chat_member.user else "Unknown"


# Global variables to track the announced Pokémon and caught Pokémon
announced_pokemon = None
caught_pokemon = {}

# Handler function for /catch command
@app.on_message(filters.command("catch"))
def catch_pokemon(client, message):
    global announced_pokemon  # Declare announced_pokemon as a global variable
    user_id = message.from_user.id
    user_input = message.text
    pokemon_name = user_input.split("/catch ", 1)[-1].lower()

    # Check if a Pokémon is currently announced
    if announced_pokemon is None:
        client.send_message(chat_id=message.chat.id, text="No Pokémon is currently announced.", reply_to_message_id=message.message_id)
        return

    # Check if the caught Pokémon matches the announced Pokémon
    if pokemon_name.lower() == announced_pokemon["name"].lower():

        # Check if the Pokémon has already been caught
        if announced_pokemon["name"] in caught_pokemon:
            client.send_message(chat_id=message.chat.id, text="{} has already been caught.".format(announced_pokemon["name"], reply_to_message_id=message.message_id))
            return

        catch_probability = random.random()

        if catch_probability <= announced_pokemon["catch_rate"]:
            client.send_message(chat_id=message.chat.id, text="Congratulations [{}](tg://user?id={})! You caught {}!".format(message.from_user.first_name, message.from_user.id, announced_pokemon["name"], parse_mode="Markdown", reply_to_message_id=message.message_id))
            add_to_pokedex(user_id, announced_pokemon["name"])

            # Add the caught Pokémon and the user who caught it to the dictionary
            caught_pokemon[announced_pokemon["name"]] = user_id

            # Set announced_pokemon to None to allow the announcement of a new Pokémon
            announced_pokemon = None
        else:
            client.send_message(chat_id=message.chat.id, text="Oh no! {} escaped!".format(announced_pokemon["name"], reply_to_message_id=message.message_id))
    else:
        client.send_message(chat_id=message.chat.id, text="The announced Pokémon is not {}.".format(pokemon_name), reply_to_message_id=message.message_id)


# Handler function for group messages
@app.on_message(filters.group)
def group_message(client, message):
    global message_count, announced_pokemon

    message_count += 1

    if message_count % 100 == 0:
        announced_pokemon = random.choice(pokemon_database)
        pokemon_data = pokemon(announced_pokemon["name"].lower())
        pokemon_image_url = pokemon_data.sprites.front_default

        # Download the Pokémon image
        image_response = requests.get(pokemon_image_url)
        image_file_name = f"{announced_pokemon['name']}.png"
        with open(image_file_name, 'wb') as image_file:
            image_file.write(image_response.content)

        # Send the Pokémon image and announcement message
        client.send_photo(message.chat.id, photo=image_file_name, caption="A wild Pokemon appeared! Type '/catch '''Pokemon Name'''' to catch it.".format(announced_pokemon["name"], announced_pokemon["name"]))

        # Remove the downloaded image file
        image_file.close()
        os.remove(image_file_name)

# Function to add a caught Pokémon to the user's Pokedex
def add_to_pokedex(user_id, pokemon_name):
    pokedex_data = collection.find_one({"user_id": user_id})
    if pokedex_data:
        pokedex = pokedex_data['pokedex']
        if pokemon_name not in pokedex:
            pokedex.append(pokemon_name)
        collection.update_one({"user_id": user_id}, {"$set": {"pokedex": pokedex}})
    else:
        collection.insert_one({"user_id": user_id, "pokedex": [pokemon_name]})

            
# Start the bot
app.run()
idle()
