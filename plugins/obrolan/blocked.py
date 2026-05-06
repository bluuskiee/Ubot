from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest, GetBlockedRequest
from database import get_prefix
from config import Config
from utils.helpers import get_user_from_event

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}block", outgoing=True))
    async def block_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            help_text = (
                f"<blockquote>🚫 Bantuan Perintah Blocked</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Blokir user (reply ke pesan user)</b>\n"
                f"        .block\n"
                f"    <b>Buka blokir user</b>\n"
                f"        .unblock\n"
                f"    <b>Buka blokir semua user</b>\n"
                f"        .unblockall\n"
                f"    <b>Liat daftar user yang diblokir</b>\n"
                f"        .blocked\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        await client(BlockRequest(id=target_id))
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"🚫 **{name}** berhasil diblokir!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unblock", outgoing=True))
    async def unblock_handler(event):
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            await event.edit("❌ Reply ke user yang mau dibuka blokirnya!")
            return
        
        await client(UnblockRequest(id=target_id))
        name = getattr(target_user, 'first_name', str(target_id)) if target_user else str(target_id)
        await event.edit(f"✅ **{name}** berhasil dibuka blokirnya!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unblockall", outgoing=True))
    async def unblockall_handler(event):
        await event.edit("⏳ **Membuka blokir semua user...**")
        
        blocked = await client(GetBlockedRequest(offset=0, limit=100))
        count = 0
        
        for user in blocked.users:
            try:
                await client(UnblockRequest(id=user.id))
                count += 1
            except:
                pass
        
        await event.edit(f"✅ Berhasil membuka blokir **{count}** user!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}blocked", outgoing=True))
    async def blocked_list_handler(event):
        await event.edit("⏳ **Mengambil daftar blocked...**")
        
        blocked = await client(GetBlockedRequest(offset=0, limit=100))
        
        if not blocked.users:
            await event.edit("📋 Tidak ada user yang diblokir.")
            return
        
        text = f"**🚫 Daftar User Terblokir ({len(blocked.users)}):**\n\n"
        for i, user in enumerate(blocked.users, 1):
            username = f"@{user.username}" if user.username else "Tidak ada"
            text += f"{i}. **{user.first_name}** ({username})\n   ID: `{user.id}`\n"
        
        await event.edit(text)