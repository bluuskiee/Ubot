from telethon import events
from database import get_prefix
from config import Config

HELP_TEXT = """
<blockquote>📚 Bantuan Utama</blockquote>

<b><blockquote expandable>📂 Kategori Plugin</blockquote></b>

<b>1. 💬 Obrolan/Chat</b>
   Admin, Blocked, Chats, Global, Locks, PMPermit, Tagall, VCTools

<b>2. ⬇️ Downloader</b>
   Download Vid, Music DL, Story DL

<b>3. 🎭 Hiburan</b>
   Button, Clone, Fake, Dmute, Cat, Brat, Toxic

<b>4. 🖼️ Media</b>
   Image, Img2Text, Music, QRCode, Quote, Sticker

<b>5. 🔄 Otomatisasi</b>
   AutoBC, AutoRead, Broadcast, Copy, Invite, Spam

<b>6. 💳 Payment</b>
   Saweria, Payment

<b>7. 🔍 Search</b>
   Info, Maps

<b>8. ⚙️ System</b>
   Settings, Spambot, Sudoers, Alive, Bahasa, Emoji, Help, Ignore, Logs, Prefix, Profile

<b>9. 👤 User</b>
   CardInfo, Extras, History, Notes

<b>10. 🛠️ Utility</b>
   Translate, Voice, WebDL, WebShot, Kalkulator, Mail, Convert

🤖 INI BOT - @{bot_username}
"""

