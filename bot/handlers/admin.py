from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import (
    add_premium, del_premium, list_premium, 
    get_all_users, get_all_sessions, get_user
)
from bot.main_bot import app

def is_admin(user_id: int) -> bool:
    return user_id == Config.OWNER_ID or user_id in Config.ADMINS

@app.on_callback_query(filters.regex("^admin_panel$"))
async def admin_panel(client: Client, callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Kamu bukan admin!", show_alert=True)
        return
    
    users = get_all_users()
    sessions = get_all_sessions()
    premium_users = list_premium()
    
    text = (
        f"**👑 Admin Panel**\n\n"
        f"📊 **Statistik:**\n"
        f"👥 Total User: {len(users)}\n"
        f"🤖 Total Userbot: {len(sessions)}\n"
        f"💎 Premium User: {len(premium_users)}\n\n"
        f"**Kelola sistem dari sini:**"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💎 Tambah Premium", callback_data="admin_addpro"),
            InlineKeyboardButton("🗑️ Hapus Premium", callback_data="admin_delpro")
        ],
        [
            InlineKeyboardButton("📋 List Premium", callback_data="admin_listpro"),
            InlineKeyboardButton("👥 List User", callback_data="admin_listuser")
        ],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
            InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart")
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ])
    await callback.message.edit(text, reply_markup=keyboard)

@app.on_message(filters.command("addpro") & filters.private)
async def add_pro_cmd(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    if len(message.command) < 2:
        await message.reply("**Usage:** `/addpro [user_id]`")
        return
    
    try:
        target_id = int(message.command[1])
        add_premium(target_id, message.from_user.id)
        await message.reply(f"✅ User `{target_id}` berhasil ditambahkan sebagai premium!")
        
        # Notify user
        try:
            await client.send_message(
                target_id,
                f"🎉 **Selamat!** Kamu telah diupgrade ke Premium!\n\n"
                f"Semua fitur premium sudah bisa kamu gunakan.\n"
                f"Hubungi @{Config.OWNER_USERNAME} jika ada pertanyaan."
            )
        except:
            pass
    except ValueError:
        await message.reply("❌ User ID tidak valid!")

@app.on_message(filters.command("delpro") & filters.private)
async def del_pro_cmd(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    if len(message.command) < 2:
        await message.reply("**Usage:** `/delpro [user_id]`")
        return
    
    try:
        target_id = int(message.command[1])
        del_premium(target_id)
        await message.reply(f"✅ Premium user `{target_id}` berhasil dihapus!")
    except ValueError:
        await message.reply("❌ User ID tidak valid!")

@app.on_message(filters.command("listpro") & filters.private)
async def list_pro_cmd(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    premium_list = list_premium()
    if not premium_list:
        await message.reply("📋 **Belum ada user premium.**")
        return
    
    text = "**💎 Daftar User Premium:**\n\n"
    for i, uid in enumerate(premium_list, 1):
        user = get_user(int(uid))
        name = user.get("name", "Unknown") if user else "Unknown"
        text += f"{i}. `{uid}` - {name}\n"
    
    await message.reply(text)