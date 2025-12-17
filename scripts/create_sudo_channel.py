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

    # 1. Create/Get Category '🔒 INTERNAL' or '🔒 ADMIN'
    cat_name = "🔒 ADMIN"
    category = discord.utils.get(guild.categories, name=cat_name)
    
    if not category:
        print(f"Creating Category '{cat_name}'...")
        # Overwrites: Hide from everyone by default
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        category = await guild.create_category(cat_name, overwrites=overwrites)
    else:
        print(f"Category '{cat_name}' exists.")
        # Ensure hidden
        await category.set_permissions(guild.default_role, view_channel=False)

    # 2. Create Text Channel 'sudo'
    chan_name = "sudo"
    channel = discord.utils.get(category.text_channels, name=chan_name)
    
    if not channel:
        print(f"Creating text channel '#{chan_name}'...")
        channel = await guild.create_text_channel(chan_name, category=category)
        await channel.send("🤖 **Sudo Channel Initialized**\nEste canal es privado para administradores.")
        await channel.send("Usa este canal para comandos discretos (`!setup`, `!clear`) o logs del sistema.")
        print("✅ Channel created.")
    else:
        print(f"Channel '#{chan_name}' already exists.")

    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
