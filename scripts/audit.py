import os
import discord
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timezone

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

async def audit_server():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print(f"Error: Could not find guild with ID {GUILD_ID}")
        await client.close()
        return

    print(f"--- Audit Report for: {guild.name} ---")
    print(f"Member Count: {guild.member_count}")
    print("\n[Categories & Channels]")
    
    channels_data = []

    # Get all channels and sort by position
    for category in sorted(guild.categories, key=lambda x: x.position):
        print(f"\n📂 Category: {category.name.upper()} (ID: {category.id})")
        
        for channel in sorted(category.channels, key=lambda x: x.position):
            last_msg_info = "N/A"
            if isinstance(channel, discord.TextChannel):
                try:
                    # Fetch last message to determine activity
                    last_message = None
                    async for msg in channel.history(limit=1):
                        last_message = msg
                        break
                    
                    if last_message:
                        days_since = (datetime.now(timezone.utc) - last_message.created_at).days
                        last_msg_info = f"{days_since} days ago ({last_message.created_at.strftime('%Y-%m-%d')})"
                    else:
                        last_msg_info = "Never / Unknown"
                except Exception as e:
                    last_msg_info = f"Error fetching: {e}"
            
            print(f"  - {channel.type} | {channel.name} | Last Active: {last_msg_info}")
            channels_data.append({
                "name": channel.name,
                "type": str(channel.type),
                "last_active": last_msg_info,
                "category": category.name
            })

    print("\n[Roles]")
    for role in sorted(guild.roles, key=lambda x: x.position, reverse=True):
        print(f"  - {role.name} (Members: {len(role.members)})")

    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await audit_server()

if __name__ == "__main__":
    client.run(TOKEN)
