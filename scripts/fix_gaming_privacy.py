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
    if not guild: return

    everyone = guild.default_role
    role_gamers = discord.utils.get(guild.roles, name="Gamers")

    # List of channels to HIDE from Everyone but SHOW to Gamers
    hide_targets = ["COD", "BF6", "Equipo 1", "Equipo 2"]
    
    cat_gaming = discord.utils.get(guild.categories, name="🎮 GAMING")
    
    if cat_gaming:
        print(f"Locking down channels in {cat_gaming.name}...")
        for vc in cat_gaming.voice_channels:
            if any(t in vc.name for t in hide_targets):
                print(f"🔒 Locking: {vc.name}")
                
                # 1. Deny View to Everyone permission Explicitly
                await vc.set_permissions(everyone, view_channel=False, connect=False)
                
                # 2. Grant View to Gamers permission Explicitly
                if role_gamers:
                    await vc.set_permissions(role_gamers, view_channel=True, connect=True)
                
                print(f"   ✅ Done.")

    print("Privacy Fix Applied.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
