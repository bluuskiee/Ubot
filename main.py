import asyncio
import os
import sys
import json
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import Config
from database import db, get_all_sessions, get_prefix

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Active userbot clients
active_clients = {}

async def load_plugins(client: TelegramClient, user_id: int):
    """Load all plugins for a client"""
    plugin_dirs = [
        "plugins/obrolan",
        "plugins/downloader",
        "plugins/hiburan",
        "plugins/media",
        "plugins/otomatisasi",
        "plugins/payment",
        "plugins/search",
        "plugins/system",
        "plugins/user",
        "plugins/utility",
        "plugins/premium",
    ]
    
    loaded = []
    for plugin_dir in plugin_dirs:
        if not os.path.exists(plugin_dir):
            continue
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_path = f"{plugin_dir}/{filename}".replace("/", ".").replace(".py", "")
                try:
                    module = __import__(module_path, fromlist=["setup"])
                    if hasattr(module, "setup"):
                        await module.setup(client, user_id)
                    loaded.append(filename)
                except Exception as e:
                    logger.error(f"Error loading plugin {filename}: {e}")
    
    logger.info(f"Loaded {len(loaded)} plugins for user {user_id}")

async def start_userbot(user_id: int, session_string: str):
    """Start a userbot client"""
    try:
        client = TelegramClient(
            StringSession(session_string),
            Config.API_ID,
            Config.API_HASH
        )
        await client.start()
        active_clients[user_id] = client
        await load_plugins(client, user_id)
        logger.info(f"Userbot started for user {user_id}")
        return client
    except Exception as e:
        logger.error(f"Error starting userbot for user {user_id}: {e}")
        return None

async def start_all_userbots():
    """Start all registered userbots"""
    sessions = get_all_sessions()
    tasks = []
    for user_id, session_data in sessions.items():
        session_string = session_data.get("session_string")
        if session_string and session_data.get("active", True):
            tasks.append(start_userbot(int(user_id), session_string))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    
    logger.info(f"Started {len(tasks)} userbots")

async def main():
    """Main entry point"""
    logger.info("🚀 Starting Userbot System...")
    logger.info(f"OS: {Config.OS_VERSION}")
    logger.info(f"DB: {Config.DB_TYPE}")
    
    # Start management bot
    from bot.main_bot import start_bot
    bot_task = asyncio.create_task(start_bot())
    
    # Start all registered userbots
    await start_all_userbots()
    
    logger.info("✅ All systems started!")
    
    await bot_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")