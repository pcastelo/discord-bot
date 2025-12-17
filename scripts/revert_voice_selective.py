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

# Keywords/Names to KEEP (Do NOT revert)
KEEP_LIST = ["General Gaming", "AFK", "Gaming", "Estudio"] # User didn't mention Estudio explicitly to revert, but he asked for it to be created. 
# Wait, user said "crea en Voz un canal Estudio...". 
# User said "los d etetos dejalos como estaban antes" (text restored).
# User said "loz de voz tambien , menos el de afk y el de general gaming".
# So "Estudio" should probably be reverted if it was in backup? 
# Estudio didn't exist in backup initially or was created recently.
# Let's check backup: "1450910754176761950": "🔊 Estudio". 
# Current name: "📚 Estudio".
# If I revert, it becomes "🔊 Estudio". 
# User said "menos el de afk y el de general gaming". 
# Strict interpretation: Revert Estudio too.
# However, "Estudio" is a new feature he asked for properly. "🔊 Estudio" has the speaker icon which he might consider "default/boring".
# But he said "loz de voz tambien".
# I will strictly follow: Exempt AFK and General Gaming.
# Everything else goes back to backup.
# If Estudio was not in backup (because it's new), it won't be in JSON? 
# I ran backup AFTER creating checks? No, backup was Step 1699. create_study_room was 1689.
# So Estudio IS in backup as "🔊 Estudio" (wait, create_study_room created "🔊 Estudio").
# Then apply_channel_icons renamed it to "📚 Estudio".
# So reverting will make it "🔊 Estudio". That seems to be what he wants (old style).

EXEMPT_KEYWORDS = ["General Gaming", "AFK"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild: return

    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
            backup = json.load(f)
    except FileNotFoundError:
        print("❌ Backup file not found!")
        await bot.close()
        return

    print("Restoring Voice Channels (Selectively)...")
    
    for channel in guild.voice_channels:
        # Check Exemption
        is_exempt = False
        for kw in EXEMPT_KEYWORDS:
            if kw.lower() in channel.name.lower():
                is_exempt = True
                break
        
        if is_exempt:
            print(f"🛑 Skipping '{channel.name}' (Exempt/Keep New)")
            continue

        str_id = str(channel.id)
        if str_id in backup:
            original_name = backup[str_id]
            
            if channel.name != original_name:
                print(f"↺ Reverting '{channel.name}' -> '{original_name}'")
                try:
                    await channel.edit(name=original_name)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            else:
                 print(f"✅ '{channel.name}' unchanged.")
        else:
            print(f"❓ '{channel.name}' not in backup (Skipping)")

    print("Voice Restoration Complete.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
