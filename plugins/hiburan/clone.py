import os
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest
from database import get_prefix
from config import Config
from utils.helpers import get_user_from_event

original_profile = {}

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}clone(?:\\s+(.+))?", outgoing=True))
    async def clone_handler(event):
        if not is_premium_check(user_id):
            await event.edit("❌ **Fitur ini hanya untuk pengguna premium!**")
            return
        
        target_id, target_user = await get_user_from_event(event)
        
        if not target_id:
            help_text = (
                f"<blockquote>👥 Bantuan Perintah Clone</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Clone profil orang lain (reply/username)</b>\n"
                f"        .clone\n"
                f"    <b>Reset profil ke semula</b>\n"
                f"        .unclone\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        await event.edit("⏳ **Mengkloning profil...**")
        
        try:
            # Save original profile
            me = await client.get_me()
            original_profile[user_id] = {
                "first_name": me.first_name or "",
                "last_name": me.last_name or "",
                "bio": ""
            }
            
            # Clone target's profile
            target_name = target_user.first_name or ""
            target_lastname = target_user.last_name or ""
            
            await client(UpdateProfileRequest(
                first_name=target_name,
                last_name=target_lastname
            ))
            
            # Clone photo if available
            try:
                photos = await client.get_profile_photos(target_user.id)
                if photos:
                    photo_path = await client.download_profile_photo(target_user.id)
                    if photo_path:
                        await client.upload_profile_photo(photo_path)
                        os.remove(photo_path)
            except:
                pass
            
            await event.edit(
                f"✅ **Profil berhasil dikloning!**\n\n"
                f"Diklon dari: **{target_name} {target_lastname}**\n\n"
                f"Gunakan `.unclone` untuk reset ke profil asli."
            )
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}unclone", outgoing=True))
    async def unclone_handler(event):
        if user_id not in original_profile:
            await event.edit("❌ Kamu belum mengkloning profil siapapun!")
            return
        
        try:
            orig = original_profile[user_id]
            await client(UpdateProfileRequest(
                first_name=orig["first_name"],
                last_name=orig["last_name"]
            ))
            
            del original_profile[user_id]
            await event.edit("✅ **Profil berhasil direset ke asli!**")
            
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")

def is_premium_check(user_id):
    from database import is_premium
    from config import Config
    return is_premium(user_id) or user_id == Config.OWNER_ID