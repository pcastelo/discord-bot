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

BACKUP_FILE = "channel_names_backup.json"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    # Load Backup
    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            backup = json.load(f)
    except FileNotFoundError:
        print("❌ Backup file not found!")
        await bot.close()
        return

    print("Restoring Text Channels...")
    
    # Iterate Guild Text Channels
    for channel in guild.text_channels:
        str_id = str(channel.id)
        if str_id in backup:
            original_name = backup[str_id]
            
            # Check if current name matches original
            if channel.name != original_name:
                print(f"↺ Reverting '{channel.name}' -> '{original_name}'")
                try:
                    await channel.edit(name=original_name)
                    # Small delay to respect rate limits
                    await asyncio.sleep(0.5) 
                except Exception as e:
                    print(f"⚠️ Error reverting {channel.name}: {e}")
            else:
                print(f"✅ '{channel.name}' is unchanged.")
        else:
            print(f"❓ Channel {channel.name} ({channel.id}) not found in backup.")

    print("Text Channel Restoration Complete.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
