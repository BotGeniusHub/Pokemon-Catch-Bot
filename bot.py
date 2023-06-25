import os
import random
import requests
import pyrogram
from pymongo import MongoClient
from pyrogram import Client, filters, idle
from pokebase import pokemon
from uuid import uuid4
from collections import defaultdict
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

def update_leaderboard(client, chat_id):
    leaderboard = {}

    # Iterate over the entries in the database
    for entry in db:
        user_id = entry["user_id"]
        caught_count = entry["caught_count"]
        leaderboard[user_id] = caught_count

    # Sort the leaderboard based on the caught count in descending order
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    # Prepare the message to be sent
    message = "<b>Leaderboard:</b>\n\n"
    message += "Top 10 Pokemon Catchers:\n"
    count = 1
    for user_id, caught_count in sorted_leaderboard[:10]:
        try:
            # Get the user's information
            user = client.get_chat_member(chat_id, user_id)
            username = user.user.username if user.user.username else user.user.first_name
            message += f"{count}. {username}: {caught_count}\n"
            count += 1
        except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
            continue

    # Send the leaderboard message
    client.send_message(chat_id, message, parse_mode="html")


# Command handler for the /leaderboard command
@app.on_message(filters.command("leaderboard"))
def show_leaderboard(client, message):
    leaderboard = update_leaderboard(client, message.chat.id)
    client.send_message(chat_id=message.chat.id, text=leaderboard, reply_to_message_id=message.message_id)





#-----------------------

# Handler function for /pokedex command
@app.on_message(filters.command("pokedex"))
def view_pokedex(client, message):
    user_id = message.from_user.id
    pokedex_data = collection.find_one({"user_id": user_id})
    if pokedex_data:
        pokedex = pokedex_data['pokedex']
        total_pokemon = len(pokedex)

        if total_pokemon == 0:
            client.send_message(message.chat.id, "Your Pokedex is empty.", reply_to_message_id=message.message_id)
            return

        page_size = 10  # Number of Pokémon to display per page
        current_page = 1
        total_pages = (total_pokemon - 1) // page_size + 1

        if 'pokedex_page' in message.command:
            try:
                current_page = int(message.command[1])
                if current_page < 1 or current_page > total_pages:
                    raise ValueError()
            except (ValueError, IndexError):
                client.send_message(message.chat.id, "Invalid page number.", reply_to_message_id=message.message_id)
                return

        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        current_pokedex = pokedex[start_index:end_index]

        pokedex_list = ""
        for i, pokemon_name in enumerate(current_pokedex, start=start_index + 1):
            pokedex_list += "{}. {}\n".format(i, pokemon_name)

        caption = "** [{}](tg://user?id={}) 's Pokedex (Page {}/{}) **\n{}\n**Total Pokémon Caught:** {}".format(
            message.from_user.first_name,
            message.from_user.id,
            current_page,
            total_pages,
            pokedex_list,
            total_pokemon
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Previous Page", callback_data=f"prev_pokedex_page {current_page - 1}"),
                    InlineKeyboardButton("Next Page", callback_data=f"next_pokedex_page {current_page + 1}")
                ]
            ]
        )

        if current_page == 1:
            keyboard.inline_keyboard[0].pop(0)  # Remove the "Previous Page" button for the first page
        elif current_page == total_pages:
            keyboard.inline_keyboard[0].pop()  # Remove the "Next Page" button for the last page

        client.send_message(
            message.chat.id,
            caption,
            reply_to_message_id=message.message_id,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        client.send_message(message.chat.id, "Your Pokedex is empty.", reply_to_message_id=message.message_id)


# Handler function for callback queries
@app.on_callback_query()
def handle_callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    message = callback_query.message
    callback_data = callback_query.data

    if callback_data.startswith("next_pokedex_page"):
        try:
            _, next_page = callback_data.split()
            next_page = int(next_page)
            if next_page < 1:
                raise ValueError()
        except (ValueError, IndexError):
            client.answer_callback_query(callback_query.id, text="Invalid page number.")
            return

        pokedex_data = collection.find_one({"user_id": user_id})
        if pokedex_data:
            pokedex = pokedex_data['pokedex']
            total_pokemon = len(pokedex)
            page_size = 10
            total_pages = (total_pokemon - 1) // page_size + 1

            if next_page > total_pages:
                client.answer_callback_query(callback_query.id, text="No more pages available.")
                return

            start_index = (next_page - 1) * page_size
            end_index = start_index + page_size
            current_pokedex = pokedex[start_index:end_index]

            pokedex_list = ""
            for i, pokemon_name in enumerate(current_pokedex, start=start_index + 1):
                pokedex_list += "{}. {}\n".format(i, pokemon_name)

            caption = "** [{}](tg://user?id={}) 's Pokedex (Page {}/{}) **\n{}\n**Total Pokémon Caught:** {}".format(
                message.from_user.first_name,
                message.from_user.id,
                next_page,
                total_pages,
                pokedex_list,
                total_pokemon
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Previous Page", callback_data=f"prev_pokedex_page {next_page - 1}"),
                        InlineKeyboardButton("Next Page", callback_data=f"next_pokedex_page {next_page + 1}")
                    ]
                ]
            )

            if next_page == 1:
                keyboard.inline_keyboard[0].pop(0)  # Remove the "Previous Page" button for the first page

            client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=caption,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

            client.answer_callback_query(callback_query.id, text="Page {} of {}".format(next_page, total_pages))
        else:
            client.answer_callback_query(callback_query.id, text="Your Pokedex is empty.")

    elif callback_data.startswith("prev_pokedex_page"):
        try:
            _, prev_page = callback_data.split()
            prev_page = int(prev_page)
            if prev_page < 1:
                raise ValueError()
        except (ValueError, IndexError):
            client.answer_callback_query(callback_query.id, text="Invalid page number.")
            return

        pokedex_data = collection.find_one({"user_id": user_id})
        if pokedex_data:
            pokedex = pokedex_data['pokedex']
            total_pokemon = len(pokedex)
            page_size = 10
            total_pages = (total_pokemon - 1) // page_size + 1

            if prev_page < 1:
                client.answer_callback_query(callback_query.id, text="No more previous pages.")
                return

            start_index = (prev_page - 1) * page_size
            end_index = start_index + page_size
            current_pokedex = pokedex[start_index:end_index]

            pokedex_list = ""
            for i, pokemon_name in enumerate(current_pokedex, start=start_index + 1):
                pokedex_list += "{}. {}\n".format(i, pokemon_name)

            caption = "** [{}](tg://user?id={}) 's Pokedex (Page {}/{}) **\n{}\n*Total Pokémon Caught:* {}".format(
                user.first_name,
                user.id,
                prev_page,
                total_pages,
                pokedex_list,
                total_pokemon
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Previous Page", callback_data=f"prev_pokedex_page {prev_page - 1}"),
                        InlineKeyboardButton("Next Page", callback_data=f"next_pokedex_page {prev_page + 1}")
                    ]
                ]
            )

            if prev_page == total_pages:
                keyboard.inline_keyboard[0].pop()  # Remove the "Next Page" button for the last page

            client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=caption,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

            client.answer_callback_query(callback_query.id, text="Page {} of {}".format(prev_page, total_pages))
        else:
            client.answer_callback_query(callback_query.id, text="Your Pokedex is empty.")



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
        client.send_photo(message.chat.id, photo=image_file_name, caption="A wild Pokemon appeared! Type '/catch ```Pokemon Name``` to catch it.".format(announced_pokemon["name"], announced_pokemon["name"]))

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
