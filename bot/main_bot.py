import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db

logger = logging.getLogger(__name__)

app = Client(
    "management_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

async def start_bot():
    """Start the management bot"""
    from bot.handlers import start, buy, manage, admin
    await app.start()
    logger.info("Management bot started!")
    await app.idle()