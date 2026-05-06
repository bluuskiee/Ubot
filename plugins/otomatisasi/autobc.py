import asyncio
from telethon import events
from database import get_prefix, get_autobc, set_autobc, del_autobc, is_premium
from config import Config

autobc_tasks = {}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    # Restore autobc if was running
    autobc_data = get_autobc(user_id)
    if autobc_data.get("running"):
        asyncio.create_task(run_autobc(client, user_id))
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}setbc(?:\\s+(.+))?", outgoing=True))
    async def setbc_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            await event.edit(
                f"<blockquote>📢 Bantuan Perintah AutoBC</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Set pesan AutoBC</b>\n"
                f"        .setbc (pesan)\n"
                f"    <b>Nyalain AutoBC dengan interval</b>\n"
                f"        .autobc on (menit)\n"
                f"    <b>Matiin AutoBC</b>\n"
                f"        .autobc off\n"
                f"    <b>Liat status AutoBC</b>\n"
                f"        .autobc status\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            return
        
        autobc_data = get_autobc(user_id) or {}
        autobc_data["message"] = args
        set_autobc(user_id, autobc_data)
        
        await event.edit(f"✅ **Pesan AutoBC berhasil diset!**\n\nPesan: {args}")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}autobc(?:\\s+(.+))?", outgoing=True))
    async def autobc_handler(event):
        if not is_premium(user_id) and user_id != Config.OWNER_ID:
            await event.edit("❌ **Fitur ini hanya untuk pengguna premium!**")
            return
        
        args = event.pattern_match.group(1)
        
        if not args:
            autobc_data = get_autobc(user_id) or {}
            status = "✅ Berjalan" if autobc_data.get("running") else "❌ Berhenti"
            await event.edit(
                f"**📢 Status AutoBC:**\n"
                f"Status: {status}\n"
                f"Interval: {autobc_data.get('interval', '-')} menit\n"
                f"Pesan: {autobc_data.get('message', 'Belum diset')}"
            )
            return
        
        parts = args.split(None, 1)
        action = parts[0].lower()
        
        if action == "on":
            autobc_data = get_autobc(user_id) or {}
            if not autobc_data.get("message"):
                await event.edit("❌ Set pesan dulu dengan `.setbc (pesan)`!")
                return
            
            interval = 60
            if len(parts) > 1:
                try:
                    interval = int(parts[1])
                except:
                    pass
            
            autobc_data["running"] = True
            autobc_data["interval"] = interval
            set_autobc(user_id, autobc_data)
            
            if user_id in autobc_tasks:
                autobc_tasks[user_id].cancel()
            
            autobc_tasks[user_id] = asyncio.create_task(run_autobc(client, user_id))
            await event.edit(f"✅ **AutoBC berhasil diaktifkan!**\nInterval: {interval} menit")
        
        elif action == "off":
            autobc_data = get_autobc(user_id) or {}
            autobc_data["running"] = False
            set_autobc(user_id, autobc_data)
            
            if user_id in autobc_tasks:
                autobc_tasks[user_id].cancel()
                del autobc_tasks[user_id]
            
            await event.edit("❌ **AutoBC berhasil dimatikan!**")
        
        elif action == "status":
            autobc_data = get_autobc(user_id) or {}
            status = "✅ Berjalan" if autobc_data.get("running") else "❌ Berhenti"
            await event.edit(
                f"**📢 Status AutoBC:**\n"
                f"Status: {status}\n"
                f"Interval: {autobc_data.get('interval', '-')} menit\n"
                f"Pesan: {autobc_data.get('message', 'Belum diset')}"
            )

async def run_autobc(client, user_id: int):
    while True:
        autobc_data = get_autobc(user_id)
        if not autobc_data or not autobc_data.get("running"):
            break
        
        message = autobc_data.get("message")
        interval = autobc_data.get("interval", 60)
        
        if message:
            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    try:
                        await client.send_message(dialog.id, message)
                        await asyncio.sleep(2)
                    except:
                        pass
        
        await asyncio.sleep(interval * 60)