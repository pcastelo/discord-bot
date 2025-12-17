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
    if not guild:
         print("Guild not found")
         await bot.close()
         return

    everyone = guild.default_role
    print(f"Applying Default Permissions to @everyone ({everyone.name})...")

    # 1. INFORMACIÓN -> Visible
    cat_info = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
    if cat_info:
        await cat_info.set_permissions(everyone, view_channel=True, send_messages=False, connect=False)
        print("✅ Puesto INFORMACIÓN: Visible (Read-only)")
    else:
        print("⚠️ No encontré '📌 INFORMACIÓN'")

    # 2. SOCIAL -> Visible (Antes 'COMUNIDAD')
    cat_social = discord.utils.get(guild.categories, name="💬 SOCIAL")
    if cat_social:
        await cat_social.set_permissions(everyone, view_channel=True, send_messages=True)
        print("✅ Puesto SOCIAL: Visible")
    else:
         print("⚠️ No encontré '💬 SOCIAL'")

    # 3. GAMING -> Visible
    cat_gaming = discord.utils.get(guild.categories, name="🎮 GAMING")
    if cat_gaming:
        await cat_gaming.set_permissions(everyone, view_channel=True, send_messages=True)
        print("✅ Puesto GAMING: Visible")
    else:
         print("⚠️ No encontré '🎮 GAMING'")

    # 4. VOZ -> Visible (Antes 'ROOMS')
    cat_voz = discord.utils.get(guild.categories, name="🔊 VOZ")
    if cat_voz:
        await cat_voz.set_permissions(everyone, view_channel=True, connect=True)
        print("✅ Puesto VOZ: Visible")
    else:
         print("⚠️ No encontré '🔊 VOZ'")

    # 5. TECH & DEV -> Oculto (Si existe)
    cat_tech = discord.utils.get(guild.categories, name="💻 TECH & DEV")
    if cat_tech:
        await cat_tech.set_permissions(everyone, view_channel=False)
        print("🔒 Puesto TECH: Oculto")

    print("Permissions Finalized.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
