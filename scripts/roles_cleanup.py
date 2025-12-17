import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True # Needed to kick bots

client = discord.Client(intents=intents)

# Configuration
# Roles to KEEP (Normalized matches or Exact names)
ROLES_TO_KEEP = ["Administrator", "Gamers", "Estudio", "🤖| Bots", "villacastelo", "YAGPDB.xyz"]
# Note: "UAI" will be processed by renaming first, then it becomes "Estudio"

# Bots to KEEP (Username or Public Flags)
BOTS_TO_KEEP = ["villacastelo", "YAGPDB.xyz"]

async def cleanup_bots(guild):
    print("\n--- 🤖 BOT CLEANUP ---")
    for member in guild.members:
        if member.bot:
            if member.name in BOTS_TO_KEEP:
                print(f"✅ Keeping Bot: {member.name}")
            else:
                print(f"👋 Kicking Bot: {member.name} (ID: {member.id})")
                try:
                    await member.kick(reason="Server Cleanup: Unused Bot")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"❌ Failed to kick {member.name}: {e}")

async def cleanup_roles(guild):
    print("\n--- 🎭 ROLE CLEANUP ---")
    
    # 1. Rename logic
    role_uai = discord.utils.get(guild.roles, name="UAI")
    if role_uai:
        try:
            await role_uai.edit(name="Estudio")
            print("✅ Renamed role 'UAI' to 'Estudio'")
        except Exception as e:
            print(f"❌ Failed to rename UAI: {e}")
    
    # 2. Delete logic
    for role in guild.roles:
        if role.is_default(): continue # Skip @everyone
        if role.managed: 
            print(f"⏭️ Skipping Managed Role: {role.name}")
            continue # Skip bot integration roles
            
        # Check if we should keep it
        should_keep = False
        if role.name in ROLES_TO_KEEP:
            should_keep = True
        
        # Specific check for renamed role
        if role.name == "Estudio": 
            should_keep = True

        if should_keep:
            print(f"✅ Keeping Role: {role.name}")
        else:
            print(f"🗑 Deleting Role: {role.name}")
            try:
                await role.delete()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to delete {role.name}: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found")
        return

    await cleanup_bots(guild)
    await cleanup_roles(guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
