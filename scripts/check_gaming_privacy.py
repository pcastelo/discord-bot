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

    # List of private channels to check
    targets = ["COD", "BF6", "Equipo 1", "Equipo 2"]
    
    cat_gaming = discord.utils.get(guild.categories, name="🎮 GAMING")
    
    if cat_gaming:
        print(f"Checking channels in {cat_gaming.name}...")
        for vc in cat_gaming.voice_channels:
            # Check if name contains any target
            if any(t in vc.name for t in targets):
                print(f"\nCHANNEL: {vc.name}")
                
                # Check Everyone (Default Role)
                perm_everyone = vc.permissions_for(guild.default_role)
                print(f"  - @everyone: View={perm_everyone.view_channel}")

                # Check Estudio
                role_estudio = discord.utils.get(guild.roles, name="Estudio")
                if role_estudio:
                    perm_estudio = vc.permissions_for(role_estudio)
                    print(f"  - Estudio: View={perm_estudio.view_channel}")
                
                # Check Gamers
                role_gamers = discord.utils.get(guild.roles, name="Gamers")
                if role_gamers:
                    perm_gamers = vc.permissions_for(role_gamers)
                    print(f"  - Gamers: View={perm_gamers.view_channel}")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
