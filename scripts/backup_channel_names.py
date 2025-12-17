import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

OUTPUT_FILE = "channel_names_backup.json"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    backup_data = {}
    print(f"Backing up channel names for {guild.name}...")

    for channel in guild.text_channels + guild.voice_channels + guild.categories:
        backup_data[str(channel.id)] = channel.name
        print(f"  - {channel.name} ({channel.id})")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Backup saved to {OUTPUT_FILE}")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
