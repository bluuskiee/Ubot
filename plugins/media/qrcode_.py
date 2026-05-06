import os
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from telethon import events
from database import get_prefix
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}qr(?:\\s+(.+))?", outgoing=True))
    async def qr_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>📱 Bantuan Perintah QRCode</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Buat QR Code dari teks/url</b>\n"
                f"        .qr (teks)\n"
                f"    <b>Baca QR Code dari gambar (reply)</b>\n"
                f"        .readqr\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        await event.edit("⏳ **Membuat QR Code...**")
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(args)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_path = f"/tmp/qr_{user_id}.png"
            img.save(img_path)
            
            await client.send_file(
                event.chat_id,
                img_path,
                caption=f"📱 **QR Code**\n\nData: `{args[:50]}{'...' if len(args) > 50 else ''}`"
            )
            
            os.remove(img_path)
            await event.delete()
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}readqr", outgoing=True))
    async def readqr_handler(event):
        if not event.reply_to_msg_id:
            await event.edit("❌ Reply ke gambar QR Code!")
            return
        
        reply = await event.get_reply_message()
        if not reply.photo:
            await event.edit("❌ Reply ke gambar QR Code!")
            return
        
        await event.edit("⏳ **Membaca QR Code...**")
        
        try:
            file_path = await reply.download_media()
            img = Image.open(file_path)
            decoded = decode(img)
            
            os.remove(file_path)
            
            if not decoded:
                await event.edit("❌ Tidak bisa membaca QR Code dari gambar ini!")
                return
            
            result = decoded[0].data.decode("utf-8")
            await event.edit(
                f"✅ **QR Code Berhasil Dibaca!**\n\n"
                f"**Data:**\n`{result}`"
            )
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")