CATEGORY_HELP = {
    "obrolan": """
<blockquote>💬 Bantuan Kategori Obrolan/Chat</blockquote>

<b><blockquote expandable>📋 Semua Plugin Obrolan</blockquote></b>

<b>📌 Admin</b>
    <b>Kick member dari grup</b>
        .kick
    <b>Ban member dari grup</b>
        .ban
    <b>Unban member</b>
        .unban
    <b>Mute member</b>
        .mute (waktu)
    <b>Unmute member</b>
        .unmute
    <b>Promote member jadi admin</b>
        .promote
    <b>Demote admin jadi member</b>
        .demote
    <b>Pin pesan</b>
        .pin
    <b>Unpin pesan</b>
        .unpin
    <b>Unpin semua pesan</b>
        .unpinall
    <b>Hapus pesan</b>
        .del
    <b>Hapus semua pesan dari user</b>
        .purge
    <b>Info admin grup</b>
        .adminlist

<b>🚫 Blocked</b>
    <b>Blokir user</b>
        .block
    <b>Buka blokir user</b>
        .unblock
    <b>Buka blokir semua user</b>
        .unblockall
    <b>Liat daftar user yang diblokir</b>
        .blocked

<b>💬 Chats</b>
    <b>Tinggalkan semua grup</b>
        .leaveall
    <b>Tinggalkan grup ini</b>
        .leave
    <b>Liat semua grup/channel</b>
        .chats
    <b>Hapus semua pesan di chat</b>
        .delall
    <b>Arsipkan semua chat</b>
        .archiveall
    <b>Buka arsip semua chat</b>
        .unarchiveall

<b>🌐 Global</b>
    <b>Global ban user di semua grup</b>
        .gban
    <b>Global unban user</b>
        .ungban
    <b>Global mute user di semua grup</b>
        .gmute
    <b>Global unmute user</b>
        .ungmute
    <b>List user yang di gban</b>
        .gbanlist

<b>🔒 Locks</b>
    <b>Kunci tipe pesan tertentu</b>
        .lock (tipe)
    <b>Buka kunci</b>
        .unlock (tipe)
    <b>Liat semua kunci</b>
        .locks
    <b>Tipe lock: msg, media, sticker, gif, url, game, poll, invite</b>

<b>🛡️ PMPermit</b>
    <b>Nyalain PMPermit</b>
        .pmpermit on
    <b>Matiin PMPermit</b>
        .pmpermit off
    <b>Set pesan PMPermit</b>
        .setpmsg (pesan)
    <b>Approve user di PM</b>
        .approve
    <b>Unapprove user di PM</b>
        .unapprove
    <b>Liat daftar approved user</b>
        .approved

<b>👥 Tagall</b>
    <b>Tag semua member grup</b>
        .tagall (pesan)
    <b>Tag semua admin</b>
        .tagadmin (pesan)

<b>🎤 VCTools</b>
    <b>Join voice chat</b>
        .vcjoin
    <b>Leave voice chat</b>
        .vcleave
    <b>Mute di voice chat</b>
        .vcmute
    <b>Unmute di voice chat</b>
        .vcunmute
    <b>Play musik di VC</b>
        .vcplay (judul/url)
    <b>Skip musik</b>
        .vcskip
    <b>Stop musik</b>
        .vcstop

🤖 INI BOT - @{bot_username}
""",

    "blocked": """
<blockquote>🚫 Bantuan Perintah Blocked</blockquote>

<b><blockquote expandable>Perintah Dasar</blockquote></b>

    <b>Blokir user (reply/username/id)</b>
        .block
    <b>Buka blokir user</b>
        .unblock
    <b>Buka blokir semua user</b>
        .unblockall
    <b>Liat daftar user yang diblokir</b>
        .blocked

🤖 INI BOT - @{bot_username}
""",

    "downloader": """
<blockquote>⬇️ Bantuan Kategori Downloader</blockquote>

<b><blockquote expandable>📥 Semua Plugin Download</blockquote></b>

<b>🎬 Download Video</b>
    <b>Download video dari YouTube</b>
        .yt (url)
    <b>Download video dari TikTok</b>
        .tiktok (url)
    <b>Download video dari Instagram</b>
        .igdl (url)
    <b>Download video dari Twitter/X</b>
        .twdl (url)
    <b>Download video dari Facebook</b>
        .fbdl (url)
    <b>Download video dari URL apapun</b>
        .dl (url)
    <b>Download audio saja</b>
        .ytmp3 (url)

<b>🎵 Music Download</b>
    <b>Download musik dari Spotify</b>
        .spotify (judul/url)
    <b>Download musik dari YouTube Music</b>
        .ytmusic (judul/url)
    <b>Download dari SoundCloud</b>
        .sc (url)
    <b>Cari lirik lagu</b>
        .lirik (judul lagu)

<b>📸 Story Download</b>
    <b>Download story Instagram</b>
        .igstory (username)
    <b>Download story TikTok</b>
        .tkstory (username)
    <b>Download story Telegram</b>
        .tstory (reply)

🤖 INI BOT - @{bot_username}
""",

    "hiburan": """
<blockquote>🎭 Bantuan Kategori Hiburan</blockquote>

<b><blockquote expandable>🎮 Semua Plugin Hiburan</blockquote></b>

<b>🔘 Button</b>
    <b>Buat pesan dengan tombol inline</b>
        .button (teks) | (label) | (url)
    <b>Buat multiple button</b>
        .buttons (teks) | (label1:url1) (label2:url2)

<b>👥 Clone</b>
    <b>Clone profil orang lain</b>
        .clone (reply/username)
    <b>Reset profil ke semula</b>
        .unclone

<b>🎭 Fake</b>
    <b>Buat forward palsu</b>
        .fake (nama) : (pesan)
    <b>Buat screenshot palsu</b>
        .fakess (reply)

<b>🔇 Dmute</b>
    <b>Delete dan mute user (reply)</b>
        .dmute
    <b>Unmute dan pulihkan</b>
        .undmute

<b>🐱 Cat</b>
    <b>Kirim foto kucing random</b>
        .cat
    <b>Kirim gif kucing random</b>
        .catgif
    <b>Kirim fakta kucing</b>
        .catfact

<b>😤 Brat</b>
    <b>Generate teks brat</b>
        .brat (teks)
    <b>Generate brat gif</b>
        .bratgif (teks)

<b>☠️ Toxic</b>
    <b>Kirim pesan toxic random</b>
        .toxic
    <b>Rate toxicity pesan (reply)</b>
        .toxicrate

🤖 INI BOT - @{bot_username}
""",

    "media": """
<blockquote>🖼️ Bantuan Kategori Media</blockquote>

<b><blockquote expandable>📁 Semua Plugin Media</blockquote></b>

<b>🖼️ Image</b>
    <b>Cari gambar dari internet</b>
        .img (query)
    <b>Edit gambar (blur)</b>
        .blur (reply)
    <b>Edit gambar (grayscale)</b>
        .grayscale (reply)
    <b>Crop gambar</b>
        .crop (reply)
    <b>Resize gambar</b>
        .resize (width)x(height) (reply)
    <b>Rotate gambar</b>
        .rotate (derajat) (reply)

<b>📝 Img2Text</b>
    <b>Ekstrak teks dari gambar</b>
        .img2text (reply)
    <b>Ekstrak teks dari dokumen</b>
        .ocr (reply)

<b>🎵 Music</b>
    <b>Identifikasi lagu dari audio</b>
        .shazam (reply)
    <b>Konversi audio ke voice note</b>
        .tovoice (reply)
    <b>Konversi voice note ke audio</b>
        .toaudio (reply)

<b>📱 QRCode</b>
    <b>Buat QR Code dari teks/url</b>
        .qr (teks)
    <b>Baca QR Code dari gambar</b>
        .readqr (reply)

<b>💬 Quote</b>
    <b>Buat quote dari pesan (reply)</b>
        .q
    <b>Buat quote dengan style tertentu</b>
        .q (style)

<b>🎨 Sticker</b>
    <b>Konversi gambar/gif ke stiker</b>
        .sticker (reply)
    <b>Konversi stiker ke gambar</b>
        .unsticker (reply)
    <b>Buat stiker dari teks</b>
        .textsticker (teks)
    <b>Tambah stiker ke paket</b>
        .addsticker (reply)
    <b>Buat paket stiker baru</b>
        .newpack (nama paket)
    <b>Hapus stiker dari paket</b>
        .delsticker (reply)

🤖 INI BOT - @{bot_username}
""",

    "otomatisasi": """
<blockquote>🔄 Bantuan Kategori Otomatisasi</blockquote>

<b><blockquote expandable>⚡ Semua Plugin Otomatisasi</blockquote></b>

<b>📢 AutoBC</b>
    <b>Set pesan AutoBC</b>
        .setbc (pesan)
    <b>Nyalain AutoBC dengan interval</b>
        .autobc on (menit)
    <b>Matiin AutoBC</b>
        .autobc off
    <b>Liat status AutoBC</b>
        .autobc status

<b>👁️ AutoRead</b>
    <b>Nyalain baca otomatis semua pesan</b>
        .autoread on
    <b>Matiin baca otomatis</b>
        .autoread off

<b>📣 Broadcast</b>
    <b>Broadcast pesan ke semua grup</b>
        .bc (pesan)
    <b>Broadcast ke semua kontak</b>
        .bcuser (pesan)
    <b>Broadcast dengan reply</b>
        .bc (reply)

<b>📋 Copy</b>
    <b>Copy pesan ke channel/grup lain</b>
        .copy (chat_id)
    <b>Copy forward semua pesan baru</b>
        .autocopy on (source) (dest)
    <b>Matiin autocopy</b>
        .autocopy off

<b>📨 Invite</b>
    <b>Invite semua kontak ke grup</b>
        .inviteall
    <b>Invite dari file/list</b>
        .invite (reply txt)
    <b>Invite user tertentu</b>
        .invite @username

<b>💣 Spam</b>
    <b>Spam pesan</b>
        .spam (jumlah) (pesan)
    <b>Spam stiker (reply)</b>
        .spamsticker (jumlah)
    <b>Hentikan spam</b>
        .stopspam

🤖 INI BOT - @{bot_username}
""",

    "payment": """
<blockquote>💳 Bantuan Kategori Payment</blockquote>

<b><blockquote expandable>💰 Semua Plugin Payment</blockquote></b>

<b>🌊 Saweria</b>
    <b>Cek donasi masuk</b>
        .saweria cek
    <b>Set username Saweria</b>
        .saweria set (username)
    <b>Tampilkan link Saweria</b>
        .saweria link
    <b>Tampilkan QR Saweria</b>
        .saweria qr

<b>💳 Payment</b>
    <b>Cek status pembayaran</b>
        .cekpayment (id)
    <b>Konfirmasi pembayaran</b>
        .konfirm (user_id) (paket)
    <b>List transaksi</b>
        .transaksi
    <b>Set harga paket</b>
        .setharga (paket) (harga)

🤖 INI BOT - @{bot_username}
""",

    "search": """
<blockquote>🔍 Bantuan Kategori Search</blockquote>

<b><blockquote expandable>🔎 Semua Plugin Search</blockquote></b>

<b>ℹ️ Info</b>
    <b>Cek info user (reply/username)</b>
        .info
    <b>Cek info grup</b>
        .chatinfo
    <b>Cek info bot</b>
        .botinfo
    <b>Whois domain/ip</b>
        .whois (domain/ip)
    <b>Cek info nomor HP</b>
        .phoneinfo (nomor)

<b>🗺️ Maps</b>
    <b>Cari lokasi di peta</b>
        .maps (lokasi)
    <b>Cek cuaca di lokasi</b>
        .cuaca (lokasi)
    <b>Cari tempat terdekat</b>
        .nearby (tipe) (lokasi)

🤖 INI BOT - @{bot_username}
""",

    "system": """
<blockquote>⚙️ Bantuan Kategori System</blockquote>

<b><blockquote expandable>🔧 Semua Plugin System</blockquote></b>

<b>⚙️ Settings</b>
    <b>Liat semua pengaturan</b>
        .settings
    <b>Reset semua pengaturan</b>
        .resetsettings

<b>🤖 Spambot</b>
    <b>Report ke @SpamBot</b>
        .spambot

<b>👥 Sudoers</b>
    <b>Tambah sudo user</b>
        .addsudo (reply/username/id)
    <b>Hapus sudo user</b>
        .delsudo (reply/username/id)
    <b>Liat daftar sudo</b>
        .sudolist

<b>💚 Alive</b>
    <b>Cek userbot aktif</b>
        .alive
    <b>Set pesan alive</b>
        .setalive (pesan)

<b>🌐 Bahasa</b>
    <b>Ganti bahasa</b>
        .bahasa (id/en)
    <b>Liat bahasa aktif</b>
        .bahasa

<b>😊 Emoji</b>
    <b>Atur emoji ping</b>
        .setemoji ping (emoji)
    <b>Atur emoji uptime</b>
        .setemoji uptime (emoji)
    <b>Atur emoji profil</b>
        .setemoji profil (emoji)
    <b>Atur emoji robot</b>
        .setemoji robot (emoji)
    <b>Atur emoji msg</b>
        .setemoji msg (emoji)
    <b>Atur emoji warn</b>
        .setemoji warn (emoji)
    <b>Atur emoji block</b>
        .setemoji block (emoji)
    <b>Atur emoji gagal</b>
        .setemoji gagal (emoji)
    <b>Atur emoji sukses</b>
        .setemoji sukses (emoji)
    <b>Atur emoji owner</b>
        .setemoji owner (emoji)
    <b>Atur emoji klip</b>
        .setemoji klip (emoji)
    <b>Atur emoji net</b>
        .setemoji net (emoji)
    <b>Atur emoji up</b>
        .setemoji up (emoji)
    <b>Atur emoji down</b>
        .setemoji down (emoji)
    <b>Atur emoji speed</b>
        .setemoji speed (emoji)
    <b>Atur emoji proses</b>
        .setemoji proses (emoji)
    <b>Atur emoji status</b>
        .setemoji status (emoji)
    <b>Dapetin ID emoji atau media</b>
        .id (reply message)
    <b>Liat semua emoji yang udah diatur</b>
        .getemoji
    <b>Nyalain emoji</b>
        .setemoji emoji on
    <b>Matiin emoji</b>
        .setemoji emoji off
    
Catatan: Emoji status cuma kerja buat user premium.

<b>❓ Help</b>
    <b>Tampilkan bantuan</b>
        .help
    <b>Bantuan per kategori</b>
        .help (kategori)
    <b>Bantuan per plugin</b>
        .help (plugin)

<b>🚫 Ignore</b>
    <b>Abaikan pesan dari user</b>
        .ignore
    <b>Berhenti abaikan user</b>
        .unignore
    <b>Liat list yang diabaikan</b>
        .ignorelist

<b>📋 Logs</b>
    <b>Liat log aktivitas</b>
        .logs
    <b>Bersihkan log</b>
        .clearlogs
    <b>Set chat untuk logs</b>
        .setlogs (chat_id)

<b>#️⃣ Prefix</b>
    <b>Ganti prefix perintah</b>
        .prefix (prefix_baru)
    <b>Reset prefix ke default</b>
        .resetprefix
    <b>Liat prefix aktif</b>
        .prefix

<b>👤 Profile</b>
    <b>Ganti nama profil</b>
        .setname (nama)
    <b>Ganti bio profil</b>
        .setbio (bio)
    <b>Ganti foto profil</b>
        .setpfp (reply foto)
    <b>Hapus foto profil</b>
        .delpfp
    <b>Liat profil sendiri</b>
        .myprofile

🤖 INI BOT - @{bot_username}
""",

    "user": """
<blockquote>👤 Bantuan Kategori User</blockquote>

<b><blockquote expandable>👥 Semua Plugin User</blockquote></b>

<b>💳 CardInfo</b>
    <b>Cek info kartu bank</b>
        .cardinfo (nomor kartu)
    <b>Cek BIN kartu</b>
        .bin (6 digit pertama)

<b>⭐ Extras</b>
    <b>Kirim pesan terjadwal</b>
        .schedule (waktu) (pesan)
    <b>Set reminder</b>
        .remind (waktu) (pesan)
    <b>Liat jadwal pesan</b>
        .schedules
    <b>Hapus jadwal</b>
        .delschedule (id)

<b>📜 History</b>
    <b>Liat history pesan terhapus</b>
        .deleted
    <b>Liat history edit pesan</b>
        .edited
    <b>Bersihkan history</b>
        .clearhistory

<b>📝 Notes</b>
    <b>Simpan catatan</b>
        .save (nama) (isi)
    <b>Ambil catatan</b>
        .get (nama)
    <b>Hapus catatan</b>
        .del (nama)
    <b>Liat semua catatan</b>
        .notes
    <b>Simpan catatan dari reply</b>
        .save (nama) (reply)

🤖 INI BOT - @{bot_username}
""",

    "utility": """
<blockquote>🛠️ Bantuan Kategori Utility</blockquote>

<b><blockquote expandable>⚡ Semua Plugin Utility</blockquote></b>

<b>🌐 Translate</b>
    <b>Terjemahkan pesan (reply)</b>
        .tr (kode bahasa)
    <b>Terjemahkan teks langsung</b>
        .tr (kode bahasa) (teks)
    <b>Deteksi bahasa pesan</b>
        .detect (reply/teks)
    <b>Contoh: .tr en, .tr id, .tr ja</b>

<b>🎤 Voice</b>
    <b>Konversi teks ke suara</b>
        .tts (teks)
    <b>TTS dengan bahasa tertentu</b>
        .tts (id/en) (teks)
    <b>Konversi suara ke teks</b>
        .stt (reply)

<b>🌐 WebDL</b>
    <b>Download konten dari web</b>
        .webdl (url)
    <b>Ambil konten teks dari web</b>
        .scrape (url)

<b>📸 WebShot</b>
    <b>Screenshot halaman web</b>
        .webshot (url)
    <b>Screenshot dengan resolusi tertentu</b>
        .webshot (url) (lebar)x(tinggi)

<b>🔢 Kalkulator</b>
    <b>Hitung ekspresi matematika</b>
        .calc (ekspresi)
    <b>Konversi satuan</b>
        .convert (nilai) (dari) (ke)
    <b>Kalkulator saintifik</b>
        .calcs (ekspresi)

<b>📧 Mail</b>
    <b>Kirim email</b>
        .mail (email) (subjek) | (isi)
    <b>Set akun email pengirim</b>
        .setmail (email) (password)

<b>🔄 Convert</b>
    <b>Konversi file ke format lain</b>
        .convert (format) (reply)
    <b>Konversi gambar ke PDF</b>
        .img2pdf (reply)
    <b>Konversi PDF ke gambar</b>
        .pdf2img (reply)
    <b>Konversi video ke gif</b>
        .vid2gif (reply)
    <b>Konversi gif ke video</b>
        .gif2vid (reply)
    <b>Konversi audio ke format lain</b>
        .audio (format) (reply)
    <b>Konversi suhu (C/F/K)</b>
        .suhu (nilai) (dari) (ke)

🤖 INI BOT - @{bot_username}
""",

    "emoji": """
<blockquote>😊 Bantuan Perintah Emoji</blockquote>

<b><blockquote expandable>Perintah Dasar</blockquote></b>

    <b>Atur emoji ping pake perintah ini</b>
        .setemoji ping (emoji)
    <b>Atur emoji uptime pake perintah ini</b>
        .setemoji uptime (emoji)
    <b>Atur emoji profil pake perintah ini</b>
        .setemoji profil (emoji)
    <b>Atur emoji robot pake perintah ini</b>
        .setemoji robot (emoji)

    <b>Atur emoji msg pake perintah ini</b>
        .setemoji msg (emoji)
    <b>Atur emoji warn pake perintah ini</b>
        .setemoji warn (emoji)
    <b>Atur emoji block pake perintah ini</b>
        .setemoji block (emoji)
    <b>Atur emoji gagal pake perintah ini</b>
        .setemoji gagal (emoji)
    
    <b>Atur emoji sukses pake perintah ini</b>
        .setemoji sukses (emoji)
    <b>Atur emoji owner pake perintah ini</b>
        .setemoji owner (emoji)
    <b>Atur emoji klip pake perintah ini</b>
        .setemoji klip (emoji)
    <b>Atur emoji net pake perintah ini</b>
        .setemoji net (emoji)

    <b>Atur emoji up pake perintah ini</b>
        .setemoji up (emoji)
    <b>Atur emoji down pake perintah ini</b>
        .setemoji down (emoji)
    <b>Atur emoji speed pake perintah ini</b>
        .setemoji speed (emoji)
    <b>Atur emoji proses pake perintah ini</b>
        .setemoji proses (emoji)
    <b>Atur emoji status pake perintah ini</b>
        .setemoji status (emoji)
        
    <b>Dapetin ID emoji atau media</b>
        .id (reply message)
    <b>Liat semua emoji yang udah diatur</b>
        .getemoji
    <b>Nyalain emoji</b>
        .setemoji emoji on
    <b>Matiin emoji</b>
        .setemoji emoji off
    
    
Catatan: Emoji status cuma kerja buat user premium.

🤖 INI BOT - @{bot_username}
"""
}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}help(?:\\s+(.+))?", outgoing=True))
    async def help_handler(event):
        args = event.pattern_match.group(1)
        
        if args:
            args = args.lower().strip()
            if args in CATEGORY_HELP:
                text = CATEGORY_HELP[args].format(bot_username=Config.BOT_USERNAME)
                await event.edit(text, parse_mode="html")
            else:
                await event.edit(f"❌ Kategori `{args}` tidak ditemukan!\n\nKategori tersedia: {', '.join(CATEGORY_HELP.keys())}")
        else:
            text = HELP_TEXT.format(bot_username=Config.BOT_USERNAME)
            await event.edit(text, parse_mode="html")