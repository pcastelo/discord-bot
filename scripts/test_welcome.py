from easy_pil import Editor, Canvas, Font, load_image_async
import asyncio
import os

async def test_image():
    print("Testing Welcome Image Generation...")
    try:
        # Mock background
        background = Editor(Canvas((900, 270), color="#23272A"))
        
        # Mock profile image (using a placeholder URL for testing)
        # We'll use a standard Discord default avatar for testing
        avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        profile_image = await load_image_async(avatar_url)
        
        profile = Editor(profile_image).resize((190, 190)).circle_image()
        
        # Fonts (EasyPil downloads them automatically usually, or uses defaults)
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=30, variant="light")

        background.paste(profile, (30, 40))
        background.ellipse((30, 40), 190, 190, outline="#00ff00", stroke_width=5)
        background.text((260, 80), "BIENVENIDO", color="white", font=poppins)
        background.text((260, 140), "TestUser", color="#00ff00", font=poppins)
        background.text((260, 200), f"A LA VILLA", color="white", font=poppins_small)

        # Save locally
        output_path = "test_welcome.png"
        background.save(output_path)
        print(f"✅ Image generated successfully: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"❌ Image generation failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_image())
