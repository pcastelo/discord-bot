import os
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv
from easy_pil import Editor, Canvas, Font, load_image_async
import asyncio
import json
import aiohttp
import io
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
TEMP_ROLES_FILE = "temp_roles.json"
TEMP_CHANNELS_FILE = "temp_voice_channels.json"

def load_temp_channels():
    if not os.path.exists(TEMP_CHANNELS_FILE):
        return []
    try:
        with open(TEMP_CHANNELS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_temp_channels(channels):
    with open(TEMP_CHANNELS_FILE, "w") as f:
        json.dump(channels, f)

def add_temp_channel(channel_id):
    channels = load_temp_channels()
    if channel_id not in channels:
        channels.append(channel_id)
        save_temp_channels(channels)

def remove_temp_channel(channel_id):
    channels = load_temp_channels()
    if channel_id in channels:
        channels.remove(channel_id)
        save_temp_channels(channels)

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.presences = True

class RoleIdentityView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction: discord.Interaction, role_name: str, emoji: str):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
             await interaction.response.send_message(f"❌ El rol **{role_name}** no existe.", ephemeral=True)
             return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"❌ Te has quitado el rol de **{role_name}**.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ {emoji} Rol de **{role_name}** asignado.", ephemeral=True)

    @discord.ui.button(label="Gamers", style=discord.ButtonStyle.primary, custom_id="role_gamers", emoji="🎮")
    async def gamer_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, "Gamers", "🎮")

    @discord.ui.button(label="Estudio", style=discord.ButtonStyle.success, custom_id="role_estudio", emoji="📚")
    async def estudio_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, "Estudio", "📚")


class SystemNotificationView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_notif(self, interaction: discord.Interaction, role_name: str, emoji: str):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
             # Auto-create for System Notifications
             role = await interaction.guild.create_role(name=role_name, mentionable=False, reason="Auto-created Notification Role")
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"🔕 Notificaciones de **{role_name}** desactivadas.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"🔔 Notificaciones de **{role_name}** activadas.", ephemeral=True)

    @discord.ui.button(label="Newsletter", style=discord.ButtonStyle.primary, custom_id="notif_newsletter", emoji="📰")
    async def newsletter_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_notif(interaction, "Newsletter", "📰")

    @discord.ui.button(label="Downtime", style=discord.ButtonStyle.danger, custom_id="notif_downtime", emoji="🛑")
    async def downtime_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_notif(interaction, "Downtime", "🛑")

    @discord.ui.button(label="Releases", style=discord.ButtonStyle.success, custom_id="notif_releases", emoji="🚀")
    async def releases_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_notif(interaction, "Releases", "🚀")

class SuperBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None) # Disable default help
        self.persistent_views_added = False

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        if not self.persistent_views_added:
            self.add_view(RoleIdentityView())
            self.add_view(SystemNotificationView())
            self.persistent_views_added = True
        
        # Start Loops
        if not self.update_stats.is_running():
            self.update_stats.start()
        
        if not self.check_temp_roles.is_running():
            self.check_temp_roles.start()
        
        # NOTE: User explicitly requested to NOT disable mention_everyone automatically.
        # Reverted Security block.

        print("Bot is Ready!")

