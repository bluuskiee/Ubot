from telethon import events
from database import get_prefix, get_settings, set_settings
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}settings", outgoing=True))
    async def settings_handler(event):
        settings = get_settings(user_id)
        
        alive_status = "✅ Aktif" if settings.get("alive") else "❌ Nonaktif"
        autoread_status = "✅ Aktif" if settings.get("autoread") else "❌ Nonaktif"
        pmpermit_status = "✅ Aktif" if settings.get("pmpermit") else "❌ Nonaktif"
        emoji_status = "✅ Aktif" if settings.get("emoji_status", True) else "❌ Nonaktif"
        
        text = (
            f"<blockquote>⚙️ Pengaturan Userbot</blockquote>\n\n"
            f"<b><blockquote expandable>Semua Pengaturan</blockquote></b>\n\n"
            f"    <b>Prefix:</b> <code>{settings.get('prefix', '.')}</code>\n"
            f"    <b>Bahasa:</b> <code>{settings.get('bahasa', 'id').upper()}</code>\n"
            f"    <b>Alive:</b> {alive_status}\n"
            f"    <b>AutoRead:</b> {autoread_status}\n"
            f"    <b>PMPermit:</b> {pmpermit_status}\n"
            f"    <b>Emoji:</b> {emoji_status}\n\n"
            f"    <b>Ganti pengaturan dengan perintah:</b>\n"
            f"        .prefix (prefix_baru)\n"
            f"        .bahasa (id/en)\n"
            f"        .setemoji emoji (on/off)\n"
            f"        .pmpermit (on/off)\n"
            f"        .autoread (on/off)\n\n"
            f"🤖 INI BOT - @{Config.BOT_USERNAME}"
        )
        await event.edit(text, parse_mode="html")