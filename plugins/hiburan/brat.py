import os
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from database import get_prefix
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}brat(?:\\s+(.+))?", outgoing=True))
    async def brat_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>😤 Bantuan Perintah Brat</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Generate teks brat</b>\n"
                f"        .brat (teks)\n"
                f"    <b>Generate brat gif</b>\n"
                f"        .bratgif (teks)\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        await event.edit("⏳ **Membuat gambar brat...**")
        
        try:
            # Create brat-style image (white bg, blurry bold text)
            img_width, img_height = 500, 500
            img = Image.new("RGB", (img_width, img_height), color="white")
            draw = ImageDraw.Draw(img)
            
            # Use default font with large size
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Center text
            text = args.lower()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
            
            # Draw blurry effect
            for offset in range(3, 0, -1):
                draw.text((x + offset, y + offset), text, fill=(200, 200, 200), font=font)
            
            draw.text((x, y), text, fill="black", font=font)
            
            # Apply blur effect
            from PIL import ImageFilter
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Draw text again over blur
            draw = ImageDraw.Draw(img)
            draw.text((x, y), text, fill="black", font=font)
            
            img_path = f"/tmp/brat_{user_id}.png"
            img.save(img_path)
            
            await client.send_file(event.chat_id, img_path, caption=f"😤 **{args}**")
            os.remove(img_path)
            await event.delete()
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")