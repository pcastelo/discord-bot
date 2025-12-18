from easy_pil import Editor, Canvas, Font, load_image_async
import asyncio
def get_ordinal(n):
    if 11 <= (n % 100) <= 13: suffix = 'th'
    else: suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

async def generate_preview():
    # 1. Background (Dark) - Maintain 350 height for spacing OR revert to 250 if compact?
    # The reference image is compact. Let's try 300.
    background = Editor(Canvas((900, 300), color="#23272A"))
    
    # Text Fonts
    poppins = Font.poppins(size=50, variant="bold")
    poppins_med = Font.poppins(size=40, variant="bold")
    poppins_small = Font.poppins(size=30, variant="light")

    # 2. Avatar (Left side, big)
    # Centered vertically in 300px is y=150. Radius 95 (190 size).
    profile = Editor(Canvas((190, 190), color="#5865F2")).circle_image()
    background.paste(profile, (30, 55)) # y=55 to center in 300 (300-190=110/2=55)
    background.ellipse((30, 55), 190, 190, outline="#00ff00", stroke_width=5)
    
    # 3. Text Elements
    # Mock Data
    member_name = "Villero#3399"
    guild_name = "La Villa"
    ordinal = get_ordinal(216)
    
    # Layout: Right of avatar (starts approx x=250)
    background.text((250, 60), f"Welcome {member_name}", color="white", font=poppins)
    background.text((250, 120), f"to {guild_name}", color="#FF0000", font=poppins_med)
    background.text((250, 180), f"you are the {ordinal} user", color="white", font=poppins_small)

    background.save("preview_welcome.png")
    print("Preview saved to preview_welcome.png")

if __name__ == "__main__":
    asyncio.run(generate_preview())
