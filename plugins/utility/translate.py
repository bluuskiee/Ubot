from telethon import events
from googletrans import Translator
from database import get_prefix
from config import Config

translator = Translator()

LANG_CODES = {
    "id": "Indonesia", "en": "English", "ja": "Japanese",
    "ko": "Korean", "zh": "Chinese", "ar": "Arabic",
    "fr": "French", "de": "German", "es": "Spanish",
    "pt": "Portuguese", "ru": "Russian", "hi": "Hindi",
    "th": "Thai", "vi": "Vietnamese", "ms": "Malay"
}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}tr(?:\\s+(.+))?", outgoing=True))
    async def translate_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>🌐 Bantuan Perintah Translate</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Terjemahkan pesan (reply)</b>\n"
                f"        .tr (kode bahasa)\n"
                f"    <b>Terjemahkan teks langsung</b>\n"
                f"        .tr (kode bahasa) (teks)\n"
                f"    <b>Deteksi bahasa</b>\n"
                f"        .detect (reply/teks)\n\n"
                f"    <b>Kode Bahasa:</b>\n"
                f"    id=Indonesia, en=English, ja=Japanese\n"
                f"    ko=Korean, zh=Chinese, ar=Arabic\n"
                f"    fr=French, de=German, es=Spanish\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split(None, 1)
        dest_lang = parts[0].lower()
        
        text_to_translate = None
        
        if len(parts) > 1:
            text_to_translate = parts[1]
        elif event.reply_to_msg_id:
            reply = await event.get_reply_message()
            text_to_translate = reply.text
        
        if not text_to_translate:
            await event.edit("❌ Masukkan teks atau reply ke pesan yang mau ditranslate!")
            return
        
        try:
            result = translator.translate(text_to_translate, dest=dest_lang)
            src_lang_name = LANG_CODES.get(result.src, result.src.upper())
            dest_lang_name = LANG_CODES.get(dest_lang, dest_lang.upper())
            
            await event.edit(
                f"🌐 **Terjemahan**\n\n"
                f"**Dari:** {src_lang_name}\n"
                f"**Ke:** {dest_lang_name}\n\n"
                f"**Teks Asli:**\n{text_to_translate}\n\n"
                f"**Terjemahan:**\n{result.text}"
            )
        except Exception as e:
            await event.edit(f"❌ Gagal menerjemahkan: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}detect(?:\\s+(.+))?", outgoing=True))
    async def detect_handler(event):
        args = event.pattern_match.group(1)
        text = None
        
        if args:
            text = args
        elif event.reply_to_msg_id:
            reply = await event.get_reply_message()
            text = reply.text
        
        if not text:
            await event.edit("❌ Masukkan teks atau reply ke pesan!")
            return
        
        try:
            result = translator.detect(text)
            lang_name = LANG_CODES.get(result.lang, result.lang.upper())
            confidence = result.confidence * 100 if result.confidence else 0
            
            await event.edit(
                f"🔍 **Deteksi Bahasa**\n\n"
                f"**Bahasa:** {lang_name} ({result.lang})\n"
                f"**Kepercayaan:** {confidence:.1f}%"
            )
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")