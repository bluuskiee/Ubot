import platform
import psutil
from datetime import datetime
from telethon import events
from database import get_prefix, get_settings, get_emoji, is_emoji_enabled
from utils.helpers import get_uptime, get_system_info
from config import Config
from utils.emoji_manager import e

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}alive", outgoing=True))
    async def alive_handler(event):
        settings = get_settings(user_id)
        
        robot_emoji = e(user_id, "robot")
        ping_emoji = e(user_id, "ping")
        uptime_emoji = e(user_id, "uptime")
        sukses_emoji = e(user_id, "sukses")
        
        uptime = get_uptime()
        
        # Calculate ping
        start = datetime.now()
        msg = await event.edit(f"{robot_emoji} **Mengecek...**")
        end = datetime.now()
        ping = (end - start).microseconds / 1000
        
        text = (
            f"{robot_emoji} **Userbot Aktif!**\n\n"
            f"{ping_emoji} **Ping:** `{ping:.2f}ms`\n"
            f"{uptime_emoji} **Uptime:** `{uptime}`\n"
            f"{sukses_emoji} **Status:** `Online`\n\n"
            f"**💻 System:**\n"
            f"OS: `{Config.OS_VERSION}`\n"
            f"Python: `{platform.python_version()}`\n"
            f"Database: `{Config.DB_TYPE}`\n\n"
            f"🤖 **Bot:** @{Config.BOT_USERNAME}"
        )
        
        await msg.edit(text)