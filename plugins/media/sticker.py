import os
import asyncio
from telethon import events
from telethon.tl.functions.stickers import CreateStickerSetRequest, AddStickerToSetRequest
from telethon.tl.types import InputStickerSetShortName, InputDocument
from database import get_prefix
from config import Config
from PIL import Image

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}sticker", outgoing=True))
    async def sticker_handler(event):
        if not event.reply_to_msg_id:
            help_text = (
                f"<blockquote>🎨 Bantuan Perintah Sticker</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Konversi gambar/gif ke stiker (reply)</b>\n"
                f"        .sticker\n"
                f"    <b>Konversi stiker ke gambar</b>\n"
                f"        .unsticker (reply)\n"
                f"    <b>Buat stiker dari teks</b>\n"
                f"        .textsticker (teks)\n"
                f"    <b>Tambah stiker ke paket</b>\n"
                f"        .addsticker (reply)\n"
                f"    <b>Buat paket stiker baru</b>\n"
                f"        .newpack (nama paket)\n"
                f"    <b>Hapus stiker dari paket</b>\n"
                f"        .delsticker (reply)\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        reply = await event.get_reply_message()
        
        if not reply.media:
            await event.edit("❌ Reply ke gambar atau gif!")
            return
        
        await event.edit("⏳ **Membuat stiker...**")
        
        try:
            file_path = await reply.download_media()
            
            # Convert to webp
            img = Image.open(file_path)
            img = img.resize((512, 512))
            
            sticker_path = file_path.replace(
                os.path.splitext(file_path)[1], ".webp"
            )
            img.save(sticker_path, "WebP")
            
            # Send as sticker
            await client.send_file(
                event.chat_id,
                sticker_path,
                force_document=False,
                reply_to=event.reply_to_msg_id
            )
            
            os.remove(file_path)
            os.remove(sticker_path)
            
            await event.delete()
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unsticker", outgoing=True))
    async def unsticker_handler(event):
        if not event.reply_to_msg_id:
            await event.edit("❌ Reply ke stiker!")
            return
        
        reply = await event.get_reply_message()
        
        if not reply.sticker:
            await event.edit("❌ Reply ke stiker!")
            return
        
        await event.edit("⏳ **Mengkonversi stiker ke gambar...**")
        
        try:
            file_path = await reply.download_media()
            
            img = Image.open(file_path)
            png_path = file_path.replace(".webp", ".png")
            img.save(png_path, "PNG")
            
            await client.send_file(event.chat_id, png_path)
            
            os.remove(file_path)
            os.remove(png_path)
            
            await event.delete()
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")