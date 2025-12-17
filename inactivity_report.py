import os
import discord
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

async def check_inactivity():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found")
        await client.close()
        return

    print(f"--- 👥 INACTIVITY REPORT: {guild.name} ---")
    print(f"Total Members: {guild.member_count}")
    
    now = datetime.now(timezone.utc)
    
    candidates = []
    
    # Roles that protect a user from being kicked
    PROTECTED_ROLES = ["Administrator", "Gamers", "Estudio", "🤖| Bots", "villacastelo", "YAGPDB.xyz"]

    print("\n[Candidates for Kick (No Protected Roles + Joined > 1 Year ago)]")
    
    for member in guild.members:
        if member.bot: continue

        # Check roles
        has_protected_role = False
        member_role_names = [r.name for r in member.roles]
        
        for r_name in member_role_names:
            if r_name in PROTECTED_ROLES:
                has_protected_role = True
                break
        
        if not has_protected_role:
            # Check Join Date
            if member.joined_at:
                days_in_server = (now - member.joined_at).days
                joined_str = member.joined_at.strftime('%Y-%m-%d')
                
                # If joined more than 365 days ago
                if days_in_server > 365:
                    print(f"🔴 {member.name} (Joined: {joined_str}, {days_in_server} days ago) - Roles: {member_role_names}")
                    candidates.append(member)
                else:
                    print(f"🟡 {member.name} (Joined: {joined_str}, {days_in_server} days ago) - No roles, but new (<1 year).")
            else:
                print(f"❓ {member.name} (Unknown Join Date)")

    print(f"\nFound {len(candidates)} candidates for kicking.")
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await check_inactivity()

if __name__ == "__main__":
    client.run(TOKEN)
