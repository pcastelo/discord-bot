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

    # Find '➕ Crear Sala'
    # It might be in GAMING or VOZ or somewhere else
    channel = None
    for vc in guild.voice_channels:
        if "Crear Sala" in vc.name:
            channel = vc
            break
    
    if not channel:
        print("❌ Could not find channel '➕ Crear Sala'")
    else:
        print(f"✅ Found Channel: {channel.name} (ID: {channel.id})")
        print(f"   Category: {channel.category.name if channel.category else 'None'}")
        
        # Check Overrides
        roles_to_check = ["@everyone", "Gamers", "Estudio"]
        for role_name in roles_to_check:
            role = guild.default_role if role_name == "@everyone" else discord.utils.get(guild.roles, name=role_name)
            if role:
                perms = channel.permissions_for(role)
                print(f"   - {role.name}: View={perms.view_channel}, Connect={perms.connect}")
            else:
                print(f"   - {role_name}: Role not found")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