def get_ordinal(n):
    if 11 <= (n % 100) <= 13: suffix = 'th'
    else: suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

    async def on_member_join(self, member):
        # FEATURE 1: WELCOME IMAGES
        channel = discord.utils.get(member.guild.text_channels, name="bienvenida")
        if channel:
            # Create Image - Member Count Style
            background = Editor(Canvas((900, 300), color="#23272A"))
            
            profile_image = await load_image_async(str(member.display_avatar.url))
            profile = Editor(profile_image).resize((190, 190)).circle_image()
            
            poppins = Font.poppins(size=50, variant="bold")
            poppins_med = Font.poppins(size=40, variant="bold")
            poppins_small = Font.poppins(size=30, variant="light")

            # Left Avatar (Centered in 300px height is y=55)
            background.paste(profile, (30, 55))
            background.ellipse((30, 55), 190, 190, outline="#00ff00", stroke_width=5)
            
            # Text Elements
            guild_name = member.guild.name
            ordinal = get_ordinal(member.guild.member_count)
            
            background.text((250, 60), f"Welcome {member.name}", color="white", font=poppins)
            background.text((250, 120), f"to {guild_name}", color="#00ff00", font=poppins_med)
            background.text((250, 180), f"you are the {ordinal} user", color="white", font=poppins_small)

            file = discord.File(fp=background.image_bytes, filename="welcome.png")
            
            # Find roles channel for mention
            roles_channel = discord.utils.get(member.guild.text_channels, name="roles")
            
            # New Message Format
            welcome_text = f"Welcome {member.mention} to **{guild_name}**. You are the **{ordinal}** user!"
            
            if roles_channel:
                welcome_text += f"\nNo olvides pasar por {roles_channel.mention} para asignarte tus roles."
            
            await channel.send(welcome_text, file=file)

    async def on_voice_state_update(self, member, before, after):
        # FEATURE 3: DYNAMIC VOICE CHANNELS
        guild = member.guild
        
        # 1. CREATE CHANNEL
        if after.channel and after.channel.name == "➕ Crear Sala":
            # Target Category
            category = after.channel.category
            
            # Use 'General Gaming' as a template or just create default
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True),
                member: discord.PermissionOverwrite(manage_channels=True, move_members=True)
            }
            
            channel_name = f"🔊 Sala de {member.display_name}"
            new_channel = await guild.create_voice_channel(name=channel_name, category=category, overwrites=overwrites)
            
            # TRACKING: Save ID
            add_temp_channel(new_channel.id)

            # Move member
            await member.move_to(new_channel)
            print(f"Created temp channel: {channel_name} (ID: {new_channel.id})")

        # 2. DELETE EMPTY TEMPORARY CHANNEL
        if before.channel:
            # Check if this channel is in our Tracking List
            temp_ids = load_temp_channels()
            
            if before.channel.id in temp_ids:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    remove_temp_channel(before.channel.id)
                    print(f"Deleted empty temp channel: {before.channel.name} (ID: {before.channel.id})")

    @tasks.loop(minutes=6)
    async def update_stats(self):
        # FEATURE 4: SERVER STATS
        guild = self.get_guild(GUILD_ID)
        if not guild: return

        member_count = guild.member_count
        online_members = [m for m in guild.members if m.status != discord.Status.offline and not m.bot]
        online_count = len(online_members)
        print(f"DEBUG STATS: Online Humans ({online_count}): {[m.name for m in online_members]}")
        
        category = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
        if not category: return

        # Stat 1: Miembros
        chan_members = discord.utils.find(lambda c: c.name.startswith("👥 Miembros:"), category.channels)
        if not chan_members:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_members = await guild.create_voice_channel(f"👥 Miembros: {member_count}", category=category, overwrites=overwrites)
        else:
            if chan_members.name != f"👥 Miembros: {member_count}":
                await chan_members.edit(name=f"👥 Miembros: {member_count}")

        # Stat 2: Online
        chan_online = discord.utils.find(lambda c: c.name.startswith("🟢 Online:"), category.channels)
        if not chan_online:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_online = await guild.create_voice_channel(f"🟢 Online: {online_count}", category=category, overwrites=overwrites)
        else:
            if chan_online.name != f"🟢 Online: {online_count}":
                await chan_online.edit(name=f"🟢 Online: {online_count}")
        
        # Stat 3: Voice (Activos)
        voice_members = [m for vc in guild.voice_channels for m in vc.members if not m.bot]
        voice_count = len(voice_members)
        print(f"DEBUG STATS: Voice Humans ({voice_count}): {[m.name for m in voice_members]}")

        chan_voice = discord.utils.find(lambda c: c.name.startswith("🎧 Activos:"), category.channels)
        if not chan_voice:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_voice = await guild.create_voice_channel(f"🎧 Activos: {voice_count}", category=category, overwrites=overwrites)
        else:
            if chan_voice.name != f"🎧 Activos: {voice_count}":
                await chan_voice.edit(name=f"🎧 Activos: {voice_count}")

    @tasks.loop(minutes=60)
    async def check_temp_roles(self):
        # FEATURE: TEMP ROLES CHECKER
        if not os.path.exists(TEMP_ROLES_FILE):
             return
            
        try:
            with open(TEMP_ROLES_FILE, "r") as f:
                temp_roles = json.load(f)
        except:
            temp_roles = []
            
        guild = self.get_guild(GUILD_ID)
        if not guild: return
        
        now = datetime.now()
        updated_roles = []
        
        for entry in temp_roles:
            expiration = datetime.fromisoformat(entry['expires_at'])
            if now > expiration:
                # Expired: Remove Role
                member = guild.get_member(entry['user_id'])
                if member:
                    role = guild.get_role(entry['role_id'])
                    if role:
                        try:
                             await member.remove_roles(role)
                             print(f"Expired Temp Role: Removed {role.name} from {member.display_name}")
                        except Exception as e:
                             print(f"Error removing role: {e}")
            else:
                updated_roles.append(entry)
        
        # Save updates
        if len(updated_roles) != len(temp_roles):
             with open(TEMP_ROLES_FILE, "w") as f:
                 json.dump(updated_roles, f)

