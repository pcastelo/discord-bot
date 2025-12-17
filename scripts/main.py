import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

class CleanupBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
        try:
            guild = self.get_guild(int(GUILD_ID))
            if guild:
                print(f'Successfully connected to server: {guild.name} (ID: {guild.id})')
                print(f'Member count: {guild.member_count}')
            else:
                print(f'Could not find guild with ID {GUILD_ID}. Ensure bot is invited.')
        except Exception as e:
            print(f"Error fetching guild: {e}")

intents = discord.Intents.default()
# We need these intents to read members and content if privileged
intents.members = True 
intents.message_content = True

client = CleanupBot(intents=intents)

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
    else:
        client.run(TOKEN)
