import os
import random
import requests
from pymongo import MongoClient
from pyrogram import Client, filters, idle
from pokebase import pokemon
from uuid import uuid4

# Connect to MongoDB
client = MongoClient('mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority')
db = client['pokemon_bot']
collection = db['pokedex']

# Database of available Pokémon, you can add more Pokemon with this format
pokemon_database = [
    {"name": "Bulbasaur", "catch_rate": 45},
    {"name": "Ivysaur", "catch_rate": 45},
    {"name": "Venusaur", "catch_rate": 45},
    {"name": "Charmander", "catch_rate": 45},
    {"name": "Charmeleon", "catch_rate": 45},
    {"name": "Charizard", "catch_rate": 45},
    {"name": "Squirtle", "catch_rate": 45},
    {"name": "Wartortle", "catch_rate": 45},
    {"name": "Blastoise", "catch_rate": 45},
    {"name": "Caterpie", "catch_rate": 255},
    {"name": "Metapod", "catch_rate": 120},
    {"name": "Butterfree", "catch_rate": 45}, 
    {"name": "Weedle", "catch_rate": 255},
    {"name": "Kakuna", "catch_rate": 120},
    {"name": "Beedrill", "catch_rate": 45},
    {"name": "Pidgey", "catch_rate": 255},
    {"name": "Pidgeotto", "catch_rate": 120},
    {"name": "Pidgeot", "catch_rate": 45},
    {"name": "Rattata", "catch_rate": 255},
    {"name": "Raticate", "catch_rate": 127},
    {"name": "Spearow", "catch_rate": 255},
    {"name": "Fearow", "catch_rate": 90},
    {"name": "Ekans", "catch_rate": 255},
    {"name": "Arbok", "catch_rate": 90},
    {"name": "Pikachu", "catch_rate": 190},
    {"name": "Raichu", "catch_rate": 75},
    {"name": "Sandshrew", "catch_rate": 255},
    {"name": "Sandslash", "catch_rate": 90},
    {"name": "Nidoran♀", "catch_rate": 235},
    {"name": "Nidorina", "catch_rate": 120},
    {"name": "Nidoqueen", "catch_rate": 45},
    {"name": "Nidoran♂", "catch_rate": 235},
    {"name": "Nidorino", "catch_rate": 120},
    {"name": "Nidoking", "catch_rate": 45},
    {"name": "Clefairy", "catch_rate": 150},
    {"name": "Clefable", "catch_rate": 25},
    {"name": "Vulpix", "catch_rate": 190},
    {"name": "Ninetales", "catch_rate": 75},
    {"name": "Jigglypuff", "catch_rate": 170},
    {"name": "Wigglytuff", "catch_rate": 50},
    {"name": "Zubat", "catch_rate": 255},
    {"name": "Golbat", "catch_rate": 90},
    {"name": "Oddish", "catch_rate": 255},
    {"name": "Gloom", "catch_rate": 120},
    {"name": "Vileplume", "catch_rate": 45},
    {"name": "Paras", "catch_rate": 190},
    {"name": "Parasect", "catch_rate": 75},
    {"name": "Venonat", "catch_rate": 190},
    {"name": "Venomoth", "catch_rate": 75},
    {"name": "Diglett", "catch_rate": 255},
    {"name": "Dugtrio", "catch_rate": 50},
    {"name": "Meowth", "catch_rate": 255},
    {"name": "Persian", "catch_rate": 90},
    {"name": "Psyduck", "catch_rate": 190},
    {"name": "Golduck", "catch_rate": 75},
    {"name": "Mankey", "catch_rate": 190},
    {"name": "Primeape", "catch_rate": 75},
    {"name": "Growlithe", "catch_rate": 190},
    {"name": "Arcanine", "catch_rate": 75},
    {"name": "Poliwag", "catch_rate": 255},
    {"name": "Poliwhirl", "catch_rate": 120},
    {"name": "Poliwrath", "catch_rate": 45},
    {"name": "Abra", "catch_rate": 200},
    {"name": "Kadabra", "catch_rate": 100},
    {"name": "Alakazam", "catch_rate": 50},
    {"name": "Machop", "catch_rate": 180},
    {"name": "Machoke", "catch_rate": 90},
    {"name": "Machamp", "catch_rate": 45},
    {"name": "Bellsprout", "catch_rate": 255},
    {"name": "Weepinbell", "catch_rate": 120},
    {"name": "Victreebel", "catch_rate": 45},
    {"name": "Tentacool", "catch_rate": 190},
    {"name": "Tentacruel", "catch_rate": 60},
    {"name": "Geodude", "catch_rate": 255},
    {"name": "Graveler", "catch_rate": 120},
    {"name": "Golem", "catch_rate": 45},
    {"name": "Ponyta", "catch_rate": 190},
    {"name": "Rapidash", "catch_rate": 60},
    {"name": "Slowpoke", "catch_rate": 190},
    {"name": "Slowbro", "catch_rate": 75},
    {"name": "Magnemite", "catch_rate": 190},
    {"name": "Magneton", "catch_rate": 75},
    {"name": "Farfetch'd", "catch_rate": 45},
    {"name": "Doduo", "catch_rate": 190},
    {"name": "Dodrio", "catch_rate": 45},
    {"name": "Seel", "catch_rate": 190},
    {"name": "Dewgong", "catch_rate": 75},
    {"name": "Grimer", "catch_rate": 190},
    {"name": "Muk", "catch_rate": 75},
    {"name": "Shellder", "catch_rate": 190},
    {"name": "Cloyster", "catch_rate": 60},
    {"name": "Gastly", "catch_rate": 190},
    {"name": "Haunter", "catch_rate": 90},
    {"name": "Gengar", "catch_rate": 45},
    {"name": "Onix", "catch_rate": 45},
    {"name": "Drowzee", "catch_rate": 190},
    {"name": "Hypno", "catch_rate": 75},
    {"name": "Krabby", "catch_rate": 225},
    {"name": "Kingler", "catch_rate": 60},
    {"name": "Voltorb", "catch_rate": 190},
    {"name": "Electrode", "catch_rate": 60},
    {"name": "Exeggcute", "catch_rate": 90},
    {"name": "Exeggutor", "catch_rate": 45},
    {"name": "Cubone", "catch_rate": 190},
    {"name": "Marowak", "catch_rate": 75},
    {"name": "Hitmonlee", "catch_rate": 45},
    {"name": "Hitmonchan", "catch_rate": 45},
    {"name": "Lickitung", "catch_rate": 45},
    {"name": "Koffing", "catch_rate": 190},
    {"name": "Weezing", "catch_rate": 60},
    {"name": "Rhyhorn", "catch_rate": 120},
    {"name": "Rhydon", "catch_rate": 60},
    {"name": "Chansey", "catch_rate": 30},
    {"name": "Tangela", "catch_rate": 45},
    {"name": "Kangaskhan", "catch_rate": 45},
    {"name": "Horsea", "catch_rate": 225},
    {"name": "Seadra", "catch_rate": 75},
    {"name": "Goldeen", "catch_rate": 225},
    {"name": "Seaking", "catch_rate": 60},
    {"name": "Staryu", "catch_rate": 225},
    {"name": "Starmie", "catch_rate": 60},
    {"name": "Mr. Mime", "catch_rate": 45},
    {"name": "Scyther", "catch_rate": 45},
    {"name": "Jynx", "catch_rate": 45},
    {"name": "Electabuzz", "catch_rate": 45},
    {"name": "Magmar", "catch_rate": 45},
    {"name": "Pinsir", "catch_rate": 45},
    {"name": "Tauros", "catch_rate": 45},
    {"name": "Magikarp", "catch_rate": 255},
    {"name": "Gyarados", "catch_rate": 45},
    {"name": "Lapras", "catch_rate": 45},
    {"name": "Ditto", "catch_rate": 35},
    {"name": "Eevee", "catch_rate": 45},
    {"name": "Vaporeon", "catch_rate": 45},
    {"name": "Jolteon", "catch_rate": 45},
    {"name": "Flareon", "catch_rate": 45},
    {"name": "Porygon", "catch_rate": 45},
    {"name": "Omanyte", "catch_rate": 45},
    {"name": "Omastar", "catch_rate": 45},
    {"name": "Kabuto", "catch_rate": 45},
    {"name": "Kabutops", "catch_rate": 45},
    {"name": "Aerodactyl", "catch_rate": 45},
    {"name": "Snorlax", "catch_rate": 25},
    {"name": "Articuno", "catch_rate": 3},
    {"name": "Zapdos", "catch_rate": 3},
    {"name": "Moltres", "catch_rate": 3},
    {"name": "Dratini", "catch_rate": 45},
    {"name": "Dragonair", "catch_rate": 45},
    {"name": "Dragonite", "catch_rate": 45},
    {"name": "Mewtwo", "catch_rate": 3},
    {"name": "Mew", "catch_rate": 45},
    {"name": "Chikorita", "catch_rate": 45},
    {"name": "Bayleef", "catch_rate": 45},
    {"name": "Meganium", "catch_rate": 45},
    {"name": "Cyndaquil", "catch_rate": 45},
    {"name": "Quilava", "catch_rate": 45},
    {"name": "Typhlosion", "catch_rate": 45},
    {"name": "Totodile", "catch_rate": 45},
    {"name": "Croconaw", "catch_rate": 45},
    {"name": "Feraligatr", "catch_rate": 45},
    {"name": "Sentret", "catch_rate": 255},
    {"name": "Furret", "catch_rate": 90},
    {"name": "Hoothoot", "catch_rate": 255},
    {"name": "Noctowl", "catch_rate": 90},
    {"name": "Ledyba", "catch_rate": 255},
    {"name": "Ledian", "catch_rate": 90},
    {"name": "Spinarak", "catch_rate": 255},
    {"name": "Ariados", "catch_rate": 90},
    {"name": "Crobat", "catch_rate": 90},
    {"name": "Chinchou", "catch_rate": 190},
    {"name": "Lanturn", "catch_rate": 75},
    {"name": "Pichu", "catch_rate": 190},
    {"name": "Cleffa", "catch_rate": 150},
    {"name": "Igglybuff", "catch_rate": 170},
    {"name": "Togepi", "catch_rate": 190},
    {"name": "Togetic", "catch_rate": 75},
    {"name": "Natu", "catch_rate": 190},
    {"name": "Xatu", "catch_rate": 75},
    {"name": "Mareep", "catch_rate": 235},
    {"name": "Flaaffy", "catch_rate": 120},
    {"name": "Ampharos", "catch_rate": 45},
    {"name": "Bellossom", "catch_rate": 45},
    {"name": "Marill", "catch_rate": 190},
    {"name": "Azumarill", "catch_rate": 75},
    {"name": "Sudowoodo", "catch_rate": 65},
    {"name": "Politoed", "catch_rate": 45},
    {"name": "Hoppip", "catch_rate": 255},
    {"name": "Skiploom", "catch_rate": 120},
    {"name": "Jumpluff", "catch_rate": 45},
    {"name": "Aipom", "catch_rate": 45},
    {"name": "Sunkern", "catch_rate": 235},
    {"name": "Sunflora", "catch_rate": 120},
    {"name": "Yanma", "catch_rate": 75},
    {"name": "Wooper", "catch_rate": 255},
    {"name": "Quagsire", "catch_rate": 90},
    {"name": "Espeon", "catch_rate": 45},
    {"name": "Umbreon", "catch_rate": 45},
    {"name": "Murkrow", "catch_rate": 30},
    {"name": "Slowking", "catch_rate": 70},
    {"name": "Misdreavous", "catch_rate": 45},
    {"name": "Unown", "catch_rate": 225},
    {"name": "Wobbuffet", "catch_rate": 45},
    {"name": "Girafarig", "catch_rate": 60},
    {"name": "Pineco", "catch_rate": 190},
    {"name": "Forretress", "catch_rate": 75},
    {"name": "Dunsparce", "catch_rate": 190},
    {"name": "Gligar", "catch_rate": 60},
    {"name": "Steelix", "catch_rate": 25},
    {"name": "Snubbull", "catch_rate": 190},
    {"name": "Granbull", "catch_rate": 75},
    {"name": "Qwilfish", "catch_rate": 45},
    {"name": "Scizor", "catch_rate": 25},
    {"name": "Shuckle", "catch_rate": 190},
    {"name": "Heracross", "catch_rate": 45},
    {"name": "Sneasel", "catch_rate": 60},
    {"name": "Teddiursa", "catch_rate": 120},
    {"name": "Ursaring", "catch_rate": 60},
    {"name": "Slugma", "catch_rate": 190},
    {"name": "Magcargo", "catch_rate": 75},
    {"name": "Swinub", "catch_rate": 225},
    {"name": "Piloswine", "catch_rate": 75},
    {"name": "Corsola", "catch_rate": 60},
    {"name": "Remoraid", "catch_rate": 190},
    {"name": "Octillery", "catch_rate": 75},
    {"name": "Delibird", "catch_rate": 45},
    {"name": "Mantine", "catch_rate": 25},
    {"name": "Skarmory", "catch_rate": 25},
    {"name": "Houndour", "catch_rate": 120},
    {"name": "Houndoom", "catch_rate": 45},
    {"name": "Kingdra", "catch_rate": 45},
    {"name": "Phanpy", "catch_rate": 120},
    {"name": "Donphan", "catch_rate": 60},
    {"name": "Porygon2", "catch_rate": 30},
    {"name": "Stantler", "catch_rate": 45},
    {"name": "Smeargle", "catch_rate": 45},
    {"name": "Tyrogue", "catch_rate": 75},
    {"name": "Hitmontop", "catch_rate": 45},
    {"name": "Smoochum", "catch_rate": 45},
    {"name": "Elekid", "catch_rate": 45},
    {"name": "Magby", "catch_rate": 45},
    {"name": "Miltank", "catch_rate": 45},
    {"name": "Blissey", "catch_rate": 30},
    {"name": "Raikou", "catch_rate": 3},
    {"name": "Entei", "catch_rate": 3},
    {"name": "Suicune", "catch_rate": 3},
    {"name": "Larvitar", "catch_rate": 45},
    {"name": "Pupitar", "catch_rate": 45},
    {"name": "Tyranitar", "catch_rate": 45},
    {"name": "Lugia", "catch_rate": 3},
    {"name": "Ho-Oh", "catch_rate": 3},
    {"name": "Celebi", "catch_rate": 45},
    {"name": "Treecko", "catch_rate": 45},
    {"name": "Grovyle", "catch_rate": 45},
    {"name": "Sceptile", "catch_rate": 45},
    {"name": "Torchic", "catch_rate": 45},
    {"name": "Combusken", "catch_rate": 45},
    {"name": "Blaziken", "catch_rate": 45},
    {"name": "Mudkip", "catch_rate": 45},
    {"name": "Marshtomp", "catch_rate": 45},
    {"name": "Swampert", "catch_rate": 45},
    {"name": "Poochyena", "catch_rate": 255},
    {"name": "Mightyena", "catch_rate": 127},
    {"name": "Zigzagoon", "catch_rate": 255},
    {"name": "Linoone", "catch_rate": 90},
    {"name": "Wurmple", "catch_rate": 255},
    {"name": "Silcoon", "catch_rate": 120},
    {"name": "Beautifly", "catch_rate": 45},
    {"name": "Cascoon", "catch_rate": 120},
    {"name": "Dustox", "catch_rate": 45},
    {"name": "Lotad", "catch_rate": 255},
    {"name": "Lombre", "catch_rate": 120},
    {"name": "Ludicolo", "catch_rate": 45},
    {"name": "Seedot", "catch_rate": 255},
    {"name": "Nuzleaf", "catch_rate": 120},
    {"name": "Shiftry", "catch_rate": 45},
    {"name": "Taillow", "catch_rate": 200},
    {"name": "Swellow", "catch_rate": 45},
    {"name": "Wingull", "catch_rate": 190},
    {"name": "Pelipper", "catch_rate": 45},
    {"name": "Ralts", "catch_rate": 235},
    {"name": "Kirlia", "catch_rate": 120},
    {"name": "Gardevoir", "catch_rate": 45},
    {"name": "Surskit", "catch_rate": 200},
    {"name": "Masquerain", "catch_rate": 75},
    {"name": "Shroomish", "catch_rate": 255},
    {"name": "Breloom", "catch_rate": 90},
    {"name": "Slakoth", "catch_rate": 255},
    {"name": "Vigoroth", "catch_rate": 120},
    {"name": "Slaking", "catch_rate": 45},
    {"name": "Nincada", "catch_rate": 255},
    {"name": "Ninjask", "catch_rate": 120},
    {"name": "Shedinja", "catch_rate": 45},
    {"name": "Whismur", "catch_rate": 190},
    {"name": "Loudred", "catch_rate": 120},
    {"name": "Exploud", "catch_rate": 45},
    {"name": "Makuhita", "catch_rate": 180},
    {"name": "Hariyama", "catch_rate": 200},
    {"name": "Azurill", "catch_rate": 150},
    {"name": "Nosepass", "catch_rate": 255},
    {"name": "Skitty", "catch_rate": 255},
    {"name": "Delcatty", "catch_rate": 60},
    {"name": "Sableye", "catch_rate": 45},
    {"name": "Mawile", "catch_rate": 45},
    {"name": "Aron", "catch_rate": 180},
    {"name": "Lairon", "catch_rate": 90},
    {"name": "Aggron", "catch_rate": 45},
    {"name": "Meditite", "catch_rate": 180},
    {"name": "Medicham", "catch_rate": 90},
    {"name": "Electrike", "catch_rate": 120},
    {"name": "Manectric", "catch_rate": 45},
    {"name": "Plusle", "catch_rate": 200},
    {"name": "Minun", "catch_rate": 200},
    {"name": "Volbeat", "catch_rate": 150},
    {"name": "Illumise", "catch_rate": 150},
    {"name": "Roselia", "catch_rate": 75},
    {"name": "Gulpin", "catch_rate": 225},
    {"name": "Swalot", "catch_rate": 75},
    {"name": "Carvanha", "catch_rate": 225},
    {"name": "Sharpedo", "catch_rate": 60},
    {"name": "Wailmer", "catch_rate": 125},
    {"name": "Wailord", "catch_rate": 60},
    {"name": "Numel", "catch_rate": 255},
    {"name": "Camerupt", "catch_rate": 150},
    {"name": "Torkoal", "catch_rate": 90},
    {"name": "Spoink", "catch_rate": 255},
    {"name": "Grumpig", "catch_rate": 60},
    {"name": "Spinda", "catch_rate": 255},
    {"name": "Trapinch", "catch_rate": 255},
    {"name": "Vibrava", "catch_rate": 120},
    {"name": "Flygon", "catch_rate": 45},
    {"name": "Cacnea", "catch_rate": 190},
    {"name": "Cacturne", "catch_rate": 60},
    {"name": "Swablu", "catch_rate": 255},
    {"name": "Altaria", "catch_rate": 45},
    {"name": "Zangoose", "catch_rate": 90},
    {"name": "Seviper", "catch_rate": 90},
    {"name": "Lunatone", "catch_rate": 45},
    {"name": "Solrock", "catch_rate": 45},
    {"name": "Barboach", "catch_rate": 190},
    {"name": "Whiscash", "catch_rate": 75},
    {"name": "Corphish", "catch_rate": 205},
    {"name": "Crawdaunt", "catch_rate": 155},
    {"name": "Baltoy", "catch_rate": 255},
    {"name": "Claydol", "catch_rate": 90},
    {"name": "Lileep", "catch_rate": 45},
    {"name": "Cradily", "catch_rate": 45},
    {"name": "Anorith", "catch_rate": 45},
    {"name": "Armaldo", "catch_rate": 45},
    {"name": "Feebas", "catch_rate": 255},
    {"name": "Milotic", "catch_rate": 60},
    {"name": "Castform", "catch_rate": 45},
    {"name": "Kecleon", "catch_rate": 200},
    {"name": "Shuppet", "catch_rate": 225},
    {"name": "Banette", "catch_rate": 45},
    {"name": "Duskull", "catch_rate": 190},
    {"name": "Dusclops", "catch_rate": 90},
    {"name": "Tropius", "catch_rate": 200},
    {"name": "Chimecho", "catch_rate": 45},
    {"name": "Absol", "catch_rate": 30},
    {"name": "Wynaut", "catch_rate": 125},
    {"name": "Snorunt", "catch_rate": 190},
    {"name": "Glalie", "catch_rate": 75},
    {"name": "Spheal", "catch_rate": 255},
    {"name": "Sealeo", "catch_rate": 120},
    {"name": "Walrein", "catch_rate": 45},
    {"name": "Clamperl", "catch_rate": 255},
    {"name": "Huntail", "catch_rate": 60},
    {"name": "Gorebyss", "catch_rate": 60},
    {"name": "Relicanth", "catch_rate": 25},
    {"name": "Luvdisc", "catch_rate": 225},
    {"name": "Bagon", "catch_rate": 45},
    {"name": "Shelgon", "catch_rate": 45},
    {"name": "Salamence", "catch_rate": 45},
    {"name": "Beldum", "catch_rate": 3},
    {"name": "Metang", "catch_rate": 3},
    {"name": "Metagross", "catch_rate": 3},
    {"name": "Regirock", "catch_rate": 3},
    {"name": "Regice", "catch_rate": 3},
    {"name": "Registeel", "catch_rate": 3},
    {"name": "Latias", "catch_rate": 3},
    {"name": "Latios", "catch_rate": 3},
    {"name": "Kyogre", "catch_rate": 5},
    {"name": "Groudon", "catch_rate": 5},
    {"name": "Rayquaza", "catch_rate": 3},
    {"name": "Jirachi", "catch_rate": 3},
    {"name": "Deoxys", "catch_rate": 3},
    {"name": "Turtwig", "catch_rate": 45},
    {"name": "Grotle", "catch_rate": 45},
    {"name": "Torterra", "catch_rate": 45},
    {"name": "Chimchar", "catch_rate": 45},
    {"name": "Monferno", "catch_rate": 45},
    {"name": "Infernape", "catch_rate": 45},
    {"name": "Piplup", "catch_rate": 45},
    {"name": "Prinplup", "catch_rate": 45},
    {"name": "Empoleon", "catch_rate": 45},
    {"name": "Starly", "catch_rate": 255},
    {"name": "Staravia", "catch_rate": 120},
    {"name": "Staraptor", "catch_rate": 45},
    {"name": "Bidoof", "catch_rate": 255},
    {"name": "Bibarel", "catch_rate": 127},
    {"name": "Kricketot", "catch_rate": 255},
    {"name": "Kricketune", "catch_rate": 45},
    {"name": "Shinx", "catch_rate": 235},
    {"name": "Luxio", "catch_rate": 120},
    {"name": "Luxray", "catch_rate": 45},
    {"name": "Budew", "catch_rate": 255},
    {"name": "Roserade", "catch_rate": 75},
    {"name": "Cranidos", "catch_rate": 45},
    {"name": "Rampardos", "catch_rate": 45},
    {"name": "Shieldon", "catch_rate": 45},
    {"name": "Bastiodon", "catch_rate": 45},
    {"name": "Burmy", "catch_rate": 120},
    {"name": "Wormadam", "catch_rate": 45},
    {"name": "Mothim", "catch_rate": 45},
    {"name": "Combee", "catch_rate": 120},
    {"name": "Vespiquen", "catch_rate": 45},
    {"name": "Pachirisu", "catch_rate": 200},
    {"name": "Buizel", "catch_rate": 190},
    {"name": "Floatzel", "catch_rate": 75},
    {"name": "Cherubi", "catch_rate": 190},
    {"name": "Cherrim", "catch_rate": 75},
    {"name": "Shellos", "catch_rate": 190},
    {"name": "Gastrodon", "catch_rate": 75},
    {"name": "Ambipom", "catch_rate": 45},
    {"name": "Drifloon", "catch_rate": 125},
    {"name": "Drifblim", "catch_rate": 60},
    {"name": "Buneary", "catch_rate": 190},
    {"name": "Lopunny", "catch_rate": 60},
    {"name": "Mismagius", "catch_rate": 45},
    {"name": "Honchkrow", "catch_rate": 30},
    {"name": "Glameow", "catch_rate": 190},
    {"name": "Purugly", "catch_rate": 75},
    {"name": "Chingling", "catch_rate": 120},
    {"name": "Stunky", "catch_rate": 225},
    {"name": "Skuntank", "catch_rate": 60},
    {"name": "Bronzor", "catch_rate": 255},
    {"name": "Bronzong", "catch_rate": 90},
    {"name": "Bonsly", "catch_rate": 255},
    {"name": "Mime Jr.", "catch_rate": 145},
    {"name": "Happiny", "catch_rate": 130},
    {"name": "Chatot", "catch_rate": 30},
    {"name": "Spiritomb", "catch_rate": 100},
    {"name": "Gible", "catch_rate": 45},
    {"name": "Gabite", "catch_rate": 45},
    {"name": "Garchomp", "catch_rate": 45},
    {"name": "Munchlax", "catch_rate": 50},
    {"name": "Riolu", "catch_rate": 75},
    {"name": "Lucario", "catch_rate": 45},
    {"name": "Hippopotas", "catch_rate": 140},
    {"name": "Hippowdon", "catch_rate": 60},
    {"name": "Skorupi", "catch_rate": 120},
    {"name": "Drapion", "catch_rate": 45},
    {"name": "Croagunk", "catch_rate": 140},
    {"name": "Toxicroak", "catch_rate": 75},
    {"name": "Carnivine", "catch_rate": 200},
    {"name": "Finneon", "catch_rate": 190},
    {"name": "Lumineon", "catch_rate": 75},
    {"name": "Mantyke", "catch_rate": 25},
    {"name": "Snover", "catch_rate": 120},
    {"name": "Abomasnow", "catch_rate": 60},
    {"name": "Weavile", "catch_rate": 45},
    {"name": "Magnezone", "catch_rate": 30},
    {"name": "Lickilicky", "catch_rate": 30},
    {"name": "Rhyperior", "catch_rate": 30},
    {"name": "Tangrowth", "catch_rate": 30},
    {"name": "Electivire", "catch_rate": 30},
    {"name": "Magmortar", "catch_rate": 30},
    {"name": "Togekiss", "catch_rate": 30},
    {"name": "Yanmega", "catch_rate": 30},
    {"name": "Leafeon", "catch_rate": 45},
    {"name": "Glaceon", "catch_rate": 45},
    {"name": "Gliscor", "catch_rate": 30},
    {"name": "Mamoswine", "catch_rate": 50},
    {"name": "Porygon-Z", "catch_rate": 30},
    {"name": "Gallade", "catch_rate": 45},
    {"name": "Probopass", "catch_rate": 60},
    {"name": "Dusknoir", "catch_rate": 45},
    {"name": "Froslass", "catch_rate": 75},
    {"name": "Rotom", "catch_rate": 45},
    {"name": "Uxie", "catch_rate": 3},
    {"name": "Mesprit", "catch_rate": 3},
    {"name": "Azelf", "catch_rate": 3},
    {"name": "Dialga", "catch_rate": 3},
    {"name": "Palkia", "catch_rate": 3},
    {"name": "Heatran", "catch_rate": 3},
    {"name": "Regigigas", "catch_rate": 3},
    {"name": "Giratina", "catch_rate": 3},
    {"name": "Cresselia", "catch_rate": 3},
    {"name": "Phione", "catch_rate": 30},
    {"name": "Manaphy", "catch_rate": 3},
    {"name": "Darkrai", "catch_rate": 3},
    {"name": "Shaymin", "catch_rate": 3},
    {"name": "Arceus", "catch_rate": 3},
    {"name": "Victini", "catch_rate": 3},
    {"name": "Snivy", "catch_rate": 45},
    {"name": "Servine", "catch_rate": 45},
    {"name": "Serperior", "catch_rate": 45},
    {"name": "Tepig", "catch_rate": 45},
    {"name": "Pignite", "catch_rate": 45},
    {"name": "Emboar", "catch_rate": 45},
    {"name": "Oshawott", "catch_rate": 45},
    {"name": "Dewott", "catch_rate": 45},
    {"name": "Samurott", "catch_rate": 45},
    {"name": "Patrat", "catch_rate": 255},
    {"name": "Watchog", "catch_rate": 255},
    {"name": "Lillipup", "catch_rate": 255},
    {"name": "Herdier", "catch_rate": 120},
    {"name": "Stoutland", "catch_rate": 45},
    {"name": "Purrloin", "catch_rate": 255},
    {"name": "Liepard", "catch_rate": 90},
    {"name": "Pansage", "catch_rate": 190},
    {"name": "Simisage", "catch_rate": 75},
    {"name": "Pansear", "catch_rate": 190},
    {"name": "Simisear", "catch_rate": 75},
    {"name": "Panpour", "catch_rate": 190},
    {"name": "Simipour", "catch_rate": 75},
    {"name": "Munna", "catch_rate": 190},
    {"name": "Musharna", "catch_rate": 75},
    {"name": "Pidove", "catch_rate": 255},
    {"name": "Tranquill", "catch_rate": 120},
    {"name": "Unfezant", "catch_rate": 45},
    {"name": "Blitzle", "catch_rate": 190},
    {"name": "Zebstrika", "catch_rate": 75},
    {"name": "Roggenrola", "catch_rate": 255},
    {"name": "Boldore", "catch_rate": 120},
    {"name": "Gigalith", "catch_rate": 45},
    {"name": "Woobat", "catch_rate": 190},
    {"name": "Swoobat", "catch_rate": 45},
    {"name": "Drilbur", "catch_rate": 120},
    {"name": "Excadrill", "catch_rate": 60},
    {"name": "Audino", "catch_rate": 255},
    {"name": "Timburr", "catch_rate": 180},
    {"name": "Gurdurr", "catch_rate": 90},
    {"name": "Conkeldurr", "catch_rate": 45},
    {"name": "Tympole", "catch_rate": 255},
    {"name": "Palpitoad", "catch_rate": 120},
    {"name": "Seismitoad", "catch_rate": 45},
    {"name": "Throh", "catch_rate": 45},
    {"name": "Sawk", "catch_rate": 45},
    {"name": "Sewaddle", "catch_rate": 255},
    {"name": "Swadloon", "catch_rate": 120},
    {"name": "Leavanny", "catch_rate": 45},
    {"name": "Venipede", "catch_rate": 255},
    {"name": "Whirlipede", "catch_rate": 120},
    {"name": "Scolipede", "catch_rate": 45},
    {"name": "Cottonee", "catch_rate": 190},
    {"name": "Whimsicott", "catch_rate": 75},
    {"name": "Petilil", "catch_rate": 190},
    {"name": "Lilligant", "catch_rate": 75},
    {"name": "Basculin", "catch_rate": 25},
    {"name": "Sandile", "catch_rate": 180},
    {"name": "Krokorok", "catch_rate": 90},
    {"name": "Krookodile", "catch_rate": 45},
    {"name": "Darumaka", "catch_rate": 120},
    {"name": "Darmanitan", "catch_rate": 60},
    {"name": "Maractus", "catch_rate": 255},
    {"name": "Dwebble", "catch_rate": 190},
    {"name": "Crustle", "catch_rate": 75},
    {"name": "Scraggy", "catch_rate": 180},
    {"name": "Scrafty", "catch_rate": 90},
    {"name": "Sigilyph", "catch_rate": 45},
    {"name": "Yamask", "catch_rate": 190},
    {"name": "Cofagrigus", "catch_rate": 90},
    {"name": "Tirtouga", "catch_rate": 45},
    {"name": "Carracosta", "catch_rate": 45},
    {"name": "Archen", "catch_rate": 45},
    {"name": "Archeops", "catch_rate": 45},
    {"name": "Trubbish", "catch_rate": 190},
    {"name": "Garbodor", "catch_rate": 60},
    {"name": "Zorua", "catch_rate": 75},
    {"name": "Zoroark", "catch_rate": 45},
    {"name": "Minccino", "catch_rate": 255},
    {"name": "Cinccino", "catch_rate": 60},
    {"name": "Gothita", "catch_rate": 200},
    {"name": "Gothorita", "catch_rate": 100},
    {"name": "Gothitelle", "catch_rate": 50},
    {"name": "Solosis", "catch_rate": 200},
    {"name": "Duosion", "catch_rate": 100},
    {"name": "Reuniclus", "catch_rate": 50},
    {"name": "Ducklett", "catch_rate": 190},
    {"name": "Swanna", "catch_rate": 45},
    {"name": "Vanillite", "catch_rate": 255},
    {"name": "Vanillish", "catch_rate": 120},
    {"name": "Vanilluxe", "catch_rate": 45},
    {"name": "Deerling", "catch_rate": 190},
    {"name": "Sawsbuck", "catch_rate": 75},
    {"name": "Emolga", "catch_rate": 200},
    {"name": "Karrablast", "catch_rate": 200},
    {"name": "Escavalier", "catch_rate": 75},
    {"name": "Foongus", "catch_rate": 190},
    {"name": "Amoonguss", "catch_rate": 75},
    {"name": "Frillish", "catch_rate": 190},
    {"name": "Jellicent", "catch_rate": 60},
    {"name": "Alomomola", "catch_rate": 75},
    {"name": "Joltik", "catch_rate": 190},
    {"name": "Galvantula", "catch_rate": 75},
    {"name": "Ferroseed", "catch_rate": 255},
    {"name": "Ferrothorn", "catch_rate": 90},
    {"name": "Klink", "catch_rate": 130},
    {"name": "Klang", "catch_rate": 60},
    {"name": "Klinklang", "catch_rate": 30},
    {"name": "Tynamo", "catch_rate": 190},
    {"name": "Eelektrik", "catch_rate": 60},
    {"name": "Eelektross", "catch_rate": 30},
    {"name": "Elgyem", "catch_rate": 255},
    {"name": "Beheeyem", "catch_rate": 90},
    {"name": "Litwick", "catch_rate": 190},
    {"name": "Lampent", "catch_rate": 90},
    {"name": "Chandelure", "catch_rate": 45},
    {"name": "Axew", "catch_rate": 75},
    {"name": "Fraxure", "catch_rate": 60},
    {"name": "Haxorus", "catch_rate": 45},
    {"name": "Cubchoo", "catch_rate": 120},
    {"name": "Beartic", "catch_rate": 60},
    {"name": "Cryogonal", "catch_rate": 25},
    {"name": "Shelmet", "catch_rate": 200},
    {"name": "Accelgor", "catch_rate": 75},
    {"name": "Stunfisk", "catch_rate": 75},
    {"name": "Mienfoo", "catch_rate": 180},
    {"name": "Mienshao", "catch_rate": 45},
    {"name": "Druddigon", "catch_rate": 45},
    {"name": "Golett", "catch_rate": 190},
    {"name": "Golurk", "catch_rate": 90},
    {"name": "Pawniard", "catch_rate": 120},
    {"name": "Bisharp", "catch_rate": 45},
    {"name": "Bouffalant", "catch_rate": 45},
    {"name": "Rufflet", "catch_rate": 190},
    {"name": "Braviary", "catch_rate": 60},
    {"name": "Vullaby", "catch_rate": 190},
    {"name": "Mandibuzz", "catch_rate": 60},
    {"name": "Heatmor", "catch_rate": 90},
    {"name": "Durant", "catch_rate": 90},
    {"name": "Deino", "catch_rate": 45},
    {"name": "Zweilous", "catch_rate": 45},
    {"name": "Hydreigon", "catch_rate": 45},
    {"name": "Larvesta", "catch_rate": 45},
    {"name": "Volcarona", "catch_rate": 15},
    {"name": "Cobalion", "catch_rate": 3},
    {"name": "Terrakion", "catch_rate": 3},
    {"name": "Virizion", "catch_rate": 3},
    {"name": "Tornadus", "catch_rate": 3},
    {"name": "Thundurus", "catch_rate": 3},
    {"name": "Reshiram", "catch_rate": 3},
    {"name": "Zekrom", "catch_rate": 3},
    {"name": "Landorus", "catch_rate": 3},
    {"name": "Kyurem", "catch_rate": 3},
    {"name": "Keldeo", "catch_rate": 3},
    {"name": "Meloetta", "catch_rate": 3},
    {"name": "Genesect", "catch_rate": 3},
    {"name": "Chespin", "catch_rate": 45},
    {"name": "Quilladin", "catch_rate": 45},
    {"name": "Chesnaught", "catch_rate": 45},
    {"name": "Fennekin", "catch_rate": 45},
    {"name": "Braixen", "catch_rate": 45},
    {"name": "Delphox", "catch_rate": 45},
    {"name": "Froakie", "catch_rate": 45},
    {"name": "Frogadier", "catch_rate": 45},
    {"name": "Greninja", "catch_rate": 45},
    {"name": "Bunnelby", "catch_rate": 255},
    {"name": "Diggersby", "catch_rate": 127},
    {"name": "Fletchling", "catch_rate": 255},
    {"name": "Fletchinder", "catch_rate": 120},
    {"name": "Talonflame", "catch_rate": 45},
    {"name": "Scatterbug", "catch_rate": 255},
    {"name": "Spewpa", "catch_rate": 120},
    {"name": "Vivillon", "catch_rate": 45},
    {"name": "Litleo", "catch_rate": 220},
    {"name": "Pyroar", "catch_rate": 65},
    {"name": "Flabébé", "catch_rate": 225},
    {"name": "Floette", "catch_rate": 120},
    {"name": "Florges", "catch_rate": 45}, 

]

