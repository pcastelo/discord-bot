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

async def update_permissions():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    
    if not guild:
        print("Guild not found")
        await client.close()
        return

    print("--- 🔐 UPDATING PERMISSIONS ---")

    # Roles
    # Note: 'Administrator' role usually has implicit access, but we'll be explicit where needed or rely on the permission.
    # To 'hide' a channel from everyone else, we deny @everyone view_channel.
    
    role_admin = discord.utils.get(guild.roles, name="Administrator")
    role_gamers = discord.utils.get(guild.roles, name="Gamers")
    role_estudio = discord.utils.get(guild.roles, name="Estudio")
    role_invitados = discord.utils.get(guild.roles, name="Invitados") # Might verify if exists
    role_everyone = guild.default_role

    if not role_invitados:
        print("⚠️ Role 'Invitados' not found. Creating it...")
        try:
            role_invitados = await guild.create_role(name="Invitados", hoist=False, mentionable=False)
            print("✅ Created role 'Invitados'")
        except Exception as e:
            print(f"❌ Failed to create Invitados: {e}")

    # 1. 🔒 sudo (Voice Channel) -> Admin Only
    # It is likely in "🔊 VOZ" category.
    # We find the channel by name globally to be sure.
    # Assuming unique name 'sudo' or '🔒 sudo' (created in previous step)
    
    # We look for partial name "sudo"
    chan_sudo = discord.utils.find(lambda c: "sudo" in c.name.lower() and isinstance(c, discord.VoiceChannel), guild.channels)
    
    if chan_sudo:
        print(f"Configuring 'sudo' channel ({chan_sudo.name})...")
        # Deny everyone, Allow Admin
        overwrites = {
            role_everyone: discord.PermissionOverwrite(view_channel=False, connect=False),
            role_admin: discord.PermissionOverwrite(view_channel=True, connect=True)
            # Bot usually has admin so it sees it.
        }
        await chan_sudo.edit(overwrites=overwrites)
        print("✅ 'sudo' is now Admin-only.")
    else:
        print("⚠️ Channel 'sudo' not found.")

    # 2. 🎮 GAMING (Category) -> Admin + Gamers Only
    cat_gaming = discord.utils.find(lambda c: "GAMING" in c.name.upper(), guild.categories)
    
    if cat_gaming:
        print(f"Configuring 'GAMING' category ({cat_gaming.name})...")
        # Deny everyone, allow Gamers and Admin
        overwrites = {
            role_everyone: discord.PermissionOverwrite(view_channel=False),
            role_gamers: discord.PermissionOverwrite(view_channel=True, connect=True),
            role_admin: discord.PermissionOverwrite(view_channel=True, connect=True)
        }
        await cat_gaming.edit(overwrites=overwrites)
        print("✅ 'GAMING' category restricted to Gamers & Admins.")
    else:
        print("⚠️ 'GAMING' category not found.")

    # 3. 💬 SOCIAL (Category) -> Estudio + Invitados + Gamers + Admin
    # Basically everyone? Or specifically these roles?
    # Usually 'Social' is for everyone. If we deny @everyone, then people without roles see nothing.
    # User said: "estudio debe ver social al igual q invitados , obvciamente gamer ve lo mismo"
    # Implication: Non-role users (if any) shouldn't see it? Or just ensuring these roles DO see it.
    # Safest bet: Allow these specific roles, deny everyone else if that's the strict requirement.
    
    cat_social = discord.utils.find(lambda c: "SOCIAL" in c.name.upper(), guild.categories)
    
    if cat_social:
        print(f"Configuring 'SOCIAL' category ({cat_social.name})...")
        overwrites = {
            role_everyone: discord.PermissionOverwrite(view_channel=False), # Hide by default?
            role_estudio: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            role_invitados: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            role_gamers: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            role_admin: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        await cat_social.edit(overwrites=overwrites)
        print("✅ 'SOCIAL' category visible to: Estudio, Invitados, Gamers, Admin.")
    else:
        print("⚠️ 'SOCIAL' category not found.")

    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await update_permissions()

if __name__ == "__main__":
    client.run(TOKEN)
