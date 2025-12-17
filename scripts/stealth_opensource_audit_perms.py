import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_GUILD_ID = 1161994306828128346

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Conectado como {client.user}", flush=True)
    guild = client.get_guild(TARGET_GUILD_ID)
    if not guild:
         try: guild = await client.fetch_guild(TARGET_GUILD_ID)
         except: return

    print(f"🎯 Servidor: {guild.name}")
    print("\n--- 🕵️‍♂️ AUDITORÍA DE PERMISOS V2 (Fuzzy) ---")
    
    keywords = ["development", "cloud", "devops", "game", "ai"]
    
    for kw in keywords:
        found = False
        for ch in guild.text_channels:
            if kw in ch.name: # Fuzzy match
                found = True
                print(f"\n📂 Canal: {ch.name} (Cat: {ch.category.name if ch.category else 'N/A'})")
                
                # Check Overwrites
                if not ch.overwrites:
                    print("   ⚠️ Permisos: VACÍO (Público/Heredado)")
                else:
                    print("   👥 Permisos Específicos:")
                    count = 0
                    for target, perm in ch.overwrites.items():
                        if isinstance(target, discord.Role):
                            # Focus on View Channel
                            v = perm.read_messages
                            v_icon = "✅" if v is True else "❌" if v is False else "⬜"
                            if v is False: # Hidden from someone?
                                print(f"      - {target.name}: {v_icon} (Oculto)")
                            elif v is True: # Visible to someone specific?
                                print(f"      - {target.name}: {v_icon} (Visible)")
                            count += 1
                            
                    # Check @everyone
                    everyone = guild.default_role
                    ev_perm = ch.overwrites_for(everyone)
                    ev_view = ev_perm.read_messages
                    ev_icon = "✅" if ev_view is True else "❌" if ev_view is False else "⬜"
                    print(f"      - @everyone: {ev_icon}")
                break
        if not found:
            print(f"❌ No encontré ningún canal con '{kw}'")

    await client.close()

client.run(TOKEN)