# Global variables to track the group message count and the currently announced Pokémon
message_count = 0
announced_pokemon = None

# Create a Pyrogram client
api_id = 16743442
api_hash = '12bbd720f4097ba7713c5e40a11dfd2a'
bot_token = '6206599982:AAHJlIHxPWqMTpRP4iMvGb0I0pcOf_o-nG8'
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
        client.send_message(message.chat.id, "**Your Pokedex:**\n{}\n**Total Pokémon Caught:** {}".format(message.from_user.username, pokedex_list, pokemon_count), reply_to_message_id=message.message_id)
    else:
        client.send_message(message.chat.id, "Your Pokedex is empty.", reply_to_message_id=message.message_id)

# Function to get the user's name using Pyrogram's get_chat_member method
def get_user_name(user_id):
    chat_member = app.get_chat_member(chat_id="your_chat_id", user_id=user_id)  # Replace "your_chat_id" with your chat ID
    return chat_member.user.first_name if chat_member.user else "Unknown"

# Handler function for /topcatcher command
@app.on_message(filters.command("topcatcher"))
def top_catcher_command(client, message):
    top_catchers = collection.aggregate([
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ])
    
    top_catchers = list(top_catchers)  # Convert the result to a list
    
    if not top_catchers:
        client.send_message(chat_id=message.chat.id, text="No Pokemon catchers found.", reply_to_message_id=message.message_id)
        return
    
    top_catcher_text = "Top 5 Pokemon Catchers:\n"
    for i, catcher in enumerate(top_catchers, start=1):
        user_id = catcher["_id"]
        user_name = collection.find_one(user_id)  # Replace with your own logic to get the user's name
        catch_count = catcher["count"]
        top_catcher_text += f"{i}. {user_name} - {catch_count} Pokemon\n"

    client.send_message(chat_id=message.chat.id, text=top_catcher_text, reply_to_message_id=message.message_id)



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
            client.send_message(chat_id=message.chat.id, text="Congratulations! You caught {}!".format(announced_pokemon["name"], reply_to_message_id=message.message_id))
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
