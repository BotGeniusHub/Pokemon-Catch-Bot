from pyrogram import Client, filter

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

    caption = f"You encountered a wild {pokemon_name}!\n\nUse /help for help menu!"

    app.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/58ca90f1f28d86419205e.jpg",
        caption=caption,
        reply_to_message_id=message.message_id,
    )

@app.on_message(filters.command("help"))
def help_command(client, message):
    
    image_path = "IMG_20230622_003312_519.jpg"  
    with open(image_path, "rb") as image_file:
        caption = f"Welcome to the Pokémon Catching Bot!\n\nCommands👇🏻\n/start - Start the bot and encounter a wild Pokémon\n/catch - Attempt to catch the encountered Pokémon\n/help - Display this help menu\n/pokedex - View your Pokémon"
                       
        client.send_photo(chat_id=message.chat.id, photo=image_file, caption=caption, reply_to_message_id=message.message_id)

