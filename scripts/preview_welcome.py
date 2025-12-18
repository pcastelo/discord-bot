from easy_pil import Editor, Canvas, Font, load_image_async
import asyncio
import os

async def generate_preview():
    # 1. Background (Dark) - Increased Height to 350
    background = Editor(Canvas((900, 350), color="#23272A"))
    
    # Text Fonts
    poppins = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=30, variant="light")

    # 3. Avatar (Re-positioned to y=80 for vertical center)
    profile = Editor(Canvas((190, 190), color="#5865F2")).circle_image()
    background.paste(profile, (30, 80))
    background.ellipse((30, 80), 190, 190, outline="#00ff00", stroke_width=5)
    
    # Text Elements
    background.text((260, 60), "BIENVENIDO", color="white", font=poppins)
    background.text((260, 120), "User_Preview", color="#00ff00", font=poppins)
    background.text((260, 180), "A LA VILLA", color="white", font=poppins_small)

    # 2. Logo Logic (Below Text)
    logo_path = "assets/villa-castelo.png"
    if os.path.exists(logo_path):
        # Resize to fit nicely below text
        logo = Editor(logo_path).resize((350, 110))
        background.paste(logo, (260, 230)) # Below "A LA VILLA"
        print("Logo pasted at bottom.")
    else:
        print("Logo NOT found.")

    background.save("preview_welcome.png")
    print("Preview saved to preview_welcome.png")

if __name__ == "__main__":
    asyncio.run(generate_preview())
