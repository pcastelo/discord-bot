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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found")
        await bot.close()
        return

    print(f"--- Structure for {guild.name} ---")
    for category in guild.categories:
        print(f"Category: {category.name} (ID: {category.id})")
        for channel in category.text_channels:
            print(f"  - # {channel.name}")
        for channel in category.voice_channels:
            print(f"  - 🔊 {channel.name}")
    print("-----------------------------------")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
