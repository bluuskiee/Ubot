import asyncio
from telethon import events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from database import get_prefix
from config import Config
from utils.decorators import userbot_cmd

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}tagall(?:\\s+(.+))?", outgoing=True))
    async def tagall_handler(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya untuk grup!")
            return
        
        args = event.pattern_match.group(1) or "📢 Tag All!"
        
        await event.edit("⏳ **Mengambil daftar member...**")
        
        try:
            members = []
            async for member in client.iter_participants(event.chat_id):
                if not member.bot and not member.deleted:
                    members.append(member)
            
            chunk_size = 5
            for i in range(0, len(members), chunk_size):
                chunk = members[i:i + chunk_size]
                mentions = " ".join([f"[​](tg://user?id={m.id})" for m in chunk])
                
                if i == 0:
                    await event.edit(f"{args}\n{mentions}")
                else:
                    await event.respond(f"{mentions}")
                
                await asyncio.sleep(1)
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}tagadmin(?:\\s+(.+))?", outgoing=True))
    async def tagadmin_handler(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya untuk grup!")
            return
        
        args = event.pattern_match.group(1) or "📢 Tag Admin!"
        
        try:
            admins = []
            async for admin in client.iter_participants(event.chat_id, filter=None):
                if hasattr(admin, 'participant'):
                    part = admin.participant
                    if hasattr(part, 'admin_rights') or hasattr(part, 'is_creator'):
                        admins.append(admin)
            
            mentions = " ".join([f"[​](tg://user?id={a.id})" for a in admins])
            await event.edit(f"{args}\n{mentions}")
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")