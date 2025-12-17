import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import asyncio

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.bot import RoleIdentityView, SystemNotificationView 

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

    # Target channel: 'roles'
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

    print("Purging old panels (Limit 100)...")
    try:
        await channel.purge(limit=100) 
    except Exception as e:
        print(f"Purge error: {e}")

    # 1. Identity Panel
    print("Deploying Identity Panel...")
    embed_id = discord.Embed(title="🎭 Roles de Identidad", description="Elige tus roles para acceder a los canales.", color=0x00ff00)
    embed_id.add_field(name="Roles", value="🎮 **Gamers**: Canales de juegos.\n📚 **Estudio**: Zona de concentración.", inline=False)
    await channel.send(embed=embed_id, view=RoleIdentityView())
    
    # 2. Notification Panel
    print("Deploying Notification Panel...")
    embed_notif = discord.Embed(title="🔔 Notificaciones del Sistema", description="Suscríbete a las alertas que te interesen.", color=0xe74c3c)
    embed_notif.add_field(name="Alertas", value="📰 **Newsletter**: Novedades del proyecto.\n🛑 **Downtime**: Avisos de mantenimiento.\n🚀 **Releases**: Nuevas features del bot.", inline=False)
    await channel.send(embed=embed_notif, view=SystemNotificationView())
    
    print("✅ All Panels Sent!")
    
    await bot.close()

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment.")
    else:
        bot.run(TOKEN)
