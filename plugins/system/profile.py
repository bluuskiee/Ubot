import os
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest
from database import get_prefix
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}setname(?:\\s+(.+))?", outgoing=True))
    async def setname_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>👤 Bantuan Perintah Profile</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Ganti nama profil</b>\n"
                f"        .setname (nama)\n"
                f"    <b>Ganti bio profil</b>\n"
                f"        .setbio (bio)\n"
                f"    <b>Ganti foto profil (reply foto)</b>\n"
                f"        .setpfp\n"
                f"    <b>Hapus foto profil</b>\n"
                f"        .delpfp\n"
                f"    <b>Liat profil sendiri</b>\n"
                f"        .myprofile\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        
        try:
            await client(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            await event.edit(f"✅ **Nama berhasil diubah ke:** {args}")
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}setbio(?:\\s+(.+))?", outgoing=True))
    async def setbio_handler(event):
        args = event.pattern_match.group(1)
        bio = args or ""
        
        try:
            await client(UpdateProfileRequest(about=bio))
            if bio:
                await event.edit(f"✅ **Bio berhasil diubah!**\n\nBio baru: {bio}")
            else:
                await event.edit("✅ **Bio berhasil dihapus!**")
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}setpfp", outgoing=True))
    async def setpfp_handler(event):
        if not event.reply_to_msg_id:
            await event.edit("❌ Reply ke foto yang mau dijadikan foto profil!")
            return
        
        reply = await event.get_reply_message()
        if not reply.photo:
            await event.edit("❌ Reply ke foto!")
            return
        
        await event.edit("⏳ **Mengubah foto profil...**")
        
        try:
            file_path = await reply.download_media()
            await client.upload_profile_photo(file_path)
            os.remove(file_path)
            await event.edit("✅ **Foto profil berhasil diubah!**")
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}myprofile", outgoing=True))
    async def myprofile_handler(event):
        me = await client.get_me()
        
        name = f"{me.first_name or ''} {me.last_name or ''}".strip()
        username = f"@{me.username}" if me.username else "Tidak ada"
        premium = "✅ Premium" if getattr(me, 'premium', False) else "❌ Regular"
        
        text = (
            f"<blockquote>👤 Profil Saya</blockquote>\n\n"
            f"<b>Nama:</b> {name}\n"
            f"<b>Username:</b> {username}\n"
            f"<b>ID:</b> <code>{me.id}</code>\n"
            f"<b>Phone:</b> <code>+{me.phone}</code>\n"
            f"<b>Premium:</b> {premium}\n\n"
            f"🤖 INI BOT - @{Config.BOT_USERNAME}"
        )
        
        await event.edit(text, parse_mode="html")