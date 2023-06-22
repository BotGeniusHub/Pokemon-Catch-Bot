from pyrogram import Client, idle

# Create a Pyrogram client instance
api_id = 16743442  # Replace with your API ID
api_hash = "12bbd720f4097ba7713c5e40a11dfd2a"  # Replace with your API Hash
bot_token = "6206599982:AAHJlIHxPWqMTpRP4iMvGb0I0pcOf_o-nG8"  # Replace with your Bot Token
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Your code for setting up the bot and handlers goes here

# Start the bot's event loop
app.run()
idle() 

