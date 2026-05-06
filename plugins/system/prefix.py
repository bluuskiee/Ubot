from telethon import events
from database import get_prefix, set_prefix, reset_prefix
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}prefix(?:\\s+(.+))?", outgoing=True))
    async def prefix_handler(event):
        args = event.pattern_match.group(1)
        current_prefix = get_prefix(user_id)
        
        if not args:
            help_text = (
                f"<blockquote>#️⃣ Bantuan Perintah Prefix</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Liat prefix aktif</b>\n"
                f"        .prefix\n"
                f"    <b>Ganti prefix</b>\n"
                f"        .prefix (prefix_baru)\n"
                f"    <b>Reset prefix ke default (.)</b>\n"
                f"        .resetprefix\n\n"
                f"    <b>Prefix aktif saat ini:</b> <code>{current_prefix}</code>\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        new_prefix = args.strip()
        if len(new_prefix) > 3:
            await event.edit("❌ Prefix maksimal 3 karakter!")
            return
        
        set_prefix(user_id, new_prefix)
        await event.edit(
            f"✅ **Prefix berhasil diubah!**\n\n"
            f"Prefix lama: `{current_prefix}`\n"
            f"Prefix baru: `{new_prefix}`\n\n"
            f"⚠️ Restart userbot untuk menerapkan perubahan."
        )
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}resetprefix", outgoing=True))
    async def resetprefix_handler(event):
        old_prefix = get_prefix(user_id)
        reset_prefix(user_id)
        await event.edit(
            f"✅ **Prefix berhasil direset!**\n\n"
            f"Prefix lama: `{old_prefix}`\n"
            f"Prefix baru: `.`"
        )