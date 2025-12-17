import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
try:
    ENV_GUILD_ID = int(os.getenv('GUILD_ID'))
except:
    ENV_GUILD_ID = None

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Configured GUILD_ID in .env: {ENV_GUILD_ID}")
    
    # List all connected guilds
    found = False
    for guild in bot.guilds:
        print(f"\n--- Connected Guild: {guild.name} (ID: {guild.id}) ---")
        if guild.id == ENV_GUILD_ID:
            print("✅ MATCHES .env configuration")
            found = True
        
        # Debug 'Estudio' Role
        estudio = discord.utils.get(guild.roles, name="Estudio")
        if estudio:
            print(f"Role 'Estudio' found (ID: {estudio.id})")
            if estudio.permissions.administrator:
                print("⚠️ CRITICAL: 'Estudio' has ADMINISTRATOR permission!")
            
            print("Category Overrides for 'Estudio':")
            for cat in guild.categories:
                overwrite = cat.overwrites_for(estudio)
                perms = []
                if overwrite.view_channel is not None: perms.append(f"View: {overwrite.view_channel}")
                if overwrite.connect is not None: perms.append(f"Connect: {overwrite.connect}")
                
                if perms:
                    print(f"  - {cat.name}: {', '.join(perms)}")
                else:
                    print(f"  - {cat.name}: (No specific overrides)")
        else:
            print("❌ Role 'Estudio' NOT found in this guild.")
            
    if not found:
        print(f"\n⚠️ WARNING: Bot is NOT connected to the guild ID specified in .env ({ENV_GUILD_ID})")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
