import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import asyncio

# Load path relative to the script location if needed, or just assume .env in root
# Adjust path to find .env in parent directory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.bot import PersistentRoleView # Updated View Name

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

    # Use '📌 INFORMACIÓN' category
    category = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
    if not category:
        print("Category '📌 INFORMACIÓN' not found")
        await bot.close()
        return

    # Target channel: 'roles' or 'configuración'
    channel_name = "roles"
    channel = discord.utils.get(category.text_channels, name=channel_name)
    
    if not channel:
        print(f"Creating channel {channel_name}...")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False),
            guild.me: discord.PermissionOverwrite(send_messages=True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
    else:
        print(f"Channel {channel_name} exists.")

    # Send Panel
    print("Deploying Unified Panel...")
    embed = discord.Embed(title="🎛️ Panel de Configuración", description="Gestiona tus Roles y Notificaciones aquí.", color=0x00ff00)
    embed.add_field(name="Identidad", value="🎮 **Gamers**: Acceso a canales de juegos.\n👋 **Invitados**: Acceso social básico.", inline=True)
    embed.add_field(name="Alertas", value="📰 **Newsletter**: Noticias del proyecto.\n🛑 **Downtime**: Avisos de mantenimiento.", inline=True)
    
    await channel.send(embed=embed, view=PersistentRoleView())
    print("✅ Unified Panel Sent!")
    
    await bot.close()

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment.")
    else:
        bot.run(TOKEN)
