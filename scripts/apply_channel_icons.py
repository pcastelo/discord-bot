import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# MAPPING: "Keyword to match" -> "New Full Name" (or "Prefix + CleanName")
# We will use exact match or contains logic
RENAME_MAP = {
    "bienvenida": "👋 bienvenida",
    "roles": "🎭 roles",
    "general": "💬 general",
    "memes": "🐸 memes",
    "musica": "🎵 musica",
    "chat-gaming": "🎮 chat-gaming",
    "General Gaming": "🎮 General Gaming",
    "COD": "🔫 COD",
    "BF6": "🪖 BF6",
    "Equipo 1": "🛡️ Equipo 1",
    "Equipo 2": "⚔️ Equipo 2",
    "Crear Sala": "➕ Crear Sala",
    "Lounge": "🛋️ Lounge",
    "Estudio": "📚 Estudio",
    "AFK": "💤 AFK",
    "sudo": "🔒 sudo",
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    print("Applying Icons...")
    
    # Iterate all channels
    for channel in guild.text_channels + guild.voice_channels:
        # Avoid stats channels (start with icons already usually, but let's be careful)
        if "Miembros" in channel.name or "Online" in channel.name or "Activos" in channel.name:
            continue
            
        # Clean current name (remove existing common emojis/prefixes to rematch)
        # Simplify: Just check if the core name is in our map
        
        # We try to match keys in RENAME_MAP to the current name
        # We strip common garbage "🔊 ", " " to find the key
        clean_name = channel.name.replace("🔊 ", "").replace(" ", "").lower()
        
        target_name = None
        
        # Sort keys by length descending to match "General Gaming" before "General"
        sorted_keys = sorted(RENAME_MAP.keys(), key=len, reverse=True)

        # Heuristic Match
        for key in sorted_keys:
            new_name = RENAME_MAP[key]
            # Check if key is contained in channel name (case insensitive)
            # OR if channel name is contained in key
            if key.replace(" ", "").lower() in clean_name:
                target_name = new_name
                break
            
            # Direct match check (more loose)
            if key.lower() in channel.name.lower():
                target_name = new_name
                break
        
        if target_name:
            if channel.name != target_name:
                print(f"✏️ Renaming '{channel.name}' -> '{target_name}'")
                try:
                    await channel.edit(name=target_name)
                    await asyncio.sleep(0.5) # Rate limit safety
                except Exception as e:
                    print(f"⚠️ Error renaming {channel.name}: {e}")
            else:
                 print(f"✅ '{channel.name}' is already correct.")
        else:
             print(f"⏭️ Skipping '{channel.name}' (No match)")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
