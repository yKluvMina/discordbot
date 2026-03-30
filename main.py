import discord

import asyncio

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

intents.voice_states = True

client = discord.Client(intents=intents)   # On utilise Client au lieu de Bot (plus léger)

SALON_VOCAL = "yK"   # ← CHANGE ÇA avec le nom EXACT de ton salon vocal

async def keep_alive(voice_client):

    while voice_client.is_connected():

        try:

            voice_client.send_audio_packet(b'\xF8\xFF\xFE', encode=False)

            await asyncio.sleep(15)

        except:

            break

@client.event

async def on_ready():

    print(f"{client.user} est connecté et prêt !")

    for guild in client.guilds:

        channel = discord.utils.get(guild.voice_channels, name=SALON_VOCAL)

        if channel:

            try:

                vc = await channel.connect()

                print(f"✅ Connecté dans le vocal : {channel.name}")

                await keep_alive(vc)

                return

            except Exception as e:

                print(f"Erreur : {e}")

client.run(TOKEN)
