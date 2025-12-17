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

async def reorder_channels():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    print(f"--- 🧹 REORDERING CHANNELS: {guild.name} ---")

    category = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
    if not category:
        print("❌ Category '📌 INFORMACIÓN' not found.")
        await client.close()
        return

    # 1. Delete #reglas
    reglas_channel = discord.utils.get(category.text_channels, name="reglas")
    if reglas_channel:
        try:
            await reglas_channel.delete()
            print("✅ Deleted channel '#reglas'.")
        except Exception as e:
            print(f"❌ Failed to delete '#reglas': {e}")
    else:
        print("ℹ️ Channel '#reglas' not found (already deleted?).")

    # 2. Identify Channels for Reordering
    # Desired Order: Members (Voice), Online (Voice), bienvenida (Text), roles (Text)
    
    # Note: Discord sorting is tricky. Voice and Text channels are often separated visually by Discord clients regardless of position,
    # BUT in a mixed category, 'position' attribute is shared relative to the category? 
    # Actually, text and voice channels have separate lists in the UI usually, but we can try to set positions.
    # However, if they are all in one category, we can set absolute positions.
    
    # Let's find the objects
    chan_members = discord.utils.find(lambda c: c.name.startswith("👥"), category.voice_channels)
    chan_online = discord.utils.find(lambda c: c.name.startswith("🟢"), category.voice_channels)
    chan_bienvenida = discord.utils.get(category.text_channels, name="bienvenida")
    chan_roles = discord.utils.get(category.text_channels, name="roles")

    # We will construct a dict for edit_positions
    # {channel: position}
    
    # We want them at the very top of the category.
    # Positions are 0-indexed relative to the category? Or guild?
    # Usually it's better to use `category.edit_channels` or `guild.move_channel`.
    
    # Let's try `channel.edit(position=X)`.
    # Warning: Discord UI separates Text and Voice. Voice usually sits below text or vice versa depending on client settings? 
    # Wait, in a category, you can mix them, but usually they are grouped.
    # User asked: "miembros y onlie dejarlos arriba biernvenida sy luego roles"
    # This implies Stats (Voice) top, then Text.
    # Standard Discord behavior: Text channels usually appear above Voice channels in a category unless synced?
    # Actually, NO. Positions are strictly ordered. You can put Voice above Text.

    updates = {}
    current_pos = 0
    
    if chan_members:
        updates[chan_members] = current_pos
        current_pos += 1
        print(f"Planning: '👥 Miembros' -> Pos {updates[chan_members]}")
    
    if chan_online:
        updates[chan_online] = current_pos
        current_pos += 1
        print(f"Planning: '🟢 Online' -> Pos {updates[chan_online]}")
        
    if chan_bienvenida:
        updates[chan_bienvenida] = current_pos
        current_pos += 1
        print(f"Planning: '#bienvenida' -> Pos {updates[chan_bienvenida]}")

    if chan_roles:
        updates[chan_roles] = current_pos
        current_pos += 1
        print(f"Planning: '#roles' -> Pos {updates[chan_roles]}")

    try:
        # Applying changes
        # It's safer to move them one by one? Or use edit_positions if available on Category? Not directly.
        # We use guild.edit_channel_positions? No, that's old? Not sure.
        # `channel.edit(position=...)` is the standard way.
        
        for ch, pos in updates.items():
            await ch.edit(position=pos)
            print(f"✅ Moved {ch.name} to position {pos}")
            # Slight delay to ensure Discord processes the reorder
            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"❌ Failed to reorder: {e}")

    await client.close()

@client.event
async def on_ready():
    await reorder_channels()

if __name__ == "__main__":
    client.run(TOKEN)
