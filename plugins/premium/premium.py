from telethon import events
from database import (
    get_prefix, is_premium, add_premium, del_premium, 
    list_premium, get_user
)
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    # Owner prefix commands (x prefix for owner)
    owner_prefix = Config.OWNER_PREFIX
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}addpro(?:\\s+(.+))?", outgoing=True))
    async def addpro_handler(event):
        # Only accessible by owner and admins
        if user_id != Config.OWNER_ID and user_id not in Config.ADMINS:
            return
        
        args = event.pattern_match.group(1)
        if not args:
            help_text = (
                f"<blockquote>💎 Bantuan Perintah Premium</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Premium (Owner/Admin Only)</blockquote></b>\n\n"
                f"    <b>Tambah user premium</b>\n"
                f"        .addpro (reply/username/id)\n"
                f"    <b>Hapus user premium</b>\n"
                f"        .delpro (reply/username/id)\n"
                f"    <b>Liat daftar user premium</b>\n"
                f"        .listpro\n\n"
                f"👑 Pemilik: @{Config.OWNER_USERNAME}\n"
                f"👮 Admin: {', '.join(['@' + a for a in Config.ADMIN_USERNAMES])}\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        try:
            if event.reply_to_msg_id:
                reply = await event.get_reply_message()
                target_id = reply.sender_id
                target_user = reply.sender
            else:
                target_user = await client.get_entity(args.strip())
                target_id = target_user.id
            
            add_premium(target_id, user_id)
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"✅ **{name}** berhasil ditambahkan sebagai user premium!")
            
            try:
                await client.send_message(
                    target_id,
                    f"🎉 Selamat! Kamu telah diupgrade ke **Premium** oleh @{Config.OWNER_USERNAME}!\n\n"
                    f"Semua fitur premium sudah bisa kamu gunakan."
                )
            except:
                pass
                
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}delpro(?:\\s+(.+))?", outgoing=True))
    async def delpro_handler(event):
        if user_id != Config.OWNER_ID and user_id not in Config.ADMINS:
            return
        
        args = event.pattern_match.group(1)
        
        try:
            if event.reply_to_msg_id:
                reply = await event.get_reply_message()
                target_id = reply.sender_id
                target_user = reply.sender
            else:
                target_user = await client.get_entity(args.strip())
                target_id = target_user.id
            
            del_premium(target_id)
            name = getattr(target_user, 'first_name', str(target_id))
            await event.edit(f"✅ Premium **{name}** berhasil dihapus!")
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}listpro", outgoing=True))
    async def listpro_handler(event):
        if user_id != Config.OWNER_ID and user_id not in Config.ADMINS:
            return
        
        premium_list = list_premium()
        
        if not premium_list:
            await event.edit("📋 **Belum ada user premium.**")
            return
        
        text = f"**💎 Daftar User Premium ({len(premium_list)}):**\n\n"
        for i, uid in enumerate(premium_list, 1):
            user_data = get_user(int(uid))
            name = user_data.get("name", "Unknown") if user_data else "Unknown"
            text += f"{i}. `{uid}` - {name}\n"
        
        await event.edit(text)
    
    # OWNER GLOBAL COMMAND (x prefix)
    # xaddbl = owner add block all users in group with one command
    @client.on(events.NewMessage(pattern=f"\\{owner_prefix}addbl(?:\\s+(.+))?", outgoing=True))
    async def owner_addbl_handler(event):
        if user_id != Config.OWNER_ID:
            return
        
        args = event.pattern_match.group(1)
        
        await event.edit("⏳ **Memblokir semua user di grup...**")
        
        blocked_count = 0
        async for member in client.iter_participants(event.chat_id):
            if member.bot or member.id == user_id:
                continue
            try:
                from telethon.tl.functions.contacts import BlockRequest
                await client(BlockRequest(id=member.id))
                blocked_count += 1
            except:
                pass
        
        await event.edit(f"✅ **Berhasil memblokir {blocked_count} user di grup ini!**\n\n👑 Perintah Owner")