import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

async def create_gaming_channel():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    print(f"--- 🎮 SETUP GAMING CHANNEL: {guild.name} ---")

    # Find Category
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if not category:
        category = discord.utils.get(guild.categories, name="GAMING")
    
    if category:
        # Check if exists
        channel = discord.utils.get(category.text_channels, name="chat-gaming")
        if not channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            channel = await guild.create_text_channel("chat-gaming", category=category, overwrites=overwrites)
            print(f"✅ Canal creado: {channel.name}")
            
            # Optional: Send a welcome message
            role_gamers = discord.utils.get(guild.roles, name="Gamers")
            mention = role_gamers.mention if role_gamers else "@everyone"
            await channel.send(f"🎮 **Gaming Zone** activada! Hola {mention}.")
        else:
            print(f"ℹ️ El canal {channel.name} ya existe.")
    else:
        print("❌ No encontré la categoría GAMING.")

    await client.close()

@client.event
async def on_ready():
    await create_gaming_channel()

if __name__ == "__main__":
    client.run(TOKEN)
