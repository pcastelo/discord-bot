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

# Target ID from backup analysis (will be filled after reading backup)
# Looking for "🔊 General Gaming" in backup
TARGET_NAME_OLD = "🔊 General Gaming"
TARGET_NAME_NEW = "🎮 General Gaming"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    # Load Backup to find ID
    with open("channel_names_backup.json", "r", encoding="utf-8") as f:
        backup = json.load(f)
    
    target_id = None
    for cid, name in backup.items():
        if name == TARGET_NAME_OLD:
            target_id = int(cid)
            break
    
    if not target_id:
        print(f"❌ Could not find '{TARGET_NAME_OLD}' in backup.")
    else:
        channel = guild.get_channel(target_id)
        if channel:
            print(f"Found Channel: {channel.name} ({channel.id})")
            if channel.name != TARGET_NAME_NEW:
                print(f"🚑 Rescuing: Renaming to '{TARGET_NAME_NEW}'")
                await channel.edit(name=TARGET_NAME_NEW)
                print("✅ Rescue Complete.")
            else:
                print("✅ Channel already has correct name.")
        else:
            print("❌ Channel ID found in backup but not in guild.")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