bot = SuperBot()

# --- COMMANDS ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🤖 Comandos de La Villa", color=0x3498db)
    
    embed.add_field(name="🎮 Gaming", value="`!gaming` - Avisa a los Gamers (Solo en #chat-gaming)", inline=False)
    embed.add_field(name="🔊 Voz", value="`!room [nombre]` - Cambia el nombre de tu sala temporal", inline=False)
    embed.add_field(name="🖼️ Utilidad", value="`!avatar @user` - Ver foto de perfil\n`!poll \"Pregunta\" \"Opción1\"...` - Crear encuesta", inline=False)
    
    if ctx.author.guild_permissions.administrator:
        embed.add_field(name="🛡️ Admin", value="`!setup_roles` - Roles\n`!setup_notifications` - Notif.\n`!tempRole` - Roles Temp\n`!addEmoji` - Emojis\n`!addSound` - Sonidos", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title=f"Avatar de {member.display_name}", color=member.color)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Borrados {amount} mensajes.", delete_after=3)

@bot.command()
async def poll(ctx, question, *options):
    if len(options) == 0:
        await ctx.send("❌ Uso: `!poll \"Pregunta\" \"Opcion A\" \"Opcion B\"`")
        return
    if len(options) > 10:
        await ctx.send("❌ Máximo 10 opciones.")
        return

    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    description = []
    for x, option in enumerate(options):
        description.append(f"{reactions[x]} {option}")
    
    embed = discord.Embed(title=f"📊 {question}", description="\n\n".join(description), color=0xffd700)
    embed.set_footer(text=f"Encuesta iniciada por {ctx.author.display_name}")
    
    poll_msg = await ctx.send(embed=embed)
    for i in range(len(options)):
         await poll_msg.add_reaction(reactions[i])

@bot.command()
async def room(ctx, *, new_name):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ Debes estar en un canal de voz.", delete_after=5)
        return

    channel = ctx.author.voice.channel
    
    # Check if it is a temp channel (ID based)
    temp_ids = load_temp_channels()
    if channel.id not in temp_ids:
         await ctx.send("❌ Solo puedes renombrar salas temporales creadas por el bot.", delete_after=5)
         return
    permissions = channel.permissions_for(ctx.author)
    if not permissions.manage_channels:
         await ctx.send("❌ No eres el dueño de esta sala.", delete_after=5)
         return
    
    try:
        name_to_set = f"🔊 {new_name}"
        await channel.edit(name=name_to_set)
        await ctx.send(f"✅ Sala renombrada a **{name_to_set}**", delete_after=5)
    except discord.RateLimited:
         await ctx.send("⏳ Discord limita los cambios de nombre (2 veces cada 10 min). Espera un poco.", delete_after=10)
    except Exception as e:
         print(f"Error renaming room: {e}")
         await ctx.send("❌ Error cambiando el nombre.", delete_after=5)

@bot.command()
@commands.has_permissions(administrator=True)
async def tempRole(ctx, role_name: str, members: commands.Greedy[discord.Member], days: int):
    # Search for the role
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ No encuentro el rol: **{role_name}**")
        return

    if not members:
        await ctx.send("❌ Debes mencionar al menos a un usuario. Uso: `!tempRole Admin @User 7`")
        return

    expiration_date = datetime.now() + timedelta(days=days)
    expiration_iso = expiration_date.isoformat()
    
    # Load Existing
    if os.path.exists(TEMP_ROLES_FILE):
        with open(TEMP_ROLES_FILE, "r") as f:
            try:
                temp_data = json.load(f)
            except:
                temp_data = []
    else:
        temp_data = []

    assigned_names = []
    for member in members:
        await member.add_roles(role)
        assigned_names.append(member.display_name)
        
        # Add to tracking
        temp_data.append({
            "user_id": member.id,
            "role_id": role.id,
            "expires_at": expiration_iso
        })

    # Save
    with open(TEMP_ROLES_FILE, "w") as f:
        json.dump(temp_data, f)
        
    await ctx.send(f"✅ Rol **{role.name}** asignado a {', '.join(assigned_names)} por **{days} días** (Hasta: {expiration_date.strftime('%Y-%m-%d')}).")

