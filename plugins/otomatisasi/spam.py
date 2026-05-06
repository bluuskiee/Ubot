import asyncio
from telethon import events
from database import get_prefix, is_premium
from config import Config

spam_running = {}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}spam(?:\\s+(.+))?", outgoing=True))
    async def spam_handler(event):
        if not is_premium(user_id) and user_id != Config.OWNER_ID:
            await event.edit(
                "❌ **Fitur ini hanya untuk pengguna premium!**\n\n"
                f"Hubungi @{Config.OWNER_USERNAME} untuk membeli premium."
            )
            return
        
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>💣 Bantuan Perintah Spam</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Spam pesan</b>\n"
                f"        .spam (jumlah) (pesan)\n"
                f"    <b>Spam stiker (reply stiker)</b>\n"
                f"        .spamsticker (jumlah)\n"
                f"    <b>Hentikan spam</b>\n"
                f"        .stopspam\n\n"
                f"    ⚠️ <b>Gunakan dengan bijak!</b>\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split(None, 1)
        
        try:
            count = int(parts[0])
        except ValueError:
            await event.edit("❌ Format: `.spam (jumlah) (pesan)`")
            return
        
        if count > 100:
            await event.edit("❌ Maksimal 100 pesan!")
            return
        
        message = parts[1] if len(parts) > 1 else "."
        
        spam_running[user_id] = True
        await event.delete()
        
        for i in range(count):
            if not spam_running.get(user_id):
                break
            await client.send_message(event.chat_id, message)
            await asyncio.sleep(0.5)
        
        spam_running[user_id] = False
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}stopspam", outgoing=True))
    async def stopspam_handler(event):
        spam_running[user_id] = False
        await event.edit("✅ **Spam dihentikan!**")