import os
import random
import requests
import pyrogram
import pymongo
from pymongo import MongoClient
from pyrogram import Client, filters, idle
from pokebase import pokemon
from uuid import uuid4
from collections import defaultdict
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import pokemon_database  
from PIL import Image, ImageDraw, ImageFont
from pokestore import pokemon_store

# Connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority')
db = client['pokemon_bot']
collection = db['pokedex']
leaderboard_collection = db['leaderboard']


# Global variables to track the group message count and the currently announced Pokémon
message_count = 0
announced_pokemon = None

# Create a Pyrogram client
api_id = 16743442
api_hash = '12bbd720f4097ba7713c5e40a11dfd2a'
bot_token = '6100943782:AAG9DRpPrYJH2Q3OwxEQjcm9MdlPicSZgsI'
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
        caption = f"Welcome to the Pokémon Catching Bot!\nCommands:\n/start - Start the bot and encounter a wild Pokémon\n/catch - Attempt to catch the encountered Pokémon\n/help - Display this help menu\n/pokedex - View your Pokémon\n/guess - Guess the pokemon\n/ball - To get the guessed pokemon\n/bank - To get the amount of money you have\n/store - To buy the pokemon\n\nYou have any issues with bot join our channel and said us what issues you face..Thank you ❤"
                       
        client.send_photo(chat_id=message.chat.id, photo=image_file, caption=caption, reply_to_message_id=message.message_id)


#-----------------------

# Global variables
announced_pokemon = None
user_pokedex = []
user_money = {}
pokemon_store = []


# Function to generate a random amount of money for the user
def generate_money():
    return random.randint(10, 100)  # Generates a random amount between 10 and 100


# Function to load the Pokémon store data
def load_pokemon_store():
    global pokemon_store

    

# Function to get the current page of the Pokémon store
def get_store_page(page_number):
    page_size = 1  # Number of Pokémon per page
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return pokemon_store[start_index:end_index]


@app.on_message(filters.command("guess"))
def guess_command(client, message):
    global announced_pokemon

    if announced_pokemon:
        client.send_message(
            chat_id=message.chat.id,
            text="There is already an ongoing guess. Type /ball to catch it!"
        )
        return

    # Choose a random Pokémon from the database
    pokemon_name = random.choice(pokemon_database)["name"]
    pokemon_info = pokemon(pokemon_name.lower())

    # Get the front sprite image of the Pokémon
    image_url = pokemon_info.sprites.front_default
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("pokemon_image.jpg", "wb") as file:
            file.write(response.content)

    # Draw a question mark over the Pokémon image
    image = Image.open("pokemon_image.jpg")
    image = image.convert("RGB")  # Convert to RGB mode
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=50)
    text_width, text_height = draw.textsize("?", font=font)
    text_position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    draw.text(text_position, "?", fill="white", font=font)
    image.save("guess_image.jpg", "JPEG")  # Save as JPEG

    # Send the modified image to the user
    with open("guess_image.jpg", "rb") as file:
        client.send_photo(chat_id=message.chat.id, photo=file, caption="Guess the Pokémon!")

    # Save the correct answer for later verification
    announced_pokemon = pokemon_name.lower()




# Global variables
announced_pokemon = None
user_pokedex = []
user_bank = {}

# ...

@app.on_message(filters.command("ball"))
def ball_command(client, message):
    global announced_pokemon

    # Check if there is a Pokémon to catch
    if not announced_pokemon:
        client.send_message(
            chat_id=message.chat.id,
            text="No Pokémon to catch. Type /guess to start a new guessing game."
        )
        return

    # Get the Pokémon name provided by the user
    command_parts = message.text.split(" ")
    if len(command_parts) < 2:
        client.send_message(
            chat_id=message.chat.id,
            text="Please provide a Pokémon name."
        )
        return

    pokemon_name = command_parts[1].lower()

    if pokemon_name == announced_pokemon:
        # Pokémon caught successfully
        client.send_message(
            chat_id=message.chat.id,
            text="Congratulations! You caught the Pokémon!"
        )
        user_pokedex.append(pokemon_name)

        # Give a random amount of money to the user
        money_amount = random.randint(10, 50)
        user_id = message.from_user.id
        if user_id in user_bank:
            user_bank[user_id] += money_amount
        else:
            user_bank[user_id] = money_amount

        client.send_message(
            chat_id=message.chat.id,
            text="You received {} money!".format(money_amount)
        )
    else:
        # Incorrect Pokémon name
        client.send_message(
            chat_id=message.chat.id,
            text="Oops! That's not the correct Pokémon."
        )

    # Reset the announced Pokémon
    announced_pokemon = None



current_page = 0
items_per_page = 3

