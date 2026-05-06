import asyncio
from datetime import timedelta
from telethon import events
from telethon.tl.functions.channels import (
    EditBannedRequest, EditAdminRequest, GetParticipantsRequest
)
from telethon.tl.types import (
    ChatBannedRights, ChatAdminRights, ChannelParticipantsSearch
)
from database import get_prefix
from config import Config
from utils.helpers import get_user_from_event

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}kick", outgoing=True))
    async def kick_handler(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya untuk grup!")
            return
        
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau dikick!")
            return
        
        try:
            await client.kick_participant(event.chat_id, target_id)
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"✅ **{name}** berhasil dikick!")
        except Exception as e:
            await event.edit(f"❌ Gagal kick: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}ban", outgoing=True))
    async def ban_handler(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya untuk grup!")
            return
        
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau diban!")
            return
        
        try:
            rights = ChatBannedRights(
                until_date=None,
                view_messages=True
            )
            await client(EditBannedRequest(event.chat_id, target_id, rights))
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"🔨 **{name}** berhasil diban!")
        except Exception as e:
            await event.edit(f"❌ Gagal ban: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unban", outgoing=True))
    async def unban_handler(event):
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau di-unban!")
            return
        
        try:
            rights = ChatBannedRights(until_date=None)
            await client(EditBannedRequest(event.chat_id, target_id, rights))
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"✅ **{name}** berhasil di-unban!")
        except Exception as e:
            await event.edit(f"❌ Gagal unban: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}mute(?:\\s+(.+))?", outgoing=True))
    async def mute_handler(event):
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau dimute!")
            return
        
        args = event.pattern_match.group(1)
        duration = None
        
        if args:
            try:
                # Parse duration (e.g. "1h", "30m", "1d")
                time_str = args.strip().split()[-1]
                if time_str.endswith('h'):
                    duration = timedelta(hours=int(time_str[:-1]))
                elif time_str.endswith('m'):
                    duration = timedelta(minutes=int(time_str[:-1]))
                elif time_str.endswith('d'):
                    duration = timedelta(days=int(time_str[:-1]))
            except:
                pass
        
        try:
            rights = ChatBannedRights(
                until_date=duration,
                send_messages=True
            )
            await client(EditBannedRequest(event.chat_id, target_id, rights))
            name = getattr(target_user, 'first_name', str(target_id))
            duration_text = f" selama {args}" if duration else ""
            await event.edit(f"🔇 **{name}** berhasil dimute{duration_text}!")
        except Exception as e:
            await event.edit(f"❌ Gagal mute: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unmute", outgoing=True))
    async def unmute_handler(event):
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau di-unmute!")
            return
        
        try:
            rights = ChatBannedRights(until_date=None, send_messages=False)
            await client(EditBannedRequest(event.chat_id, target_id, rights))
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"🔊 **{name}** berhasil di-unmute!")
        except Exception as e:
            await event.edit(f"❌ Gagal unmute: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}promote", outgoing=True))
    async def promote_handler(event):
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau dipromote!")
            return
        
        try:
            rights = ChatAdminRights(
                change_info=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                manage_call=True
            )
            await client(EditAdminRequest(event.chat_id, target_id, rights, "Admin"))
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"⭐ **{name}** berhasil dipromote jadi admin!")
        except Exception as e:
            await event.edit(f"❌ Gagal promote: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}demote", outgoing=True))
    async def demote_handler(event):
        target_id, target_user = await get_user_from_event(event)
        if not target_id:
            await event.edit("❌ Reply ke user yang mau didemote!")
            return
        
        try:
            rights = ChatAdminRights()
            await client(EditAdminRequest(event.chat_id, target_id, rights, ""))
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"📉 **{name}** berhasil didemote!")
        except Exception as e:
            await event.edit(f"❌ Gagal demote: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}pin", outgoing=True))
    async def pin_handler(event):
        if not event.reply_to_msg_id:
            await event.edit("❌ Reply ke pesan yang mau dipin!")
            return
        
        try:
            await client.pin_message(event.chat_id, event.reply_to_msg_id)
            await event.edit("📌 **Pesan berhasil dipin!**")
        except Exception as e:
            await event.edit(f"❌ Gagal pin: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}del", outgoing=True))
    async def del_handler(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            await reply.delete()
        await event.delete()
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}purge", outgoing=True))
    async def purge_handler(event):
        if not event.reply_to_msg_id:
            await event.edit("❌ Reply ke pesan awal yang mau dipurge!")
            return
        
        reply = await event.get_reply_message()
        msg_ids = list(range(reply.id, event.id + 1))
        
        await event.client.delete_messages(event.chat_id, msg_ids)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}adminlist", outgoing=True))
    async def adminlist_handler(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya untuk grup!")
            return
        
        await event.edit("⏳ **Mengambil daftar admin...**")
        
        try:
            admins = []
            async for admin in client.iter_participants(event.chat_id, filter=None):
                if hasattr(admin, 'participant') and hasattr(admin.participant, 'admin_rights'):
                    admins.append(admin)
            
            if not admins:
                await event.edit("📋 Tidak ada admin di grup ini.")
                return
            
            text = f"**👑 Daftar Admin ({len(admins)}):**\n\n"
            for i, admin in enumerate(admins, 1):
                username = f"@{admin.username}" if admin.username else "Tidak ada"
                text += f"{i}. **{admin.first_name}** ({username})\n"
            
            await event.edit(text)
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")