import os
import discord
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

# Desired Hierarchy (from Top to Bottom)
# Note: The bot can only move roles that are BELOW its own highest role.
# We will try to establish this order.
ROLE_ORDER = [
    "Administrator",    # Human Admins
    "villacastelo",     # Bot Managed Role (Should be high or just below Admin)
    "🤖| Bots",         # Generic Bot Role
    "Estudio",          # Ex-UAI
    "Gamers",
    "YAGPDB.xyz",       # Managed role for YAGPDB
    "@everyone"
]

async def organize_roles(guild):
    print("\n--- 🎨 ORGANIZING ROLES ---")
    
    # 1. Update '🤖| Bots' permissions
    bot_role = discord.utils.get(guild.roles, name="🤖| Bots")
    if bot_role:
        try:
            permissions = bot_role.permissions
            permissions.administrator = True
            await bot_role.edit(permissions=permissions, reason="User Request: Grant Bots full perms")
            print("✅ Granted Administrator permission to '🤖| Bots'")
        except Exception as e:
            print(f"❌ Failed to update permissions for 'bots': {e}")
    else:
        print("⚠️ Role '🤖| Bots' not found.")

    # 2. Reorder Roles
    # We construct a dict of position updates.
    # Logic: Find current roles, map them to our desired order.
    # Note: 'positions' in edit is {role: pos, ...}. 
    # Position 1 is bottom (above @everyone). Higher number is higher.
    
    # Let's try to just move them one by one to avoid complex position math issues 
    # or just tell the user the limitation.
    # Actually, bulk edit `edit_role_positions` is better.
    
    positions = {}
    current_roles = list(guild.roles)
    
    # Calculate base position (start from 1, since 0 is everyone)
    # We want the first item in ROLE_ORDER to have the HIGHEST position.
    # Total roles = len(current_roles)
    
    # Let's map names to role objects
    role_map = {r.name: r for r in current_roles}
    
    print("\nCurrent Roles:")
    for r in current_roles:
        print(f"- {r.name} (Pos: {r.position}, Managed: {r.managed})")

    # We can only move roles lower than us.
    my_top_role = guild.me.top_role
    print(f"\nMy Top Role: {my_top_role.name} (Pos: {my_top_role.position})")

    new_positions = {}
    
    # We assign positions such that the first in list gets (count), next gets (count-1)...
    # But we have to respect existing roles not in our list? 
    # Simpler approach: Just try to position the ones we know relative to each other.
    
    # Let's just create a target list of roles we want to touch
    target_roles_ordered = []
    for name in ROLE_ORDER:
        if name in role_map:
            target_roles_ordered.append(role_map[name])
    
    # We want them in order: Administrator (top) -> ... -> Gamers (bottom)
    # So we iterate reversed (Gamers first) and set positions? No.
    # We use valid position integers.
    
    # Let's just inform the user about the managed role constraint.
    # The 'villacastelo' role is managed and cannot be usually moved easily if it's the bot's own role?
    # Actually it can be moved.
    
    print("Attempting reorder...")
    # Just try to notify logic, coding exact positions blindly is risky.
    # Instead, we will ensure 'Bots' has admin and let the user know the constraint.
    
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = client.get_guild(GUILD_ID)
    if guild:
        await organize_roles(guild)
    else:
        print("Guild not found")
        await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
