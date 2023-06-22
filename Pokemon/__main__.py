from pyrogram import Client, idle

# Create a Pyrogram client instance
api_id = 123456  # Replace with your API ID
api_hash = "your_api_hash"  # Replace with your API Hash
bot_token = "your_bot_token"  # Replace with your Bot Token
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Your code for setting up the bot and handlers goes here

# Start the bot's event loop
app.run()
idle() 

