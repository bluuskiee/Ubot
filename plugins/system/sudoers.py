from telethon import events
from database import get_prefix, get_sudoers, add_sudoer, del_sudoer
from config import Config
from utils.helpers import get_user_from_event

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}addsudo", outgoing=True))
    async def addsudo_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            await event.edit("❌ Reply ke user atau masukkan username/ID!")
            return
        
        sudoers = get_sudoers(user_id)
        if target_id in sudoers:
            await event.edit(f"⚠️ User `{target_id}` sudah jadi sudo!")
            return
        
        add_sudoer(user_id, target_id)
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"✅ **{name}** berhasil ditambahkan sebagai sudo user!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}delsudo", outgoing=True))
    async def delsudo_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            await event.edit("❌ Reply ke user atau masukkan username/ID!")
            return
        
        del_sudoer(user_id, target_id)
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"✅ **{name}** berhasil dihapus dari sudo user!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}sudolist", outgoing=True))
    async def sudolist_handler(event):
        sudoers = get_sudoers(user_id)
        
        if not sudoers:
            help_text = (
                f"<blockquote>👥 Bantuan Perintah Sudoers</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Tambah sudo user</b>\n"
                f"        .addsudo (reply/username/id)\n"
                f"    <b>Hapus sudo user</b>\n"
                f"        .delsudo (reply/username/id)\n"
                f"    <b>Liat daftar sudo</b>\n"
                f"        .sudolist\n\n"
                f"📋 Belum ada sudo user.\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        text = f"**👥 Daftar Sudo User:**\n\n"
        for i, sudo_id in enumerate(sudoers, 1):
            try:
                user = await client.get_entity(sudo_id)
                name = user.first_name
                username = f"@{user.username}" if user.username else "Tidak ada"
            except:
                name = "Unknown"
                username = "-"
            text += f"{i}. **{name}** ({username})\n   ID: `{sudo_id}`\n"
        
        await event.edit(text)