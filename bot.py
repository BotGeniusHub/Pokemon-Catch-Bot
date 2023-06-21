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

# Database of available Pokémon, you can add more Pokemon with this format
pokemon_database = [
    {"name": "Pikachu", "catch_rate": 0.5},
    {"name": "Charizard", "catch_rate": 0.3},
    {"name": "Squirtle", "catch_rate": 0.7},
    {"name": "Bulbasaur", "catch_rate": 0.6},
    {"name": "Jigglypuff", "catch_rate": 0.4},
    {"name": "Mewtwo", "catch_rate": 0.2},
    {"name": "Mew", "catch_rate": 0.2},
    {"name": "Gengar", "catch_rate": 0.3},
    {"name": "Dragonite", "catch_rate": 0.4},
    {"name": "Gyarados", "catch_rate": 0.4},
    {"name": "Arcanine", "catch_rate": 0.5},
    {"name": "Alakazam", "catch_rate": 0.3},
    {"name": "Articuno", "catch_rate": 0.2},
    {"name": "Zapdos", "catch_rate": 0.2},
    {"name": "Moltres", "catch_rate": 0.2},
    {"name": "Lapras", "catch_rate": 0.4},
    {"name": "Snorlax", "catch_rate": 0.4},
    {"name": "Golem", "catch_rate": 0.5},
    {"name": "Venusaur", "catch_rate": 0.6},
    {"name": "Blastoise", "catch_rate": 0.6},
    {"name": "Nidoking", "catch_rate": 0.5},
    {"name": "Nidoqueen", "catch_rate": 0.5},
    {"name": "Machamp", "catch_rate": 0.4},
    {"name": "Rhydon", "catch_rate": 0.4},
    {"name": "Aerodactyl", "catch_rate": 0.3},
    {"name": "Charmander", "catch_rate": 0.6},
    {"name": "Charmeleon", "catch_rate": 0.5},
    {"name": "Caterpie", "catch_rate": 0.8},
    {"name": "Metapod", "catch_rate": 0.7},
    {"name": "Butterfree", "catch_rate": 0.6},
    {"name": "Weedle", "catch_rate": 0.8},
    {"name": "Kakuna", "catch_rate": 0.7},
    {"name": "Beedrill", "catch_rate": 0.6},
    {"name": "Pidgey", "catch_rate": 0.8},
    {"name": "Pidgeotto", "catch_rate": 0.7},
    {"name": "Pidgeot", "catch_rate": 0.6},
    {"name": "Rattata", "catch_rate": 0.8},
    {"name": "Raticate", "catch_rate": 0.7},
    {"name": "Spearow", "catch_rate": 0.8},
    {"name": "Fearow", "catch_rate": 0.7},
    {"name": "Ekans", "catch_rate": 0.6},
    {"name": "Arbok", "catch_rate": 0.5},
    {"name": "Raichu", "catch_rate": 0.4},
    {"name": "Sandshrew", "catch_rate": 0.6},
    {"name": "Sandslash", "catch_rate": 0.5},
    {"name": "Nidoran♀", "catch_rate": 0.6},
    {"name": "Nidorina", "catch_rate": 0.5},
    {"name": "Nidoqueen", "catch_rate": 0.4},
    {"name": "Nidoran♂", "catch_rate": 0.6},
    {"name": "Nidorino", "catch_rate": 0.5},
    {"name": "Nidoking", "catch_rate": 0.4},
    {"name": "Clefairy", "catch_rate": 0.5},
    {"name": "Clefable", "catch_rate": 0.4},
    {"name": "Vulpix", "catch_rate": 0.6},
    {"name": "Ninetales", "catch_rate": 0.5},
    {"name": "Wigglytuff", "catch_rate": 0.3},
    {"name": "Zubat", "catch_rate": 0.7},
    {"name": "Golbat", "catch_rate": 0.6},
    {"name": "Oddish", "catch_rate": 0.6},
    {"name": "Gloom", "catch_rate": 0.5},
    {"name": "Vileplume", "catch_rate": 0.4},
    {"name": "Paras", "catch_rate": 0.6},
    {"name": "Parasect", "catch_rate": 0.5},
    {"name": "Venonat", "catch_rate": 0.6},
    {"name": "Venomoth", "catch_rate": 0.5},
    {"name": "Diglett", "catch_rate": 0.6},
    {"name": "Dugtrio", "catch_rate": 0.5},
    {"name": "Meowth", "catch_rate": 0.6},
    {"name": "Persian", "catch_rate": 0.5},
    {"name": "Psyduck", "catch_rate": 0.6},
    {"name": "Golduck", "catch_rate": 0.5},
    {"name": "Mankey", "catch_rate": 0.6},
    {"name": "Primeape", "catch_rate": 0.5},
    {"name": "Growlithe", "catch_rate": 0.6},
    {"name": "Poliwag", "catch_rate": 0.6},
    {"name": "Poliwhirl", "catch_rate": 0.5},
    {"name": "Poliwrath", "catch_rate": 0.4},
    {"name": "Abra", "catch_rate": 0.6},
    {"name": "Kadabra", "catch_rate": 0.5},
    {"name": "Alakazam", "catch_rate": 0.4},
    {"name": "Machop", "catch_rate": 0.6},
    {"name": "Machoke", "catch_rate": 0.5},
    {"name": "Machamp", "catch_rate": 0.4},
    {"name": "Bellsprout", "catch_rate": 0.6},
    {"name": "Weepinbell", "catch_rate": 0.5},
    {"name": "Victreebel", "catch_rate": 0.4},
    {"name": "Tentacool", "catch_rate": 0.6},
    {"name": "Tentacruel", "catch_rate": 0.5},
    {"name": "Geodude", "catch_rate": 0.6},
    {"name": "Graveler", "catch_rate": 0.5},
    {"name": "Golem", "catch_rate": 0.4},
    {"name": "Ponyta", "catch_rate": 0.6},
    {"name": "Rapidash", "catch_rate": 0.5},
    {"name": "Slowpoke", "catch_rate": 0.6},
    {"name": "Slowbro", "catch_rate": 0.5},
    {"name": "Magnemite", "catch_rate": 0.6},
    {"name": "Magneton", "catch_rate": 0.5},
    {"name": "Farfetch'd", "catch_rate": 0.5},
    {"name": "Doduo", "catch_rate": 0.6},
    {"name": "Dodrio", "catch_rate": 0.5},
    {"name": "Seel", "catch_rate": 0.6},
    {"name": "Dewgong", "catch_rate": 0.5},
    {"name": "Grimer", "catch_rate": 0.6},
    {"name": "Muk", "catch_rate": 0.5},
    {"name": "Shellder", "catch_rate": 0.6},
    {"name": "Cloyster", "catch_rate": 0.5},
    {"name": "Gastly", "catch_rate": 0.6},
    {"name": "Haunter", "catch_rate": 0.5},
    {"name": "Gengar", "catch_rate": 0.4},
    {"name": "Onix", "catch_rate": 0.5},
    {"name": "Drowzee", "catch_rate": 0.6},
    {"name": "Hypno", "catch_rate": 0.5},
    {"name": "Krabby", "catch_rate": 0.6},
    {"name": "Kingler", "catch_rate": 0.5},
    {"name": "Voltorb", "catch_rate": 0.6},
    {"name": "Electrode", "catch_rate": 0.5},
    {"name": "Exeggcute", "catch_rate": 0.6},
    {"name": "Exeggutor", "catch_rate": 0.5},
    {"name": "Cubone", "catch_rate": 0.6},
    {"name": "Marowak", "catch_rate": 0.5},
    {"name": "Hitmonlee", "catch_rate": 0.4},
    {"name": "Hitmonchan", "catch_rate": 0.4},
    {"name": "Lickitung", "catch_rate": 0.4},
    {"name": "Koffing", "catch_rate": 0.6},
    {"name": "Weezing", "catch_rate": 0.5},
    {"name": "Rhyhorn", "catch_rate": 0.6},
    {"name": "Rhydon", "catch_rate": 0.4}, 
    {"name": "Entei", "catch_rate": 0.3},
    {"name": "Suicune", "catch_rate": 0.3},

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
        pokedex_list = ""
        for i, pokemon_name in enumerate(pokedex_data['pokedex'], start=1):
            pokedex_list += "{}. {}\n".format(i, pokemon_name)
        pokemon_count = len(pokedex_data['pokedex'])
        client.send_message(message.chat.id, "**Your Pokedex:**\n{}\n**Total Pokémon Caught:** {}".format(pokedex_list, pokemon_count))
    else:
        client.send_message(message.chat.id, "Your Pokedex is empty.")


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

# Handler function for /leaderboard command
@app.on_message(filters.command("leaderboard"))
def show_leaderboard(client, message):
    leaderboard = get_leaderboard()
    leaderboard_text = "**Leaderboard:**\n\n"
    rank = 1
    for user_data in leaderboard:
        user_id = user_data["user_id"]
        username = client.get_chat(user_id).username if client.get_chat(user_id).username else client.get_chat(user_id).first_name
        pokemon_count = user_data["pokedex_count"]
        leaderboard_text = "{}. {} - {} Pokémon\n".format(rank, username, pokemon_count)
        rank += 1
    client.send_message(chat_id=message.chat.id, text=leaderboard_text)

# Command handler for /pokemon command
@app.on_message(filters.command("pokemon"))
def pokemon_command(client, message):
    # Extract the Pokemon name from the command
    command_parts = message.command
    if len(command_parts) < 2:
        message.reply_text("Please provide a Pokemon name.")
        return
    pokemon_name = command_parts[1].lower()

    # Query the database for the Pokemon information
    result = collection.find_one({"name": pokemon_name})
    if result:
        message.reply_text(f"Name: {result['name']}\nType: {result['type']}\nHeight: {result['height']}\nWeight: {result['weight']}")
    else:
        # If the Pokemon is not found in the database, query the PokeAPI
        try:
            response = pokemon(pokemon_name)
            height = response.height / 10  # Convert height from decimeters to meters
            weight = response.weight / 10  # Convert weight from hectograms to kilograms
            types = [t.type.name for t in response.types]
            message.reply_text(f"Name: {response.name}\nType: {', '.join(types)}\nHeight: {height} m\nWeight: {weight} kg")
            # Save the Pokemon information to the database
            collection.insert_one({
                "name": response.name,
                "type": types,
                "height": height,
                "weight": weight
            })
        except requests.exceptions.HTTPError:
            message.reply_text("Pokemon not found.")
            
# Start the bot
app.run()
idle()
