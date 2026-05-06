from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from database import get_prefix
from config import Config
from utils.helpers import get_user_from_event

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}info(?:\\s+(.+))?", outgoing=True))
    async def info_handler(event):
        await event.edit("⏳ **Mengambil info...**")
        
        target_id = None
        target_user = None
        
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            target_id = reply.sender_id
            target_user = reply.sender
        else:
            args = event.pattern_match.group(1)
            if args:
                try:
                    target_user = await client.get_entity(args.strip())
                    target_id = target_user.id
                except:
                    await event.edit(f"❌ User `{args}` tidak ditemukan!")
                    return
            else:
                target_user = await client.get_me()
                target_id = target_user.id
        
        if not target_user:
            await event.edit("❌ User tidak ditemukan!")
            return
        
        try:
            full = await client(GetFullUserRequest(target_id))
            user = full.users[0]
            
            username = f"@{user.username}" if user.username else "Tidak ada"
            name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            premium = "✅ Ya" if getattr(user, 'premium', False) else "❌ Tidak"
            bot = "🤖 Ya" if user.bot else "👤 Tidak"
            verified = "✅ Ya" if getattr(user, 'verified', False) else "❌ Tidak"
            bio = full.full_user.about or "Tidak ada"
            common_chats = full.full_user.common_chats_count or 0
            
            text = (
                f"<blockquote>👤 Info User</blockquote>\n\n"
                f"<b>Nama:</b> {name}\n"
                f"<b>Username:</b> {username}\n"
                f"<b>ID:</b> <code>{user.id}</code>\n"
                f"<b>Bot:</b> {bot}\n"
                f"<b>Premium:</b> {premium}\n"
                f"<b>Verified:</b> {verified}\n"
                f"<b>Bio:</b> {bio}\n"
                f"<b>Grup Bersama:</b> {common_chats}\n"
                f"<b>Link:</b> tg://user?id={user.id}\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            
            await event.edit(text, parse_mode="html")
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}chatinfo", outgoing=True))
    async def chatinfo_handler(event):
        await event.edit("⏳ **Mengambil info grup...**")
        
        try:
            chat = await event.get_chat()
            full = await client(GetFullChannelRequest(event.chat_id))
            
            title = chat.title
            username = f"@{chat.username}" if chat.username else "Private"
            members = full.full_chat.participants_count or 0
            desc = full.full_chat.about or "Tidak ada"
            chat_id = event.chat_id
            
            text = (
                f"<blockquote>💬 Info Grup/Channel</blockquote>\n\n"
                f"<b>Nama:</b> {title}\n"
                f"<b>Username:</b> {username}\n"
                f"<b>ID:</b> <code>{chat_id}</code>\n"
                f"<b>Member:</b> {members:,}\n"
                f"<b>Deskripsi:</b> {desc}\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            
            await event.edit(text, parse_mode="html")
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")