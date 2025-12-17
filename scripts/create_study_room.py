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

    # Roles
    everyone = guild.default_role
    role_estudio = discord.utils.get(guild.roles, name="Estudio")
    role_gamers = discord.utils.get(guild.roles, name="Gamers")

    if not role_estudio:
         # Auto-create Estudio role if missing?
         role_estudio = await guild.create_role(name="Estudio", mentionable=True, color=discord.Color.blue())
         print("Created role 'Estudio'")

    # Category: VOZ
    cat_voz = discord.utils.get(guild.categories, name="🔊 VOZ")
    if not cat_voz:
        print("❌ Category '🔊 VOZ' not found!")
        await bot.close()
        return

    # Check existence
    chan = discord.utils.get(cat_voz.voice_channels, name="🔊 Estudio")
    if not chan: chan = discord.utils.get(cat_voz.voice_channels, name="Estudio")

    if not chan:
        print("Creating '🔊 Estudio' channel...")
        overwrites = {
            everyone: discord.PermissionOverwrite(view_channel=False, connect=False),
            role_estudio: discord.PermissionOverwrite(view_channel=True, connect=True),
        }
        
        # Explicitly deny Gamers? 
        # Logic: If Gamers is separate from Everyone, and Everyone is denied, Gamers inherit denial unless they have explicit grant.
        # But if Gamers accidentally have 'Admin' or overwrite, we deny explicitly as requested.
        if role_gamers:
            overwrites[role_gamers] = discord.PermissionOverwrite(view_channel=False, connect=False)

        chan = await guild.create_voice_channel("🔊 Estudio", category=cat_voz, overwrites=overwrites)
        print("✅ Created and Secured '🔊 Estudio'")
    else:
        print(f"Channel {chan.name} exists. Updating perms...")
        await chan.set_permissions(everyone, view_channel=False, connect=False)
        await chan.set_permissions(role_estudio, view_channel=True, connect=True)
        if role_gamers:
            await chan.set_permissions(role_gamers, view_channel=False, connect=False)
        print("✅ Permissions Updated.")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
