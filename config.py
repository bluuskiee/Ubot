import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "database/")
    
    # Owner & Admin
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Bluuesnt")
    ADMINS = list(map(int, os.getenv("ADMINS", "").split())) if os.getenv("ADMINS") else []
    ADMIN_USERNAMES = ["Cimekcu", "Princebluu"]
    
    # Bot Info
    BOT_USERNAME = os.getenv("BOT_USERNAME", "namabot")
    BOT_NAME = os.getenv("BOT_NAME", "UserBot Manager")
    
    # Payment
    SAWERIA_TOKEN = os.getenv("SAWERIA_TOKEN", "")
    
    # Default Config
    DEFAULT_PREFIX = "."
    OWNER_PREFIX = "x"
    
    # Premium Features
    PREMIUM_FEATURES = [
        "autobc", "spam", "clone", "broadcast", 
        "invite", "copy", "pmpermit", "vctools"
    ]
    
    # Ubuntu Version
    OS_VERSION = "Ubuntu LTS 24.04"
    
    # Database Type
    DB_TYPE = "JSON"