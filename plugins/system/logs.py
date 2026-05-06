import os
from telethon import events
from database import get_prefix, get_settings, set_settings
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    log_messages = []
    
    @client.on(events.NewMessage(outgoing=True))
    async def log_outgoing(event):
        if event.text:
            log_messages.append({
                "type": "out",
                "chat": event.chat_id,
                "text": event.text[:100],
                "time": str(event.date)
            })
            if len(log_messages) > 100:
                log_messages.pop(0)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}logs", outgoing=True))
    async def logs_handler(event):
        if not log_messages:
            help_text = (
                f"<blockquote>📋 Bantuan Perintah Logs</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Liat log aktivitas</b>\n"
                f"        .logs\n"
                f"    <b>Bersihkan log</b>\n"
                f"        .clearlogs\n"
                f"    <b>Set chat untuk logs</b>\n"
                f"        .setlogs (chat_id)\n\n"
                f"    📋 Belum ada log.\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        text = f"**📋 Log Aktivitas ({len(log_messages)}):**\n\n"
        for i, log in enumerate(log_messages[-10:], 1):
            text += f"{i}. [{log['type'].upper()}] Chat: `{log['chat']}`\n   `{log['text']}`\n\n"
        
        await event.edit(text)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}clearlogs", outgoing=True))
    async def clearlogs_handler(event):
        log_messages.clear()
        await event.edit("✅ **Log berhasil dibersihkan!**")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}setlogs(?:\\s+(.+))?", outgoing=True))
    async def setlogs_handler(event):
        args = event.pattern_match.group(1)
        if not args:
            await event.edit("❌ Masukkan chat ID! Contoh: `.setlogs -100123456789`")
            return
        
        try:
            chat_id = int(args.strip())
            set_settings(user_id, "log_chat", chat_id)
            await event.edit(f"✅ **Log chat berhasil diset ke:** `{chat_id}`")
        except ValueError:
            await event.edit("❌ Chat ID tidak valid!")