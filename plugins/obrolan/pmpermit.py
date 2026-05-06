import asyncio
from telethon import events
from database import get_prefix, get_pmpermit, set_pmpermit
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    # Auto handler for PM
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def pm_handler(event):
        pmpermit = get_pmpermit(user_id)
        
        if not pmpermit.get("enabled"):
            return
        
        sender_id = event.sender_id
        approved = pmpermit.get("approved", [])
        
        if sender_id in approved:
            return
        
        # Check if it's official telegram
        if sender_id in [777000, 1087968824]:
            return
        
        message = pmpermit.get("message", "Halo! Pesan kamu sedang ditinjau oleh pemilik.")
        
        warned = pmpermit.get("warned", {})
        warn_count = warned.get(str(sender_id), 0)
        
        if warn_count == 0:
            await event.reply(
                f"⚠️ **{message}**\n\n"
                f"Jika kamu mengirim pesan lagi, kamu akan diblokir!"
            )
            warned[str(sender_id)] = 1
            pmpermit["warned"] = warned
            set_pmpermit(user_id, pmpermit)
        elif warn_count >= 2:
            from telethon.tl.functions.contacts import BlockRequest
            await client(BlockRequest(id=sender_id))
            await event.reply("🚫 Kamu telah diblokir!")
        else:
            warned[str(sender_id)] = warn_count + 1
            pmpermit["warned"] = warned
            set_pmpermit(user_id, pmpermit)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}pmpermit(?:\\s+(.+))?", outgoing=True))
    async def pmpermit_handler(event):
        args = event.pattern_match.group(1)
        pmpermit = get_pmpermit(user_id)
        
        if not args:
            status = "✅ Aktif" if pmpermit.get("enabled") else "❌ Nonaktif"
            help_text = (
                f"<blockquote>🛡️ Bantuan Perintah PMPermit</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Status PMPermit:</b> {status}\n\n"
                f"    <b>Nyalain PMPermit</b>\n"
                f"        .pmpermit on\n"
                f"    <b>Matiin PMPermit</b>\n"
                f"        .pmpermit off\n"
                f"    <b>Set pesan PMPermit</b>\n"
                f"        .setpmsg (pesan)\n"
                f"    <b>Approve user di PM</b>\n"
                f"        .approve\n"
                f"    <b>Unapprove user di PM</b>\n"
                f"        .unapprove\n"
                f"    <b>Liat daftar approved user</b>\n"
                f"        .approved\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        if args.lower() == "on":
            pmpermit["enabled"] = True
            set_pmpermit(user_id, pmpermit)
            await event.edit("✅ **PMPermit berhasil diaktifkan!**")
        elif args.lower() == "off":
            pmpermit["enabled"] = False
            set_pmpermit(user_id, pmpermit)
            await event.edit("❌ **PMPermit berhasil dinonaktifkan!**")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}approve", outgoing=True))
    async def approve_handler(event):
        if not event.is_private:
            await event.edit("❌ Perintah ini hanya di PM!")
            return
        
        chat = await event.get_chat()
        pmpermit = get_pmpermit(user_id)
        approved = pmpermit.get("approved", [])
        
        if chat.id not in approved:
            approved.append(chat.id)
            pmpermit["approved"] = approved
            set_pmpermit(user_id, pmpermit)
        
        await event.edit(f"✅ **{chat.first_name}** berhasil di-approve!")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unapprove", outgoing=True))
    async def unapprove_handler(event):
        if not event.is_private:
            await event.edit("❌ Perintah ini hanya di PM!")
            return
        
        chat = await event.get_chat()
        pmpermit = get_pmpermit(user_id)
        approved = pmpermit.get("approved", [])
        
        if chat.id in approved:
            approved.remove(chat.id)
            pmpermit["approved"] = approved
            set_pmpermit(user_id, pmpermit)
        
        await event.edit(f"✅ **{chat.first_name}** berhasil di-unapprove!")