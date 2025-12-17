import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
# Need 'manage_channels' permission
intents.guilds = True

client = discord.Client(intents=intents)

# Categories to DELETE (Exact names from Audit or IDs)
# Using IDs is safer if names change, but names are easier to read.
# Based on audit, we will target by name keywords to be safe but aggressive.
TARGET_CATEGORIES_TO_DELETE = [
    "GENERAL", "UAI", "ARCHIVE UAI", "WORLD OF WARCRAFT", 
    "MUSIC", "JUEGOS", "JAIME", "AFK",  # We delete AFK category to recreate it properly in VOZ
    "AFK" 
]

async def delete_existing_channels(guild):
    print("--- 🗑 STARTING CLEANUP ---")
    # Iterate copy of categories to avoid modification issues
    for category in list(guild.categories):
        # Check if category matches our delete list (case insensitive partial match or exact ID)
        match = False
        cat_name_clean = category.name.replace("🔸", "").strip().upper() # Normalize name from audit "🔸 GENERAL 🔸"
        
        # Check against our target list
        for target in TARGET_CATEGORIES_TO_DELETE:
            if target in cat_name_clean:
                match = True
                break
        
        if match:
            print(f"Deleting Category: {category.name} and its channels...")
            for channel in category.channels:
                try:
                    await channel.delete()
                    print(f"  - Deleted channel: {channel.name}")
                    await asyncio.sleep(0.5) # Rate limit safety
                except Exception as e:
                    print(f"  ❌ Failed to delete channel {channel.name}: {e}")
            
            try:
                await category.delete()
                print(f"✅ Deleted Category: {category.name}")
            except Exception as e:
                print(f"❌ Failed to delete category {category.name}: {e}")
            
            await asyncio.sleep(1)

    # Also check for orphan channels not in categories?
    # For now, let's assume most are in categories.

async def create_new_structure(guild):
    print("\n--- 🏗 BUILDING NEW STRUCTURE ---")
    
    # 1. 📌 INFORMACIÓN
    print("Creating: 📌 INFORMACIÓN")
    cat_info = await guild.create_category("📌 INFORMACIÓN")
    await cat_info.create_text_channel("reglas")
    await cat_info.create_text_channel("bienvenida")
    
    # 2. 💬 SOCIAL
    print("Creating: 💬 SOCIAL")
    cat_social = await guild.create_category("💬 SOCIAL")
    await cat_social.create_text_channel("general")
    await cat_social.create_text_channel("memes")
    await cat_social.create_text_channel("musica")
    
    # 3. 🎮 GAMING
    print("Creating: 🎮 GAMING")
    cat_gaming = await guild.create_category("🎮 GAMING")
    await cat_gaming.create_voice_channel("🔊 General Gaming")
    await cat_gaming.create_voice_channel("🔊 COD")
    await cat_gaming.create_voice_channel("🔊 BF6")
    await cat_gaming.create_voice_channel("🔊 Duo", user_limit=2)
    await cat_gaming.create_voice_channel("🔊 Squad", user_limit=4)
    
    # 4. 🔊 VOZ
    print("Creating: 🔊 VOZ")
    cat_voice = await guild.create_category("🔊 VOZ")
    await cat_voice.create_voice_channel("🔊 Lounge")
    afk_channel = await cat_voice.create_voice_channel("🔇 AFK")
    
    # Set Guild AFK channel
    try:
        await guild.edit(afk_channel=afk_channel)
        print("✅ Set server AFK channel to new '🔇 AFK' channel.")
    except Exception as e:
        print(f"⚠️ Could not set system AFK channel setting: {e}")

    print("--- ✨ RESTRUCTURE COMPLETE ✨ ---")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found!")
        return

    await delete_existing_channels(guild)
    await create_new_structure(guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
