import os
import random
import requests
from pymongo import MongoClient
from pyrogram import Client, filters, idle
from pokebase import pokemon

# Connect to MongoDB
client = MongoClient('mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority')
db = client['pokemon_bot']
collection = db['pokedex']

# Database of available Pokémon
pokemon_database = [
    {"name": "Pikachu", "catch_rate": 0.5},
    {"name": "Charizard", "catch_rate": 0.3},
    {"name": "Squirtle", "catch_rate": 0.7},
    {"name": "Bulbasaur", "catch_rate": 0.6},
    # Add more Pokémon to the database
]

# Global variables to track the group message count and the currently announced Pokémon
message_count = 0
announced_pokemon = None

# Create a Pyrogram client
api_id = 16743442
api_hash = '12bbd720f4097ba7713c5e40a11dfd2a'
bot_token = '6206599982:AAHJlIHxPWqMTpRP4iMvGb0I0pcOf_o-nG8'
app = Client("pokemon_bot", api_id, api_hash, bot_token=bot_token)

# Handler function for /start or /help command
@app.on_message(filters.command(["start", "help"]))
def start_help(client, message):
    client.send_message(message.chat.id, "Bot is running. Use /help to get a list of commands.")

# Handler function for /pokedex command
@app.on_message(filters.command("pokedex"))
def view_pokedex(client, message):
    user_id = message.from_user.id
    pokedex_data = collection.find_one({"user_id": user_id})
    if pokedex_data:
        pokedex_list = '\n'.join(pokedex_data['pokedex']) if pokedex_data['pokedex'] else 'Your Pokedex is empty.'
    else:
        pokedex_list = 'Your Pokedex is empty.'
    client.send_message(message.chat.id, "Your Pokedex:\n{}".format(pokedex_list))

# Handler function for /catch command
@app.on_message(filters.command("catch"))
def catch_pokemon(client, message):
    user_input = message.text
    pokemon_name = user_input.split("/catch ", 1)[-1].lower()
    if announced_pokemon is None:
        client.send_message(chat_id=message.chat.id, text="No Pokémon is currently announced.")
        return
    if pokemon_name.lower() == announced_pokemon["name"].lower():
        catch_probability = random.random()
        if catch_probability <= announced_pokemon["catch_rate"]:
            client.send_message(chat_id=message.chat.id, text="Congratulations! You caught {}!".format(announced_pokemon["name"]))
            add_to_pokedex(message.from_user.id, announced_pokemon["name"])
        else:
            client.send_message(chat_id=message.chat.id, text="Oh no! {} escaped!".format(announced_pokemon["name"]))
    else:
        client.send_message(chat_id=message.chat.id, text="The announced Pokémon is not {}.".format(pokemon_name))


# Handler function for group messages
@app.on_message(filters.group)
def group_message(client, message):
    global message_count, announced_pokemon

    message_count += 1

    if message_count % 10 == 0:
        announced_pokemon = random.choice(pokemon_database)
        pokemon_data = pokemon(announced_pokemon["name"].lower())
        pokemon_image_url = pokemon_data.sprites.front_default

        # Download the Pokémon image
        image_response = requests.get(pokemon_image_url)
        image_file_name = f"{announced_pokemon['name']}.png"
        with open(image_file_name, 'wb') as image_file:
            image_file.write(image_response.content)

        # Send the Pokémon image and announcement message
        client.send_photo(message.chat.id, photo=image_file_name, caption="A wild {} appeared! Type '/catch {}' to catch it.".format(announced_pokemon["name"], announced_pokemon["name"]))

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
