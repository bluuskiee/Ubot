from telethon import events
from database import get_prefix, get_ignored, add_ignore, del_ignore
from config import Config
from utils.helpers import get_user_from_event

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    # Auto ignore handler
    @client.on(events.NewMessage(incoming=True))
    async def auto_ignore(event):
        ignored = get_ignored(user_id)
        if event.sender_id in ignored:
            raise events.StopPropagation
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}ignore", outgoing=True))
    async def ignore_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            help_text = (
                f"<blockquote>🚫 Bantuan Perintah Ignore</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Abaikan pesan dari user (reply)</b>\n"
                f"        .ignore\n"
                f"    <b>Berhenti abaikan user</b>\n"
                f"        .unignore\n"
                f"    <b>Liat list yang diabaikan</b>\n"
                f"        .ignorelist\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        add_ignore(user_id, target_id)
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"✅ **{name}** berhasil diabaikan!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unignore", outgoing=True))
    async def unignore_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            await event.edit("❌ Reply ke user yang mau di-unignore!")
            return
        
        del_ignore(user_id, target_id)
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"✅ **{name}** sudah tidak diabaikan!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}ignorelist", outgoing=True))
    async def ignorelist_handler(event):
        ignored = get_ignored(user_id)
        
        if not ignored:
            await event.edit("📋 **Daftar ignore kosong.**")
            return
        
        text = f"**🚫 Daftar Ignored User ({len(ignored)}):**\n\n"
        for i, ig_id in enumerate(ignored, 1):
            try:
                user = await client.get_entity(ig_id)
                name = user.first_name
            except:
                name = "Unknown"
            text += f"{i}. **{name}** (`{ig_id}`)\n"
        
        await event.edit(text)