# Pokémon Catch Bot

The Pokémon Catch Bot is a Telegram bot that allows users to encounter and catch wild Pokémon in a chat group. The bot provides an interactive and fun experience for Pokémon enthusiasts.

<p align="center">
  <img src="https://graph.org/file/58ca90f1f28d86419205e.jpg" alt="Poké Catch Bot Logo" width="500" height="300">
</p>

[![License](https://img.shields.io/github/license/BotGeniusHub/Pokemon-Catch-Bot)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

## Features

- Encounter a wild Pokémon in the group chat at regular intervals.
- Catch the encountered Pokémon by using the `/catch` command.
- View the list of Pokémon caught by a user using the `/pokedex` command.
- See the leaderboard of the top Pokémon catchers using the `/topcatcher` command.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Pokemon-Catch-Bot.git

## Install the required dependencies:

   ```basb
pip install -r requirements.txt
```

## Set up a MongoDB database and configure the connection in the code.
Obtain the necessary API credentials:

Create a bot on Telegram and obtain the bot token.
Set up a Pyrogram app and obtain the API ID and API hash.
Update the following variables in the code with your API credentials:
   ```bash
api_id: Your Pyrogram app API ID.
api_hash: Your Pyrogram app API hash.
bot_token: Your Telegram bot token.
```
## Customize the bot's behavior and messages as needed.

Start the bot:
   ```bash
python bot.py
```

## Add the Pokémon Catch Bot to your Telegram group.
   ```bash
Start the bot by sending the /start command in the group.
Wait for the bot to announce a wild Pokémon at regular intervals.
Use the /catch command followed by the Pokémon's name to attempt to catch it.
Use the /pokedex command to view the list of Pokémon you have caught.
Use the /topcatcher command to see the leaderboard of the top Pokémon catchers in the group.
```
## Acknowledgements
PokéAPI: Provides Pokémon data for the bot.
Pyrogram: Python library for interacting with the Telegram API.
MongoDB: NoSQL database for storing user data.
Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please submit a pull request.

## License
The Pokémon Catch Bot is licensed under the [![License](https://img.shields.io/github/license/BotGeniusHub/Pokemon-Catch-Bot)](LICENSE)
