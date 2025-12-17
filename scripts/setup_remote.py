import os
import discord
from discord.ui import View, Button
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

client = discord.Client(intents=intents)

# Re-define the View here to recreate it
class PersistentRoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🎮 Gamers", style=discord.ButtonStyle.primary, custom_id="role_gamers", emoji="🎮")
    async def gamer_button(self, interaction, button): pass
    @discord.ui.button(label="📚 Estudio", style=discord.ButtonStyle.success, custom_id="role_estudio", emoji="📚")
    async def estudio_button(self, interaction, button): pass
    @discord.ui.button(label="👋 Invitados", style=discord.ButtonStyle.secondary, custom_id="role_invitados", emoji="👋")
    async def invitados_button(self, interaction, button): pass

async def setup_server():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    print(f"--- 🛠️ SETUP AUTOMÁTICO: {guild.name} ---")

    # 1. SETUP VOZ (Channel)
    # Search with Emoji
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if not category:
        category = discord.utils.get(guild.categories, name="GAMING")
    
    if category:
        existing = discord.utils.get(category.voice_channels, name="➕ Crear Sala")
        if not existing:
            await category.create_voice_channel("➕ Crear Sala")
            print("✅ Voz: Canal '➕ Crear Sala' creado exitosamente.")
        else:
            print("ℹ️ Voz: El canal '➕ Crear Sala' ya existe.")
    else:
        print("❌ Voz: No encontré la categoría GAMING (ni con emoji).")

    # 2. SETUP ROLES (Message)
    # Target Channel: #roles
    target_category = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
    
    # Try to find #roles
    channel = discord.utils.get(guild.text_channels, name="roles")
    
    if not channel and target_category:
        print("ℹ️ Roles: Creando canal #roles...")
        # Create channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False) # Read only
        }
        channel = await guild.create_text_channel("roles", category=target_category, overwrites=overwrites)
    
    if channel:
        print(f"✅ Roles: Canal destino encontrado: #{channel.name}")
        # Clear previous messages? Optional. Let's just append.
        embed = discord.Embed(title="🎭 Auto-asignación de Roles", description="Haz click en los botones para obtener tus roles.", color=0x00ff00)
        await channel.send(embed=embed, view=PersistentRoleView())
        print("✅ Roles: Panel enviado con éxito a #roles.")
    else:
        print("❌ Roles: No pude encontrar ni crear el canal #roles (¿Falta categoría Información?).")

    await client.close()

@client.event
async def on_ready():
    await setup_server()

if __name__ == "__main__":
    client.run(TOKEN)
