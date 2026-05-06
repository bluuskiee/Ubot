import json
import os
import asyncio
from typing import Any, Dict, Optional
from config import Config

DB_PATH = Config.DATABASE_PATH

os.makedirs(DB_PATH, exist_ok=True)

class Database:
    def __init__(self):
        self.db_files = {
            "users": f"{DB_PATH}users.json",
            "sessions": f"{DB_PATH}sessions.json",
            "settings": f"{DB_PATH}settings.json",
            "emoji": f"{DB_PATH}emoji.json",
            "prefix": f"{DB_PATH}prefix.json",
            "notes": f"{DB_PATH}notes.json",
            "premium": f"{DB_PATH}premium.json",
            "autobc": f"{DB_PATH}autobc.json",
            "locks": f"{DB_PATH}locks.json",
            "pmpermit": f"{DB_PATH}pmpermit.json",
            "ignore": f"{DB_PATH}ignore.json",
            "sudoers": f"{DB_PATH}sudoers.json",
            "payment": f"{DB_PATH}payment.json",
            "broadcast": f"{DB_PATH}broadcast.json",
        }
        self._init_db()
    
    def _init_db(self):
        for key, path in self.db_files.items():
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump({}, f)
    
    def _read(self, db_name: str) -> Dict:
        path = self.db_files.get(db_name)
        if not path:
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write(self, db_name: str, data: Dict):
        path = self.db_files.get(db_name)
        if not path:
            return
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get(self, db_name: str, key: str, default=None) -> Any:
        data = self._read(db_name)
        return data.get(str(key), default)
    
    def set(self, db_name: str, key: str, value: Any):
        data = self._read(db_name)
        data[str(key)] = value
        self._write(db_name, data)
    
    def delete(self, db_name: str, key: str):
        data = self._read(db_name)
        if str(key) in data:
            del data[str(key)]
        self._write(db_name, data)
    
    def get_all(self, db_name: str) -> Dict:
        return self._read(db_name)
    
    def exists(self, db_name: str, key: str) -> bool:
        data = self._read(db_name)
        return str(key) in data

db = Database()

# =================== USER FUNCTIONS ===================

def get_user(user_id: int) -> Optional[Dict]:
    return db.get("users", user_id)

def set_user(user_id: int, data: Dict):
    db.set("users", user_id, data)

def get_all_users() -> Dict:
    return db.get_all("users")

