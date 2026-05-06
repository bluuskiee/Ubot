from telethon import events
from database import get_prefix, get_settings, set_settings
from config import Config

LANGUAGES = {
    "id": "🇮🇩 Indonesia",
    "en": "🇺🇸 English",
    "ja": "🇯🇵 Japanese",
    "ko": "🇰🇷 Korean"
}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}bahasa(?:\\s+(.+))?", outgoing=True))
    async def bahasa_handler(event):
        args = event.pattern_match.group(1)
        settings = get_settings(user_id)
        current_lang = settings.get("bahasa", "id")
        
        if not args:
            lang_list = "\n".join([f"    `{code}` - {name}" for code, name in LANGUAGES.items()])
            help_text = (
                f"<blockquote>🌐 Bantuan Perintah Bahasa</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Bahasa aktif: {LANGUAGES.get(current_lang, current_lang)}</b>\n\n"
                f"    <b>Ganti bahasa</b>\n"
                f"        .bahasa (kode)\n\n"
                f"    <b>Bahasa tersedia:</b>\n"
                f"{lang_list}\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        new_lang = args.strip().lower()
        if new_lang not in LANGUAGES:
            await event.edit(
                f"❌ Bahasa `{new_lang}` tidak tersedia!\n\n"
                f"Tersedia: {', '.join(LANGUAGES.keys())}"
            )
            return
        
        set_settings(user_id, "bahasa", new_lang)
        await event.edit(f"✅ **Bahasa berhasil diubah ke {LANGUAGES[new_lang]}!**")