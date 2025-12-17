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
    role_gamers = discord.utils.get(guild.roles, name="Gamers")
    if not role_gamers:
        # Create if missing just in case
        role_gamers = await guild.create_role(name="Gamers", mentionable=True)

    print(f"Applying Granular Permissions...")

    # --- CATEGORY: INFORMACIÓN ---
    cat_info = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
    if cat_info:
        await cat_info.set_permissions(everyone, view_channel=True, send_messages=False, connect=False)
        print("✅ INFO: Visible Read-only (@everyone)")

    # --- CATEGORY: SOCIAL ---
    cat_social = discord.utils.get(guild.categories, name="💬 SOCIAL")
    if cat_social:
        await cat_social.set_permissions(everyone, view_channel=True, send_messages=True)
        print("✅ SOCIAL: Visible (@everyone)")

    # --- CATEGORY: GAMING ---
    cat_gaming = discord.utils.get(guild.categories, name="🎮 GAMING")
    if cat_gaming:
        # 1. Hide Category from Everyone
        await cat_gaming.set_permissions(everyone, view_channel=False)
        print("🔒 GAMING Cat: Hidden (@everyone)")
        
        # 2. Show Category to Gamers
        await cat_gaming.set_permissions(role_gamers, view_channel=True)
        print("🔓 GAMING Cat: Visible (Gamers)")

        # 3. Whitelist 'General Gaming' for Everyone
        # Note: We need to find the specific channel.
        # Assuming typical names from previous list structure
        chan_gen = discord.utils.get(cat_gaming.voice_channels, name="🔊 General Gaming")
        if not chan_gen:
             chan_gen = discord.utils.get(cat_gaming.voice_channels, name="General Gaming")
        
        if chan_gen:
            await chan_gen.set_permissions(everyone, view_channel=True, connect=True)
            print("✅ GAMING/General: Visible (@everyone)")
        else:
            print("⚠️ Channel 'General Gaming' not found in Gaming category.")

    # --- CATEGORY: VOZ ---
    cat_voz = discord.utils.get(guild.categories, name="🔊 VOZ")
    if cat_voz:
        # 1. Hide Category from Everyone
        await cat_voz.set_permissions(everyone, view_channel=False)
        print("🔒 VOZ Cat: Hidden (@everyone)")

        # 2. Whitelist 'Lounge' and 'AFK'
        chan_lounge = discord.utils.get(cat_voz.voice_channels, name="🔊 Lounge")
        if not chan_lounge: chan_lounge = discord.utils.get(cat_voz.voice_channels, name="Lounge")

        chan_afk = discord.utils.get(cat_voz.voice_channels, name="🔊 🔇 AFK") 
        if not chan_afk: chan_afk = discord.utils.get(cat_voz.voice_channels, name="🔇 AFK") 
        if not chan_afk: chan_afk = discord.utils.get(cat_voz.voice_channels, name="AFK")

        for chan in [chan_lounge, chan_afk]:
            if chan:
                await chan.set_permissions(everyone, view_channel=True, connect=True)
                print(f"✅ VOZ/{chan.name}: Visible (@everyone)")
            else:
                 print(f"⚠️ Channel Lounge/AFK not found")

    # --- CATEGORY: TECH & DEV ---
    cat_tech = discord.utils.get(guild.categories, name="💻 TECH & DEV")
    if cat_tech:
        await cat_tech.set_permissions(everyone, view_channel=False)
        print("🔒 TECH: Hidden (@everyone)")

    print("Granular Permissions Applied.")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
