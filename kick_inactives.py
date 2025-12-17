import os
import discord
from dotenv import load_dotenv
from datetime import datetime, timezone
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

async def kick_inactives():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found")
        await client.close()
        return

    print(f"--- 👢 KICKING INACTIVE USERS: {guild.name} ---")
    
    now = datetime.now(timezone.utc)
    PROTECTED_ROLES = ["Administrator", "Gamers", "Estudio", "🤖| Bots", "villacastelo", "YAGPDB.xyz"]
    
    kicked_count = 0

    # Collect candidates first to avoid modifying list while iterating (though iterating members is safe usually)
    candidates = []

    for member in guild.members:
        if member.bot: continue

        has_protected_role = False
        member_role_names = [r.name for r in member.roles]
        
        for r_name in member_role_names:
            if r_name in PROTECTED_ROLES:
                has_protected_role = True
                break
        
        if not has_protected_role:
            if member.joined_at:
                days_in_server = (now - member.joined_at).days
                if days_in_server > 365:
                    candidates.append(member)

    print(f"Found {len(candidates)} users to kick.")

    for member in candidates:
        print(f"👋 Kicking: {member.name} (Joined {member.joined_at.strftime('%Y-%m-%d')})...")
        try:
            await member.kick(reason="Server Cleanup: Inactive / No Roles")
            print(f"✅ Kicked {member.name}")
            kicked_count += 1
            await asyncio.sleep(1) # Rate limit safety
        except Exception as e:
            print(f"❌ Failed to kick {member.name}: {e}")

    print(f"\n--- DONE. Total Kicked: {kicked_count} ---")
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await kick_inactives()

if __name__ == "__main__":
    client.run(TOKEN)
