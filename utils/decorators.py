import functools
from telethon import events
from database import get_prefix, get_settings, get_ignored, is_premium
from config import Config

def userbot_cmd(command: str, category: str = "", description: str = "", premium: bool = False):
    """Decorator for userbot commands"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if not event.out:
                return
            
            user_id = event.sender_id
            
            # Check if ignored
            # ignored = get_ignored(user_id)
            
            # Check premium
            if premium and not is_premium(user_id) and user_id != Config.OWNER_ID:
                await event.edit("❌ **Fitur ini hanya untuk pengguna premium!**\nHubungi @{} untuk membeli premium.".format(Config.OWNER_USERNAME))
                return
            
            return await func(event)
        
        wrapper._command = command
        wrapper._category = category
        wrapper._description = description
        wrapper._premium = premium
        return wrapper
    return decorator

def owner_only(func):
    """Decorator for owner only commands"""
    @functools.wraps(func)
    async def wrapper(event):
        if event.sender_id != Config.OWNER_ID:
            return
        return await func(event)
    return wrapper

def admin_only(func):
    """Decorator for admin only commands"""
    @functools.wraps(func)
    async def wrapper(event):
        admins = [Config.OWNER_ID] + Config.ADMINS
        if event.sender_id not in admins:
            return
        return await func(event)
    return wrapper