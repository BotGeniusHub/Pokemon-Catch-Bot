import random

import requests

from pymongo import MongoClient

from telegram import ReplyKeyboardMarkup, KeyboardButton

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pokebase import pokemon

# Initialize the bot

updater = Updater('6206599982:AAHJlIHxPWqMTpRP4iMvGb0I0pcOf_o-nG8', use_context=True)

dispatcher = updater.dispatcher

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

# Handler function for /start or /help command

def start_help(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is running. Use /help to get a list of commands.")

# Handler function for /pokedex command

def view_pokedex(update, context):

    user_id = update.message.from_user.id

    pokedex_data = collection.find_one({"user_id": user_id})

    if pokedex_data:

        pokedex_list = '\n'.join(pokedex_data['pokedex']) if pokedex_data['pokedex'] else 'Your Pokedex is empty.'

    else:

        pokedex_list = 'Your Pokedex is empty.'

    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Pokedex:\n{}".format(pokedex_list))

# Handler function for /catch command

def catch_pokemon(update, context):

    user_input = update.message.text

    pokemon_name = user_input.split("/catch ")[-1].lower()

    if announced_pokemon is None:

        context.bot.send_message(chat_id=update.effective_chat.id, text="No Pokémon is currently announced.")

        return

    if pokemon_name == announced_pokemon["name"].lower():

        catch_probability = random.random()

        if catch_probability <= announced_pokemon["catch_rate"]:

            context.bot.send_message(chat_id=update.effective_chat.id, text="Congratulations! You caught {}!".format(announced_pokemon["name"]))

            add_to_pokedex(update.message.from_user.id, announced_pokemon["name"])

        else:

            context.bot.send_message(chat_id=update.effective_chat.id, text="Oh no! {} escaped!".format(announced_pokemon["name"]))

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text="The announced Pokémon is not {}.".format(pokemon_name))

# Handler function for /ptrade command

def trade_pokemon(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is coming soon!")

# Handler function for /pgift command

def gift_pokemon(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is coming soon!")

# Handler function for /pfav command

def make_favorite(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is coming soon!")

# Handler function for /leaderboard command

def view_leaderboard(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is coming soon!")

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

# Handler function for group messages

def group_message(update, context):

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

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_file_name, 'rb'))

        context.bot.send_message(chat_id=update.effective_chat.id, text="A wild {} appeared! Type '/catch {}' to catch it.".format(announced_pokemon["name"], announced_pokemon["name"]))

        # Remove the downloaded image file

        image_file.close()

        os.remove(image_file_name)

# Register command and message handlers

start_help_handler = CommandHandler(['start', 'help'], start_help)

dispatcher.add_handler(start_help_handler)

pokedex_handler = CommandHandler('pokedex', view_pokedex)

dispatcher.add_handler(pokedex_handler)

catch_handler = CommandHandler('catch', catch_pokemon)

dispatcher.add_handler(catch_handler)

ptrade_handler = CommandHandler('ptrade', trade_pokemon)

dispatcher.add_handler(ptrade_handler)

pgift_handler = CommandHandler('pgift', gift_pokemon)

dispatcher.add_handler(pgift_handler)

pfav_handler = CommandHandler('pfav', make_favorite)

dispatcher.add_handler(pfav_handler)

leaderboard_handler = CommandHandler('leaderboard', view_leaderboard)

dispatcher.add_handler(leaderboard_handler)

message_handler = MessageHandler(Filters.group, group_message)

dispatcher.add_handler(message_handler)

# Start the bot

updater.start_polling()
