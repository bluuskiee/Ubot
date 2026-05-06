from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import get_user, get_session
from bot.main_bot import app

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🤖 Buat Userbot", callback_data="create_userbot"),
        InlineKeyboardButton("🛒 Beli Userbot", callback_data="buy_userbot")
    ],
    [
        InlineKeyboardButton("⚙️ Kelola Userbot", callback_data="manage_userbot"),
        InlineKeyboardButton("📋 Cek Fitur", callback_data="check_features")
    ],
    [
        InlineKeyboardButton("🔄 Reset Prefix", callback_data="reset_prefix"),
        InlineKeyboardButton("🔄 Reset Session", callback_data="reset_session")
    ],
    [
        InlineKeyboardButton("🔄 Reset Emoji", callback_data="reset_emoji"),
        InlineKeyboardButton("💳 Payment", callback_data="payment_menu")
    ],
    [
        InlineKeyboardButton("❓ Bantuan", callback_data="help_menu"),
        InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")
    ]
])

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    text = (
        f"**Selamat datang di {Config.BOT_NAME}!** 🤖\n\n"
        f"Halo **{user.first_name}**! Aku adalah bot untuk mengelola userbotmu.\n\n"
        f"**Fitur Utama:**\n"
        f"• 🤖 Buat & Kelola Userbot\n"
        f"• ⚙️ Kustomisasi Prefix & Emoji\n"
        f"• 💎 Fitur Premium Tersedia\n"
        f"• 🔒 Database JSON Aman\n"
        f"• 🖥️ {Config.OS_VERSION}\n\n"
        f"**Pilih menu di bawah untuk memulai:**"
    )
    await message.reply(text, reply_markup=MAIN_MENU)

@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_callback(client: Client, callback: CallbackQuery):
    user = callback.from_user
    text = (
        f"**{Config.BOT_NAME}** 🤖\n\n"
        f"Halo **{user.first_name}**! Pilih menu:\n\n"
        f"🖥️ {Config.OS_VERSION}\n"
        f"💾 Database: {Config.DB_TYPE}"
    )
    await callback.message.edit(text, reply_markup=MAIN_MENU)