def is_premium(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False
    return user.get("premium", False)

def add_premium(user_id: int, added_by: int):
    user = get_user(user_id) or {}
    user["premium"] = True
    user["premium_by"] = added_by
    set_user(user_id, user)

def del_premium(user_id: int):
    user = get_user(user_id) or {}
    user["premium"] = False
    user.pop("premium_by", None)
    set_user(user_id, user)

def list_premium() -> list:
    users = get_all_users()
    return [uid for uid, data in users.items() if data.get("premium")]

# =================== SESSION FUNCTIONS ===================

def get_session(user_id: int) -> Optional[Dict]:
    return db.get("sessions", user_id)

def set_session(user_id: int, session_data: Dict):
    db.set("sessions", user_id, session_data)

def del_session(user_id: int):
    db.delete("sessions", user_id)

def get_all_sessions() -> Dict:
    return db.get_all("sessions")

# =================== SETTINGS FUNCTIONS ===================

def get_settings(user_id: int) -> Dict:
    default = {
        "prefix": ".",
        "bahasa": "id",
        "alive": True,
        "autoread": False,
        "pmpermit": False,
        "emoji_status": True,
    }
    settings = db.get("settings", user_id)
    if not settings:
        db.set("settings", user_id, default)
        return default
    return {**default, **settings}

def set_settings(user_id: int, key: str, value: Any):
    settings = get_settings(user_id)
    settings[key] = value
    db.set("settings", user_id, settings)

# =================== EMOJI FUNCTIONS ===================

DEFAULT_EMOJI = {
    "ping": "🏓",
    "uptime": "⏱️",
    "profil": "👤",
    "robot": "🤖",
    "msg": "💬",
    "warn": "⚠️",
    "block": "🚫",
    "gagal": "❌",
    "sukses": "✅",
    "owner": "👑",
    "klip": "📎",
    "net": "🌐",
    "up": "⬆️",
    "down": "⬇️",
    "speed": "⚡",
    "proses": "⏳",
    "status": "📊",
}

def get_emoji(user_id: int, emoji_type: str) -> str:
    emojis = db.get("emoji", user_id) or {}
    return emojis.get(emoji_type, DEFAULT_EMOJI.get(emoji_type, "❓"))

def set_emoji(user_id: int, emoji_type: str, emoji: str):
    emojis = db.get("emoji", user_id) or {}
    emojis[emoji_type] = emoji
    db.set("emoji", user_id, emojis)

def get_all_emoji(user_id: int) -> Dict:
    stored = db.get("emoji", user_id) or {}
    return {**DEFAULT_EMOJI, **stored}

def reset_emoji(user_id: int):
    db.delete("emoji", user_id)

def is_emoji_enabled(user_id: int) -> bool:
    settings = get_settings(user_id)
    return settings.get("emoji_status", True)

def toggle_emoji(user_id: int, status: bool):
    set_settings(user_id, "emoji_status", status)

# =================== PREFIX FUNCTIONS ===================

def get_prefix(user_id: int) -> str:
    settings = get_settings(user_id)
    return settings.get("prefix", ".")

def set_prefix(user_id: int, prefix: str):
    set_settings(user_id, "prefix", prefix)

def reset_prefix(user_id: int):
    set_settings(user_id, "prefix", ".")

# =================== NOTES FUNCTIONS ===================

def get_notes(user_id: int) -> Dict:
    return db.get("notes", user_id) or {}

def set_note(user_id: int, name: str, content: str):
    notes = get_notes(user_id)
    notes[name] = content
    db.set("notes", user_id, notes)

def del_note(user_id: int, name: str):
    notes = get_notes(user_id)
    if name in notes:
        del notes[name]
    db.set("notes", user_id, notes)

# =================== SUDOERS FUNCTIONS ===================

def get_sudoers(user_id: int) -> list:
    return db.get("sudoers", user_id) or []

def add_sudoer(user_id: int, sudo_id: int):
    sudoers = get_sudoers(user_id)
    if sudo_id not in sudoers:
        sudoers.append(sudo_id)
    db.set("sudoers", user_id, sudoers)

def del_sudoer(user_id: int, sudo_id: int):
    sudoers = get_sudoers(user_id)
    if sudo_id in sudoers:
        sudoers.remove(sudo_id)
    db.set("sudoers", user_id, sudoers)

# =================== PAYMENT FUNCTIONS ===================

def get_payment(user_id: int) -> Dict:
    return db.get("payment", user_id) or {}

def set_payment(user_id: int, data: Dict):
    db.set("payment", user_id, data)

# =================== AUTOBC FUNCTIONS ===================

def get_autobc(user_id: int) -> Dict:
    return db.get("autobc", user_id) or {}

def set_autobc(user_id: int, data: Dict):
    db.set("autobc", user_id, data)

def del_autobc(user_id: int):
    db.delete("autobc", user_id)

# =================== PMPERMIT FUNCTIONS ===================

def get_pmpermit(user_id: int) -> Dict:
    return db.get("pmpermit", user_id) or {
        "enabled": False,
        "message": "Halo! Pesan kamu sedang ditinjau oleh pemilik.",
        "approved": []
    }

def set_pmpermit(user_id: int, data: Dict):
    db.set("pmpermit", user_id, data)

# =================== IGNORE FUNCTIONS ===================

def get_ignored(user_id: int) -> list:
    return db.get("ignore", user_id) or []

def add_ignore(user_id: int, target_id: int):
    ignored = get_ignored(user_id)
    if target_id not in ignored:
        ignored.append(target_id)
    db.set("ignore", user_id, ignored)

def del_ignore(user_id: int, target_id: int):
    ignored = get_ignored(user_id)
    if target_id in ignored:
        ignored.remove(target_id)
    db.set("ignore", user_id, ignored)

# =================== LOCKS FUNCTIONS ===================

def get_locks(chat_id: int) -> Dict:
    return db.get("locks", chat_id) or {}

def set_lock(chat_id: int, lock_type: str, status: bool):
    locks = get_locks(chat_id)
    locks[lock_type] = status
    db.set("locks", chat_id, locks)

def is_locked(chat_id: int, lock_type: str) -> bool:
    locks = get_locks(chat_id)
    return locks.get(lock_type, False)