import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True # Needed to read messages

client = discord.Client(intents=intents)

async def clean_reglas():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    channel = discord.utils.get(guild.text_channels, name="reglas")
    if channel:
        print(f"🔎 Buscando mensajes del bot en #{channel.name}...")
        deleted_count = 0
        async for message in channel.history(limit=10):
            if message.author == client.user:
                print(f"🗑️ Borrando mensaje {message.id} (Embeds: {len(message.embeds)})")
                await message.delete()
                deleted_count += 1
        
        if deleted_count > 0:
            print(f"✅ Se borraron {deleted_count} mensajes en #reglas.")
        else:
            print("ℹ️ No encontré mensajes recientes del bot en #reglas.")
    else:
        print("❌ No encontré el canal #reglas.")

    await client.close()

@client.event
async def on_ready():
    await clean_reglas()

if __name__ == "__main__":
    client.run(TOKEN)