@bot.command()
@commands.has_permissions(administrator=True)
async def addEmoji(ctx, name: str, url: str = None):
    # Logic: If URL is provided use it, otherwise check for attachment
    image_bytes = None
    
    if ctx.message.attachments:
        url = ctx.message.attachments[0].url
    
    if not url:
        await ctx.send("❌ Debes proporcionar una URL o adjuntar una imagen.")
        return
        
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await ctx.send("❌ No pude descargar la imagen.")
                return
            image_bytes = await resp.read()

    try:
        emoji = await ctx.guild.create_custom_emoji(name=name, image=image_bytes)
        await ctx.send(f"✅ Emoji creado: {emoji}")
    except Exception as e:
        await ctx.send(f"❌ Error al crear emoji: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def addSound(ctx, name: str):
    # Check attachments
    if not ctx.message.attachments:
        await ctx.send("❌ Debes adjuntar un archivo de audio (MP3/OGG).")
        return
    
    attachment = ctx.message.attachments[0]
    
    # Needs permissions check in API or library version check
    # Soundboard support was added in recent discord.py versions
    try:
        # Read file
        audio_bytes = await attachment.read()
        
        # Create sound
        # Note: Guild.create_soundboard_sound exists in recent d.py master/2.4+
        # If this fails, it means the library version on VPS is too old.
        # We will wrap in try/except.
        
        if hasattr(ctx.guild, 'create_soundboard_sound'):
            sound = await ctx.guild.create_soundboard_sound(name=name, sound=audio_bytes, emoji=None)
            await ctx.send(f"✅ Sonido **{name}** añadido al Soundboard!")
        else:
             await ctx.send("⚠️ Tu versión de bot no soporta Soundboard nativo aun (Requiere update de librería).")
    except Exception as e:
        await ctx.send(f"❌ Error subiendo sonido: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="🎭 Roles de Identidad", description="Elige tus roles para acceder a los canales.", color=0x00ff00)
    embed.add_field(name="Roles", value="🎮 **Gamers**: Canales de juegos.\n📚 **Estudio**: Zona de concentración.", inline=False)
    await ctx.send(embed=embed, view=RoleIdentityView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_notifications(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="🔔 Notificaciones del Sistema", description="Suscríbete a las alertas que te interesen.", color=0xe74c3c)
    embed.add_field(name="Alertas", value="📰 **Newsletter**: Novedades del proyecto.\n🛑 **Downtime**: Avisos de mantenimiento.\n🚀 **Releases**: Nuevas features del bot.", inline=False)
    await ctx.send(embed=embed, view=SystemNotificationView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_voice(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if category:
        existing = discord.utils.get(category.voice_channels, name="➕ Crear Sala")
        if not existing:
            await category.create_voice_channel("➕ Crear Sala")
            await ctx.send("✅ Canal '➕ Crear Sala' creado.")
        else:
            await ctx.send("El canal ya existe.")
    else:
        await ctx.send("No encuentro la categoría GAMING.")

@bot.command(aliases=["gaming"])
async def Gaming(ctx):
    if ctx.channel.name != "chat-gaming":
        try:
             await ctx.message.delete() 
        except:
             pass 
        await ctx.send("❌ Este comando solo funciona en #chat-gaming.", delete_after=300)
        return

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if not category:
        category = discord.utils.get(guild.categories, name="GAMING")
    
    if not category:
        await ctx.send("❌ No encuentro la categoría GAMING.")
        return

    target_channel = ctx.channel
    role_gamers = discord.utils.get(guild.roles, name="Gamers")
    mention = role_gamers.mention if role_gamers else "@everyone"
    
    await target_channel.send(f"🎮 **Gaming Time** {mention} by {ctx.author.mention}!")

@bot.event
async def on_presence_update(before, after):
    role_gamers = discord.utils.get(after.guild.roles, name="Gamers")
    if role_gamers not in after.roles:
        return

    is_streaming = isinstance(after.activity, discord.Streaming)
    was_streaming = isinstance(before.activity, discord.Streaming)

    if is_streaming and not was_streaming:
        stream_url = after.activity.url
        stream_name = after.activity.name 
        
        category = discord.utils.get(after.guild.categories, name="🎮 GAMING")
        if not category:
             category = discord.utils.get(after.guild.categories, name="GAMING")
        
        target_channel = None
        if category:
            target_channel = discord.utils.get(category.text_channels, name="chat-gaming")
        
        if target_channel:
             await target_channel.send(f"🔴 **¡{after.mention} está en directo!**\n📺 **{stream_name}**\n🔗 {stream_url}")

if __name__ == "__main__":
    bot.run(TOKEN)

    async def on_member_join(self, member):
        # FEATURE 1: WELCOME IMAGES
        channel = discord.utils.get(member.guild.text_channels, name="bienvenida")
        if channel:
            # Create Image
            background = Editor(Canvas((900, 270), color="#23272A"))
            profile_image = await load_image_async(str(member.display_avatar.url))
            profile = Editor(profile_image).resize((190, 190)).circle_image()
            
            poppins = Font.poppins(size=50, variant="bold")
            poppins_small = Font.poppins(size=30, variant="light")

            background.paste(profile, (30, 40))
            background.ellipse((30, 40), 190, 190, outline="#00ff00", stroke_width=5)
            background.text((260, 80), "BIENVENIDO", color="white", font=poppins)
            background.text((260, 140), f"{member.name}", color="#00ff00", font=poppins)
            background.text((260, 200), f"A LA VILLA", color="white", font=poppins_small)

            file = discord.File(fp=background.image_bytes, filename="welcome.png")
            
            # Find roles channel for mention
            roles_channel = discord.utils.get(member.guild.text_channels, name="roles")
            welcome_text = f"Hola {member.mention}, bienvenido al servidor!"
            if roles_channel:
                welcome_text += f"\nNo olvides pasar por {roles_channel.mention} para asignarte tus roles."
            
            await channel.send(welcome_text, file=file)

    async def on_voice_state_update(self, member, before, after):
        # FEATURE 3: DYNAMIC VOICE CHANNELS
        guild = member.guild
        
        # 1. CREATE CHANNEL
        if after.channel and after.channel.name == "➕ Crear Sala":
            # Target Category
            category = after.channel.category
            
            # Use 'General Gaming' as a template or just create default
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True),
                member: discord.PermissionOverwrite(manage_channels=True, move_members=True)
            }
            
            channel_name = f"Sala de {member.display_name}"
            new_channel = await guild.create_voice_channel(name=channel_name, category=category, overwrites=overwrites)
            
            # Move member
            await member.move_to(new_channel)
            print(f"Created temp channel: {channel_name}")

        # 2. DELETE EMPTY TEMPORARY CHANNEL
        if before.channel and (before.channel.name.startswith("Sala de ") or before.channel.name.startswith("🔊 ")): 
            if len(before.channel.members) == 0:
                await before.channel.delete()
                print(f"Deleted empty temp channel: {before.channel.name}")

    @tasks.loop(minutes=6)
    async def update_stats(self):
        # FEATURE 4: SERVER STATS
        guild = self.get_guild(GUILD_ID)
        if not guild: return

        member_count = guild.member_count
        online_count = sum(1 for m in guild.members if m.status != discord.Status.offline and not m.bot)
        
        category = discord.utils.get(guild.categories, name="📌 INFORMACIÓN")
        if not category: return

        # Stat 1: Miembros
        chan_members = discord.utils.find(lambda c: c.name.startswith("👥 Miembros:"), category.channels)
        if not chan_members:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_members = await guild.create_voice_channel(f"👥 Miembros: {member_count}", category=category, overwrites=overwrites)
        else:
            if chan_members.name != f"👥 Miembros: {member_count}":
                await chan_members.edit(name=f"👥 Miembros: {member_count}")

        # Stat 2: Online
        chan_online = discord.utils.find(lambda c: c.name.startswith("🟢 Online:"), category.channels)
        if not chan_online:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_online = await guild.create_voice_channel(f"🟢 Online: {online_count}", category=category, overwrites=overwrites)
        else:
            if chan_online.name != f"🟢 Online: {online_count}":
                await chan_online.edit(name=f"🟢 Online: {online_count}")
        
        # Stat 3: Voice (Activos)
        voice_count = sum(len(vc.members) for vc in guild.voice_channels)
        chan_voice = discord.utils.find(lambda c: c.name.startswith("🎧 Activos:"), category.channels)
        if not chan_voice:
            overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False)}
            chan_voice = await guild.create_voice_channel(f"🎧 Activos: {voice_count}", category=category, overwrites=overwrites)
        else:
            if chan_voice.name != f"🎧 Activos: {voice_count}":
                await chan_voice.edit(name=f"🎧 Activos: {voice_count}")

    @tasks.loop(minutes=60)
    async def check_temp_roles(self):
        # FEATURE: TEMP ROLES CHECKER
        if not os.path.exists(TEMP_ROLES_FILE):
             return
            
        try:
            with open(TEMP_ROLES_FILE, "r") as f:
                temp_roles = json.load(f)
        except:
            temp_roles = []
            
        guild = self.get_guild(GUILD_ID)
        if not guild: return
        
        now = datetime.now()
        updated_roles = []
        
        for entry in temp_roles:
            expiration = datetime.fromisoformat(entry['expires_at'])
            if now > expiration:
                # Expired: Remove Role
                member = guild.get_member(entry['user_id'])
                if member:
                    role = guild.get_role(entry['role_id'])
                    if role:
                        try:
                             await member.remove_roles(role)
                             print(f"Expired Temp Role: Removed {role.name} from {member.display_name}")
                        except Exception as e:
                             print(f"Error removing role: {e}")
            else:
                updated_roles.append(entry)
        
        # Save updates
        if len(updated_roles) != len(temp_roles):
             with open(TEMP_ROLES_FILE, "w") as f:
                 json.dump(updated_roles, f)

bot = SuperBot()

# --- COMMANDS ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🤖 Comandos de La Villa", color=0x3498db)
    
    embed.add_field(name="🎮 Gaming", value="`!gaming` - Avisa a los Gamers (Solo en #chat-gaming)", inline=False)
    embed.add_field(name="🔊 Voz", value="`!room [nombre]` - Cambia el nombre de tu sala temporal", inline=False)
    embed.add_field(name="🖼️ Utilidad", value="`!avatar @user` - Ver foto de perfil\n`!poll \"Pregunta\" \"Opción1\"...` - Crear encuesta", inline=False)
    
    if ctx.author.guild_permissions.administrator:
        embed.add_field(name="🛡️ Admin", value="`!setup_roles` - Panel\n`!setup_voice` - Voz\n`!clear [n]` - Borrar\n`!tempRole` - Roles temporales\n`!addEmoji` - Añadir Emoji", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title=f"Avatar de {member.display_name}", color=member.color)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Borrados {amount} mensajes.", delete_after=3)

@bot.command()
async def poll(ctx, question, *options):
    if len(options) == 0:
        await ctx.send("❌ Uso: `!poll \"Pregunta\" \"Opcion A\" \"Opcion B\"`")
        return
    if len(options) > 10:
        await ctx.send("❌ Máximo 10 opciones.")
        return

    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    description = []
    for x, option in enumerate(options):
        description.append(f"{reactions[x]} {option}")
    
    embed = discord.Embed(title=f"📊 {question}", description="\n\n".join(description), color=0xffd700)
    embed.set_footer(text=f"Encuesta iniciada por {ctx.author.display_name}")
    
    poll_msg = await ctx.send(embed=embed)
    for i in range(len(options)):
         await poll_msg.add_reaction(reactions[i])

@bot.command()
async def room(ctx, *, new_name):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ Debes estar en un canal de voz.", delete_after=5)
        return

    channel = ctx.author.voice.channel
    permissions = channel.permissions_for(ctx.author)
    if not permissions.manage_channels:
         await ctx.send("❌ No eres el dueño de esta sala.", delete_after=5)
         return
    
    try:
        name_to_set = f"🔊 {new_name}"
        await channel.edit(name=name_to_set)
        await ctx.send(f"✅ Sala renombrada a **{name_to_set}**", delete_after=5)
    except discord.RateLimited:
         await ctx.send("⏳ Discord limita los cambios de nombre (2 veces cada 10 min). Espera un poco.", delete_after=10)
    except Exception as e:
         print(f"Error renaming room: {e}")
         await ctx.send("❌ Error cambiando el nombre.", delete_after=5)

@bot.command()
@commands.has_permissions(administrator=True)
async def tempRole(ctx, role_name: str, members: commands.Greedy[discord.Member], days: int):
    # Search for the role
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ No encuentro el rol: **{role_name}**")
        return

    if not members:
        await ctx.send("❌ Debes mencionar al menos a un usuario. Uso: `!tempRole Admin @User 7`")
        return

    expiration_date = datetime.now() + timedelta(days=days)
    expiration_iso = expiration_date.isoformat()
    
    # Load Existing
    if os.path.exists(TEMP_ROLES_FILE):
        with open(TEMP_ROLES_FILE, "r") as f:
            try:
                temp_data = json.load(f)
            except:
                temp_data = []
    else:
        temp_data = []

    assigned_names = []
    for member in members:
        await member.add_roles(role)
        assigned_names.append(member.display_name)
        
        # Add to tracking
        temp_data.append({
            "user_id": member.id,
            "role_id": role.id,
            "expires_at": expiration_iso
        })

    # Save
    with open(TEMP_ROLES_FILE, "w") as f:
        json.dump(temp_data, f)
        
    await ctx.send(f"✅ Rol **{role.name}** asignado a {', '.join(assigned_names)} por **{days} días** (Hasta: {expiration_date.strftime('%Y-%m-%d')}).")

@bot.command()
@commands.has_permissions(administrator=True)
async def addEmoji(ctx, name: str, url: str = None):
    # Logic: If URL is provided use it, otherwise check for attachment
    image_bytes = None
    
    if ctx.message.attachments:
        url = ctx.message.attachments[0].url
    
    if not url:
        await ctx.send("❌ Debes proporcionar una URL o adjuntar una imagen.")
        return
        
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await ctx.send("❌ No pude descargar la imagen.")
                return
            image_bytes = await resp.read()

    try:
        emoji = await ctx.guild.create_custom_emoji(name=name, image=image_bytes)
        await ctx.send(f"✅ Emoji creado: {emoji}")
    except Exception as e:
        await ctx.send(f"❌ Error al crear emoji: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    embed = discord.Embed(title="🎭 Auto-asignación de Roles", description="Haz click en los botones para obtener tus roles.", color=0x00ff00)
    await ctx.send(embed=embed, view=PersistentRoleView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_voice(ctx):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if category:
        existing = discord.utils.get(category.voice_channels, name="➕ Crear Sala")
        if not existing:
            await category.create_voice_channel("➕ Crear Sala")
            await ctx.send("✅ Canal '➕ Crear Sala' creado.")
        else:
            await ctx.send("El canal ya existe.")
    else:
        await ctx.send("No encuentro la categoría GAMING.")

@bot.command(aliases=["gaming"])
async def Gaming(ctx):
    if ctx.channel.name != "chat-gaming":
        try:
             await ctx.message.delete() 
        except:
             pass 
        await ctx.send("❌ Este comando solo funciona en #chat-gaming.", delete_after=300)
        return

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="🎮 GAMING")
    if not category:
        category = discord.utils.get(guild.categories, name="GAMING")
    
    if not category:
        await ctx.send("❌ No encuentro la categoría GAMING.")
        return

    target_channel = ctx.channel
    role_gamers = discord.utils.get(guild.roles, name="Gamers")
    mention = role_gamers.mention if role_gamers else "@everyone"
    
    await target_channel.send(f"🎮 **Gaming Time** {mention} by {ctx.author.mention}!")

@bot.event
async def on_presence_update(before, after):
    role_gamers = discord.utils.get(after.guild.roles, name="Gamers")
    if role_gamers not in after.roles:
        return

    is_streaming = isinstance(after.activity, discord.Streaming)
    was_streaming = isinstance(before.activity, discord.Streaming)

    if is_streaming and not was_streaming:
        stream_url = after.activity.url
        stream_name = after.activity.name 
        
        category = discord.utils.get(after.guild.categories, name="🎮 GAMING")
        if not category:
             category = discord.utils.get(after.guild.categories, name="GAMING")
        
        target_channel = None
        if category:
            target_channel = discord.utils.get(category.text_channels, name="chat-gaming")
        
        if target_channel:
             await target_channel.send(f"🔴 **¡{after.mention} está en directo!**\n📺 **{stream_name}**\n🔗 {stream_url}")

if __name__ == "__main__":
    bot.run(TOKEN)
