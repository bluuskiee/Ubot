from telethon import events
from database import (
    get_prefix, set_emoji, get_all_emoji, 
    reset_emoji, toggle_emoji, is_emoji_enabled
)
from config import Config

VALID_EMOJIS = [
    "ping", "uptime", "profil", "robot", "msg", "warn", 
    "block", "gagal", "sukses", "owner", "klip", "net",
    "up", "down", "speed", "proses", "status"
]

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(
        pattern=f"\\{prefix}setemoji(?:\\s+(.+))?", 
        outgoing=True
    ))
    async def setemoji_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>😊 Bantuan Perintah Emoji</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Atur emoji ping pake perintah ini</b>\n"
                f"        .setemoji ping (emoji)\n"
                f"    <b>Atur emoji uptime pake perintah ini</b>\n"
                f"        .setemoji uptime (emoji)\n"
                f"    <b>Atur emoji profil pake perintah ini</b>\n"
                f"        .setemoji profil (emoji)\n"
                f"    <b>Atur emoji robot pake perintah ini</b>\n"
                f"        .setemoji robot (emoji)\n\n"
                f"    <b>Atur emoji msg pake perintah ini</b>\n"
                f"        .setemoji msg (emoji)\n"
                f"    <b>Atur emoji warn pake perintah ini</b>\n"
                f"        .setemoji warn (emoji)\n"
                f"    <b>Atur emoji block pake perintah ini</b>\n"
                f"        .setemoji block (emoji)\n"
                f"    <b>Atur emoji gagal pake perintah ini</b>\n"
                f"        .setemoji gagal (emoji)\n\n"
                f"    <b>Atur emoji sukses pake perintah ini</b>\n"
                f"        .setemoji sukses (emoji)\n"
                f"    <b>Atur emoji owner pake perintah ini</b>\n"
                f"        .setemoji owner (emoji)\n"
                f"    <b>Atur emoji klip pake perintah ini</b>\n"
                f"        .setemoji klip (emoji)\n"
                f"    <b>Atur emoji net pake perintah ini</b>\n"
                f"        .setemoji net (emoji)\n\n"
                f"    <b>Atur emoji up pake perintah ini</b>\n"
                f"        .setemoji up (emoji)\n"
                f"    <b>Atur emoji down pake perintah ini</b>\n"
                f"        .setemoji down (emoji)\n"
                f"    <b>Atur emoji speed pake perintah ini</b>\n"
                f"        .setemoji speed (emoji)\n"
                f"    <b>Atur emoji proses pake perintah ini</b>\n"
                f"        .setemoji proses (emoji)\n"
                f"    <b>Atur emoji status pake perintah ini</b>\n"
                f"        .setemoji status (emoji)\n\n"
                f"    <b>Dapetin ID emoji atau media</b>\n"
                f"        .id (reply message)\n"
                f"    <b>Liat semua emoji yang udah diatur</b>\n"
                f"        .getemoji\n"
                f"    <b>Nyalain emoji</b>\n"
                f"        .setemoji emoji on\n"
                f"    <b>Matiin emoji</b>\n"
                f"        .setemoji emoji off\n\n\n"
                f"Catatan: Emoji status cuma kerja buat user premium.\n"
                f"   🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split(None, 1)
        if len(parts) < 1:
            await event.edit("❌ Format salah! Gunakan `.setemoji (tipe) (emoji)`")
            return
        
        emoji_type = parts[0].lower()
        
        # Handle on/off
        if emoji_type == "emoji":
            if len(parts) < 2:
                status = is_emoji_enabled(user_id)
                await event.edit(f"Status emoji: {'✅ Aktif' if status else '❌ Nonaktif'}")
                return
            
            action = parts[1].lower()
            if action == "on":
                toggle_emoji(user_id, True)
                await event.edit("✅ **Emoji berhasil diaktifkan!**")
            elif action == "off":
                toggle_emoji(user_id, False)
                await event.edit("❌ **Emoji berhasil dinonaktifkan!**")
            else:
                await event.edit("❌ Gunakan `on` atau `off`!")
            return
        
        if emoji_type not in VALID_EMOJIS:
            await event.edit(
                f"❌ Tipe emoji `{emoji_type}` tidak valid!\n\n"
                f"Tipe yang tersedia:\n`{'`, `'.join(VALID_EMOJIS)}`"
            )
            return
        
        if len(parts) < 2:
            await event.edit(f"❌ Masukkan emoji untuk tipe `{emoji_type}`!")
            return
        
        emoji_value = parts[1].strip()
        set_emoji(user_id, emoji_type, emoji_value)
        await event.edit(f"✅ Emoji **{emoji_type}** berhasil diatur ke: {emoji_value}")
    
    @client.on(events.NewMessage(
        pattern=f"\\{prefix}getemoji", 
        outgoing=True
    ))
    async def getemoji_handler(event):
        emojis = get_all_emoji(user_id)
        emoji_status = "✅ Aktif" if is_emoji_enabled(user_id) else "❌ Nonaktif"
        
        text = f"<b>😊 Daftar Emoji</b>\n"
        text += f"<b>Status: {emoji_status}</b>\n\n"
        
        for emoji_type, emoji_val in emojis.items():
            text += f"<b>{emoji_type}:</b> {emoji_val}\n"
        
        text += f"\n🤖 INI BOT - @{Config.BOT_USERNAME}"
        await event.edit(text, parse_mode="html")
    
    @client.on(events.NewMessage(
        pattern=f"\\{prefix}id", 
        outgoing=True
    ))
    async def id_handler(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            
            if reply.sticker:
                await event.edit(
                    f"<b>🎨 Info Stiker/Emoji</b>\n\n"
                    f"<b>ID:</b> <code>{reply.sticker.id}</code>\n"
                    f"<b>Access Hash:</b> <code>{reply.sticker.access_hash}</code>\n"
                    f"<b>File Unique ID:</b> <code>{reply.sticker.file_unique_id}</code>",
                    parse_mode="html"
                )
            elif reply.photo:
                await event.edit(
                    f"<b>🖼️ Info Foto</b>\n\n"
                    f"<b>ID:</b> <code>{reply.photo.id}</code>\n"
                    f"<b>Access Hash:</b> <code>{reply.photo.access_hash}</code>",
                    parse_mode="html"
                )
            elif reply.sender:
                sender = reply.sender
                await event.edit(
                    f"<b>👤 Info User</b>\n\n"
                    f"<b>ID:</b> <code>{sender.id}</code>\n"
                    f"<b>Nama:</b> {sender.first_name or ''} {sender.last_name or ''}\n"
                    f"<b>Username:</b> @{sender.username or 'Tidak ada'}",
                    parse_mode="html"
                )
        else:
            me = await client.get_me()
            await event.edit(
                f"<b>👤 Info Kamu</b>\n\n"
                f"<b>ID:</b> <code>{me.id}</code>\n"
                f"<b>Nama:</b> {me.first_name or ''} {me.last_name or ''}\n"
                f"<b>Username:</b> @{me.username or 'Tidak ada'}\n"
                f"<b>Phone:</b> <code>{me.phone}</code>",
                parse_mode="html"
            )