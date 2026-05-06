import asyncio
import os
import sys
import platform
import psutil
import humanize
from datetime import datetime
from typing import Optional
from telethon import TelegramClient
from config import Config
from database import get_prefix, get_emoji, is_emoji_enabled

START_TIME = datetime.now()

def get_uptime() -> str:
    delta = datetime.now() - START_TIME
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days = hours // 24
    hours = hours % 24
    return f"{days}h {hours}j {minutes}m {seconds}d"

def get_size(size_bytes: int) -> str:
    return humanize.naturalsize(size_bytes)

async def edit_or_reply(event, text: str, **kwargs):
    try:
        await event.edit(text, **kwargs)
    except Exception:
        await event.reply(text, **kwargs)

async def progress(current, total, event, start, text):
    now = datetime.now()
    diff = (now - start).seconds
    if diff % 5 == 0 or current == total:
        speed = current / diff if diff else 0
        elapsed = humanize.naturalsize(current)
        total_size = humanize.naturalsize(total)
        percentage = current * 100 / total
        bar = "▓" * int(percentage / 10) + "░" * (10 - int(percentage / 10))
        try:
            await event.edit(
                f"**{text}**\n"
                f"[{bar}] {percentage:.1f}%\n"
                f"📦 {elapsed} / {total_size}\n"
                f"⚡ {humanize.naturalsize(speed)}/s"
            )
        except:
            pass

def get_system_info() -> str:
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return (
        f"💻 **System Info**\n"
        f"OS: {Config.OS_VERSION}\n"
        f"CPU: {cpu}%\n"
        f"RAM: {get_size(ram.used)} / {get_size(ram.total)}\n"
        f"Disk: {get_size(disk.used)} / {get_size(disk.total)}\n"
        f"Python: {sys.version.split()[0]}"
    )

async def get_user_from_event(event):
    """Get user from reply or mention"""
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        return reply.sender_id, reply.sender
    
    args = event.pattern_match.group(1) if event.pattern_match.lastindex else ""
    if args:
        try:
            user = await event.client.get_entity(args)
            return user.id, user
        except:
            pass
    
    return None, None