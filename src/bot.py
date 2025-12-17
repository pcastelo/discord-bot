import os
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv
from easy_pil import Editor, Canvas, Font, load_image_async
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.presences = True

class PersistentRoleView(View):
    def __init__(self):
        super().__init__(timeout=None) # Persistent

    @discord.ui.button(label="🎮 Gamers", style=discord.ButtonStyle.primary, custom_id="role_gamers", emoji="🎮")
    async def gamer_button(self, interaction: discord.Interaction, button: Button):
        role = discord.utils.get(interaction.guild.roles, name="Gamers")
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("❌ Rol **Gamers** eliminado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Rol **Gamers** añadido.", ephemeral=True)

    @discord.ui.button(label="📚 Estudio", style=discord.ButtonStyle.success, custom_id="role_estudio", emoji="📚")
    async def estudio_button(self, interaction: discord.Interaction, button: Button):
        role = discord.utils.get(interaction.guild.roles, name="Estudio")
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("❌ Rol **Estudio** eliminado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Rol **Estudio** añadido.", ephemeral=True)

    @discord.ui.button(label="👋 Invitados", style=discord.ButtonStyle.secondary, custom_id="role_invitados", emoji="👋")
    async def invitados_button(self, interaction: discord.Interaction, button: Button):
        role = discord.utils.get(interaction.guild.roles, name="Invitados")
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("❌ Rol **Invitados** eliminado.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Rol **Invitados** añadido.", ephemeral=True)

class SuperBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.persistent_views_added = False

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        if not self.persistent_views_added:
            self.add_view(PersistentRoleView())
            self.persistent_views_added = True
        
        # Start Stats Loop
        if not self.update_stats.is_running():
            self.update_stats.start()
        
        # Start Voice Cleanup Loop
        print("Bot is Ready!")

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
        # We need a way to identify if it is temporary. 
        # Strategy: Checks if channel starts with "Sala de" and is empty.
        if before.channel and before.channel.name.startswith("Sala de "):
            if len(before.channel.members) == 0:
                await before.channel.delete()
                print(f"Deleted empty temp channel: {before.channel.name}")

    @tasks.loop(minutes=10)
    async def update_stats(self):
        # FEATURE 4: SERVER STATS
        guild = self.get_guild(GUILD_ID)
        if not guild: return

        member_count = guild.member_count
        online_count = sum(1 for m in guild.members if m.status != discord.Status.offline and not m.bot)

        # Look for channels or create them
        # We look for a Locked Voice Channel
        
        # Helper to find or create
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

bot = SuperBot()

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    # FEATURE 2: AUTO ROLES SETUP COMMAND
    embed = discord.Embed(title="🎭 Auto-asignación de Roles", description="Haz click en los botones para obtener tus roles.", color=0x00ff00)
    await ctx.send(embed=embed, view=PersistentRoleView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_voice(ctx):
    # Helper to create the trigger channel if missing
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

if __name__ == "__main__":
    bot.run(TOKEN)