# User bank account data structure:
# {
#     "user_id": {
#         "balance": 500,
#         "pokedex": []
#     },
#     ...
# }
user_accounts = {}

# Handler function for /store command
@app.on_message(filters.command("store"))
def store_command(client, message):
    global current_page

    # Check if there are any Pokémon in the store
    if not pokemon_store:
        client.send_message(
            chat_id=message.chat.id,
            text="The store is currently empty. Please check back later."
        )
        return

    # Calculate the start and end index for the current page
    start_index = current_page * items_per_page
    end_index = start_index + items_per_page

    # Get the Pokémon for the current page
    current_pokemon = pokemon_store[start_index:end_index]

    # Generate inline keyboard buttons for each Pokémon
    buttons = []
    for pokemon in current_pokemon:
        buttons.append(
            [InlineKeyboardButton(pokemon["name"], callback_data=f"buy_{pokemon['name']}")]
        )

    # Add next and previous buttons
    if current_page > 0:
        buttons.append(
            [InlineKeyboardButton("Previous", callback_data="previous")]
        )
    if end_index < len(pokemon_store):
        buttons.append(
            [InlineKeyboardButton("Next", callback_data="next")]
        )

    # Create inline keyboard markup
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send the store message with the current Pokémon and buttons
    client.send_message(
        chat_id=message.chat.id,
        text="Welcome to the Pokémon Store! Here are the available Pokémon:",
        reply_markup=reply_markup
    )


# Handler function for callback queries
@app.on_callback_query()
def callback_query(client, callback_query):
    global current_page

    # Get the callback data
    callback_data = callback_query.data

    # Get the user's bank account data
    user_id = callback_query.from_user.id
    user_account = user_accounts.setdefault(user_id, {"balance": 500, "pokedex": []})

    # Check if it's a buy action
    if callback_data.startswith("buy_"):
        pokemon_name = callback_data.replace("buy_", "")

        # Find the selected Pokémon in the store
        selected_pokemon = None
        for pokemon in pokemon_store:
            if pokemon["name"] == pokemon_name:
                selected_pokemon = pokemon
                break

        if selected_pokemon:
            # Check if the user has enough balance
            if user_account["balance"] >= selected_pokemon["price"]:
                # Deduct the price from the user's balance
                user_account["balance"] -= selected_pokemon["price"]

                # Add the Pokémon to the user's collection
                user_account["pokedex"].append(selected_pokemon["name"])

                # Send the purchase confirmation message
                client.send_message(
                    chat_id=callback_query.message.chat.id,
                    text=f"You have purchased {pokemon_name} for {selected_pokemon['price']} coins!"
                )
            else:
                # Insufficient balance
                client.send_message(
                    chat_id=callback_query.message.chat.id,
                    text="Sorry, you don't have enough coins to purchase this Pokémon."
                )
        else:
            # Invalid Pokémon selection
            client.send_message(
                chat_id=callback_query.message.chat.id,
                text="Invalid Pokémon selection. Please try again."
            )
    elif callback_data == "previous":
        # Move to the previous page
        current_page -= 1
        store_command(client, callback_query.message)
    elif callback_data == "next":
        # Move to the next page
        current_page += 1
        store_command(client, callback_query.message)


# Handler function for /bank command
@app.on_message(filters.command("bank"))
def bank_command(client, message):
    user_id = message.from_user.id
    user_account = user_accounts.setdefault(user_id, {"balance": 500, "pokedex": []})
    balance = user_account["balance"]

    # Send the user's bank account balance
    client.send_message(
        chat_id=message.chat.id,
        text=f"Your current balance is {balance} coins."
    )





#-----------------------

# Handler function for /pokedex command
@app.on_message(filters.command("pokedex"))
def view_pokedex(client, message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
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
                    InlineKeyboardButton("◀️", callback_data=f"prev_pokedex_page {current_page - 1}"),
                    InlineKeyboardButton("▶️", callback_data=f"next_pokedex_page {current_page + 1}")
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
                        InlineKeyboardButton("◀️", callback_data=f"prev_pokedex_page {next_page - 1}"),
                        InlineKeyboardButton("▶️", callback_data=f"next_pokedex_page {next_page + 1}")
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
                message.from_user.first_name,
                message.from_user.id,
                prev_page,
                total_pages,
                pokedex_list,
                total_pokemon
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("◀️", callback_data=f"prev_pokedex_page {prev_page - 1}"),
                        InlineKeyboardButton("▶️", callback_data=f"next_pokedex_page {prev_page + 1}")
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
        client.send_photo(message.chat.id, photo=image_file_name, caption="A wild Pokemon appeared! Type '/catch ```Name``` to catch it.".format(announced_pokemon["name"], announced_pokemon["name"]))

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
