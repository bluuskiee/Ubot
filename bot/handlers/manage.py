import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import Config
from database import (
    get_session, set_session, del_session, get_settings,
    reset_prefix, reset_emoji, get_prefix, get_all_emoji
)
from bot.main_bot import app

# States untuk conversation
user_states = {}

@app.on_callback_query(filters.regex("^create_userbot$"))
async def create_userbot(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    session = get_session(user_id)
    
    if session and session.get("active"):
        text = (
            "⚠️ **Kamu sudah punya userbot aktif!**\n\n"
            "Kalau mau buat ulang, reset session dulu."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Reset Session", callback_data="reset_session")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
        ])
        await callback.message.edit(text, reply_markup=keyboard)
        return
    
    text = (
        "**🤖 Buat Userbot Baru**\n\n"
        "Pilih metode login:\n\n"
        "📱 **Phone Number** - Login dengan nomor HP\n"
        "🔑 **Session String** - Masukkan session string langsung\n"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📱 Phone Number", callback_data="login_phone"),
            InlineKeyboardButton("🔑 Session String", callback_data="login_session")
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^login_session$"))
async def login_with_session(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = "waiting_session_string"
    
    text = (
        "**🔑 Masukkan Session String**\n\n"
        "Kirim session string Telethon kamu.\n\n"
        "⚠️ **Jangan bagikan session string ke siapapun!**\n"
        "Ketik /cancel untuk membatalkan."
    )
    await callback.message.edit(text)
    await callback.answer()

@app.on_message(filters.private & filters.text & ~filters.command(["start", "cancel"]))
async def handle_user_input(client: Client, message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    
    if not state:
        return
    
    if state == "waiting_session_string":
        session_string = message.text.strip()
        
        processing = await message.reply("⏳ **Memverifikasi session string...**")
        
        try:
            test_client = TelegramClient(
                StringSession(session_string),
                Config.API_ID,
                Config.API_HASH
            )
            await test_client.connect()
            
            if not await test_client.is_user_authorized():
                await processing.edit("❌ **Session string tidak valid!**")
                await test_client.disconnect()
                del user_states[user_id]
                return
            
            me = await test_client.get_me()
            await test_client.disconnect()
            
            # Save session
            set_session(user_id, {
                "session_string": session_string,
                "active": True,
                "phone": me.phone,
                "username": me.username,
                "name": f"{me.first_name or ''} {me.last_name or ''}".strip(),
                "userbot_id": me.id
            })
            
            del user_states[user_id]
            
            # Start userbot
            from main import start_userbot
            await start_userbot(user_id, session_string)
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
            ])
            
            await processing.edit(
                f"✅ **Userbot berhasil dibuat!**\n\n"
                f"👤 **Nama:** {me.first_name}\n"
                f"📱 **Username:** @{me.username}\n"
                f"🆔 **ID:** `{me.id}`\n\n"
                f"Userbot kamu sudah aktif! Gunakan prefix `.` untuk perintah.",
                reply_markup=keyboard
            )
            
        except Exception as e:
            await processing.edit(f"❌ **Error:** `{str(e)}`")
            del user_states[user_id]

@app.on_callback_query(filters.regex("^reset_prefix$"))
async def reset_prefix_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    session = get_session(user_id)
    
    if not session:
        await callback.answer("❌ Kamu belum punya userbot!", show_alert=True)
        return
    
    text = (
        "**🔄 Reset/Ubah Prefix**\n\n"
        f"Prefix saat ini: `{get_prefix(user_id)}`\n\n"
        "Kirim prefix baru atau pilih opsi:"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Reset ke Default (.)", callback_data="do_reset_prefix"),
        ],
        [InlineKeyboardButton("✏️ Ubah Prefix", callback_data="change_prefix")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^do_reset_prefix$"))
async def do_reset_prefix(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    reset_prefix(user_id)
    await callback.answer("✅ Prefix berhasil direset ke '.'", show_alert=True)
    await reset_prefix_callback(client, callback)

@app.on_callback_query(filters.regex("^reset_session$"))
async def reset_session_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    
    text = (
        "**🔄 Reset Session**\n\n"
        "⚠️ **Peringatan!** Session akan dihapus dan userbot akan berhenti.\n\n"
        "Yakin mau reset?"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ya, Reset", callback_data="do_reset_session"),
            InlineKeyboardButton("❌ Tidak", callback_data="main_menu")
        ]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^do_reset_session$"))
async def do_reset_session(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    
    # Stop userbot if running
    from main import active_clients
    if user_id in active_clients:
        try:
            await active_clients[user_id].disconnect()
            del active_clients[user_id]
        except:
            pass
    
    del_session(user_id)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Buat Userbot Baru", callback_data="create_userbot")],
        [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
    ])
    
    await callback.message.edit(
        "✅ **Session berhasil direset!**\n\nKamu bisa membuat userbot baru sekarang.",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("^reset_emoji$"))
async def reset_emoji_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    
    text = (
        "**🔄 Reset Emoji**\n\n"
        "Ini akan mereset semua emoji ke default.\n\n"
        "Yakin mau reset?"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ya, Reset", callback_data="do_reset_emoji"),
            InlineKeyboardButton("❌ Tidak", callback_data="main_menu")
        ]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^do_reset_emoji$"))
async def do_reset_emoji(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    reset_emoji(user_id)
    await callback.answer("✅ Emoji berhasil direset ke default!", show_alert=True)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
    ])
    await callback.message.edit(
        "✅ **Emoji berhasil direset ke default!**",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("^check_features$"))
async def check_features(client: Client, callback: CallbackQuery):
    from database import is_premium
    user_id = callback.from_user.id
    premium = is_premium(user_id)
    status = "💎 **Premium**" if premium else "🆓 **Gratis**"
    
    free_features = [
        "✅ Alive", "✅ Ping", "✅ Help", "✅ Info",
        "✅ Sticker", "✅ Quote", "✅ QRCode", "✅ Translate",
        "✅ Notes", "✅ Blocked", "✅ Tagall", "✅ Image",
        "✅ Kalkulator", "✅ WebShot", "✅ Convert", "✅ History"
    ]
    
    premium_features = [
        "💎 AutoBC", "💎 Spam", "💎 Clone", "💎 Broadcast",
        "💎 Invite", "💎 Copy", "💎 PMPermit", "💎 VCTools",
        "💎 Download Vid", "💎 Music DL", "💎 Story DL",
        "💎 Global", "💎 Payment", "💎 Sudoers"
    ]
    
    text = (
        f"**📋 Cek Fitur Userbot**\n\n"
        f"Status: {status}\n\n"
        f"**Fitur Gratis:**\n"
        + "\n".join(free_features) +
        f"\n\n**Fitur Premium:**\n"
        + "\n".join(premium_features)
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Upgrade Premium", callback_data="buy_userbot")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)