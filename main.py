import discord
from discord.ext import tasks
import asyncio
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Configuration des intents (requis pour les états vocaux et les guildes)
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

# Utilisation de Client (ou Bot si vous préférez plus d'outils)
client = discord.Client(intents=intents)

# Configuration du salon vocal
SALON_VOCAL_NOM = "yK"  # ← CHANGE ÇA avec le nom EXACT de ton salon vocal

@tasks.loop(seconds=20)
async def check_voice_connection():
    """Vérifie périodiquement que le bot est dans le bon salon vocal"""
    if not client.is_ready():
        return

    for guild in client.guilds:
        # Trouver le salon par son nom
        channel = discord.utils.get(guild.voice_channels, name=SALON_VOCAL_NOM)
        
        if channel:
            # Vérifier si on est déjà connecté dans cette guilde
            vc = discord.utils.get(client.voice_clients, guild=guild)
            
            if not vc or not vc.is_connected():
                try:
                    print(f"🔄 Tentative de connexion à {channel.name} dans {guild.name}...")
                    await channel.connect()
                    print(f"✅ Connecté avec succès !")
                except Exception as e:
                    print(f"❌ Erreur lors de la connexion : {e}")

@client.event
async def on_ready():
    print(f"🚀 {client.user} est connecté et opérationnel !")
    
    # Démarrer la boucle de surveillance si elle n'est pas déjà lancée
    if not check_voice_connection.is_running():
        check_voice_connection.start()

# Lancement du bot
if TOKEN:
    client.run(TOKEN)
else:
    print("❌ Erreur : Le TOKEN 'DISCORD_TOKEN' est introuvable dans le fichier .env")
