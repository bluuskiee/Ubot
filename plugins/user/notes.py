from telethon import events
from database import get_prefix, get_notes, set_note, del_note
from config import Config

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}save(?:\\s+(.+))?", outgoing=True))
    async def save_note_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>📝 Bantuan Perintah Notes</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Simpan catatan</b>\n"
                f"        .save (nama) (isi)\n"
                f"    <b>Simpan dari reply</b>\n"
                f"        .save (nama) (reply)\n"
                f"    <b>Ambil catatan</b>\n"
                f"        .get (nama)\n"
                f"    <b>Hapus catatan</b>\n"
                f"        .delnote (nama)\n"
                f"    <b>Liat semua catatan</b>\n"
                f"        .notes\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split(None, 1)
        note_name = parts[0].lower()
        
        if len(parts) > 1:
            note_content = parts[1]
        elif event.reply_to_msg_id:
            reply = await event.get_reply_message()
            note_content = reply.text or ""
        else:
            await event.edit("❌ Masukkan isi catatan atau reply ke pesan!")
            return
        
        set_note(user_id, note_name, note_content)
        await event.edit(f"✅ **Catatan `{note_name}` berhasil disimpan!**")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}get(?:\\s+(.+))?", outgoing=True))
    async def get_note_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            await event.edit("❌ Masukkan nama catatan! Contoh: `.get nama`")
            return
        
        note_name = args.strip().lower()
        notes = get_notes(user_id)
        
        if note_name not in notes:
            await event.edit(f"❌ Catatan `{note_name}` tidak ditemukan!")
            return
        
        await event.edit(
            f"📝 **Catatan: {note_name}**\n\n"
            f"{notes[note_name]}"
        )
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}delnote(?:\\s+(.+))?", outgoing=True))
    async def del_note_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            await event.edit("❌ Masukkan nama catatan yang mau dihapus!")
            return
        
        note_name = args.strip().lower()
        del_note(user_id, note_name)
        await event.edit(f"✅ **Catatan `{note_name}` berhasil dihapus!**")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}notes", outgoing=True))
    async def notes_list_handler(event):
        notes = get_notes(user_id)
        
        if not notes:
            await event.edit(
                f"<blockquote>📝 Bantuan Perintah Notes</blockquote>\n\n"
                f"<b>Belum ada catatan tersimpan.</b>\n\n"
                f"    <b>Simpan catatan dengan</b>\n"
                f"        .save (nama) (isi)\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            return
        
        text = f"**📝 Daftar Catatan ({len(notes)}):**\n\n"
        for i, (name, content) in enumerate(notes.items(), 1):
            preview = content[:50] + "..." if len(content) > 50 else content
            text += f"{i}. **{name}**\n   `{preview}`\n\n"
        
        text += f"Gunakan `.get (nama)` untuk melihat catatan."
        await event.edit(text)