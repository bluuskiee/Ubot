from database import get_emoji, is_emoji_enabled

def e(user_id: int, emoji_type: str) -> str:
    """Get emoji for user, return empty string if emoji disabled"""
    if not is_emoji_enabled(user_id):
        return ""
    return get_emoji(user_id, emoji_type)

def fmt(user_id: int, emoji_type: str, text: str) -> str:
    """Format text with emoji"""
    emoji = e(user_id, emoji_type)
    if emoji:
        return f"{emoji} {text}"
    return text