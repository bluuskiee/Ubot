from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import get_user, set_user, add_premium
from bot.main_bot import app

PACKAGES = {
    "basic": {
        "name": "Basic",
        "price": 15000,
        "duration": 30,
        "features": ["Semua fitur gratis", "AutoBC", "PMPermit"]
    },
    "premium": {
        "name": "Premium", 
        "price": 25000,
        "duration": 30,
        "features": ["Semua fitur Basic", "Spam", "Clone", "Broadcast", "VCTools"]
    },
    "vip": {
        "name": "VIP",
        "price": 50000,
        "duration": 30,
        "features": ["Semua fitur Premium", "Download Vid", "Music DL", "Story DL", "Invite", "Copy", "Global"]
    }
}

@app.on_callback_query(filters.regex("^buy_userbot$"))
async def buy_menu(client: Client, callback: CallbackQuery):
    text = (
        "**🛒 Beli/Upgrade Userbot**\n\n"
        "Pilih paket yang sesuai:\n\n"
        "🟢 **Basic** - Rp 15.000/bulan\n"
        "└ AutoBC, PMPermit + Fitur Gratis\n\n"
        "🔵 **Premium** - Rp 25.000/bulan\n"
        "└ Spam, Clone, Broadcast, VCTools\n\n"
        "💎 **VIP** - Rp 50.000/bulan\n"
        "└ Semua Fitur Tanpa Batas\n\n"
        "**Metode Pembayaran:** Saweria, QRIS, Transfer Bank"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Basic", callback_data="buy_basic"),
            InlineKeyboardButton("🔵 Premium", callback_data="buy_premium"),
            InlineKeyboardButton("💎 VIP", callback_data="buy_vip")
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^buy_(basic|premium|vip)$"))
async def buy_package(client: Client, callback: CallbackQuery):
    package_name = callback.data.split("_")[1]
    package = PACKAGES.get(package_name)
    
    features_text = "\n".join([f"✅ {f}" for f in package["features"]])
    
    text = (
        f"**💳 Pembelian Paket {package['name']}**\n\n"
        f"**Harga:** Rp {package['price']:,}/bulan\n"
        f"**Durasi:** {package['duration']} hari\n\n"
        f"**Fitur:**\n{features_text}\n\n"
        f"**Cara Pembayaran:**\n"
        f"1. Klik tombol Saweria/QRIS di bawah\n"
        f"2. Lakukan pembayaran\n"
        f"3. Screenshot bukti pembayaran\n"
        f"4. Kirim ke @{Config.OWNER_USERNAME}\n"
        f"5. Tunggu konfirmasi (maks 1x24 jam)\n\n"
        f"⚠️ **Hubungi admin jika ada masalah**"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 Saweria", url=f"https://saweria.co/{Config.OWNER_USERNAME}"),
            InlineKeyboardButton("📱 Hubungi Admin", url=f"https://t.me/{Config.OWNER_USERNAME}")
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="buy_userbot")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)