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

CHANNELS_TO_RESTORE = [
    "🔫 COD",
    "🪖 BF6",
    "🛡️ Equipo 1",
    "⚔️ Equipo 2"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if not category:
        print("❌ Category '🎮 GAMING' not found!")
        return

    print("Restoring Channels...")
    
    for name in CHANNELS_TO_RESTORE:
        existing = discord.utils.get(category.voice_channels, name=name)
        if not existing:
            print(f"➕ Creating '{name}'...")
            await category.create_voice_channel(name)
        else:
            print(f"✅ '{name}' already exists.")

    print("Done.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
