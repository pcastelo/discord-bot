import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

async def add_features():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found")
        await client.close()
        return

    # 1. Add Team channels to GAMING
    # Try to find the category with emoji or without just in case
    cat_gaming = discord.utils.get(guild.categories, name="🎮 GAMING")
    if cat_gaming:
        print("Found GAMING category. Adding Team channels...")
        # Check if they exist to avoid dupes? Nah, just create as requested.
        await cat_gaming.create_voice_channel("🔊 Equipo 1", user_limit=5)
        await cat_gaming.create_voice_channel("🔊 Equipo 2", user_limit=5)
        print("✅ Added Equipo 1 & 2")
    else:
        print("⚠️ GAMING category not found!")

    # 2. Add 'sudo' private channel to VOZ (General de Audio)
    cat_voice = discord.utils.get(guild.categories, name="🔊 VOZ")
    if cat_voice:
        print("Found VOZ category. Adding 'sudo' channel...")
        
        # Permission Overwrites: Hide from everyone except admins (admins bypass automaticlly)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=False)
        }
        
        await cat_voice.create_voice_channel("🔒 sudo", overwrites=overwrites)
        print("✅ Added 'sudo' private channel")
    else:
        print("⚠️ VOZ category not found!")
        
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await add_features()

if __name__ == "__main__":
    client.run(TOKEN)
