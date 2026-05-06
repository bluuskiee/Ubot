import os
import asyncio
from telethon import events
from database import get_prefix
from config import Config

async def take_screenshot(url: str, output_path: str, width: int = 1920, height: int = 1080):
    """Take screenshot using chromium"""
    cmd = [
        "chromium-browser", "--headless", "--no-sandbox",
        "--disable-gpu", f"--window-size={width},{height}",
        f"--screenshot={output_path}", url
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}webshot(?:\\s+(.+))?", outgoing=True))
    async def webshot_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>📸 Bantuan Perintah WebShot</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Screenshot halaman web</b>\n"
                f"        .webshot (url)\n"
                f"    <b>Screenshot dengan resolusi custom</b>\n"
                f"        .webshot (url) (lebar)x(tinggi)\n\n"
                f"    <b>Contoh:</b>\n"
                f"        .webshot https://google.com\n"
                f"        .webshot https://google.com 1280x720\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        parts = args.split()
        url = parts[0]
        
        width, height = 1920, 1080
        if len(parts) > 1 and "x" in parts[1]:
            try:
                w, h = parts[1].split("x")
                width, height = int(w), int(h)
            except:
                pass
        
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        await event.edit(f"⏳ **Mengambil screenshot dari {url}...**")
        
        try:
            output_path = f"/tmp/webshot_{user_id}.png"
            await take_screenshot(url, output_path, width, height)
            
            if os.path.exists(output_path):
                await client.send_file(
                    event.chat_id,
                    output_path,
                    caption=f"📸 **Screenshot**\n🌐 {url}\n📐 {width}x{height}"
                )
                os.remove(output_path)
                await event.delete()
            else:
                await event.edit("❌ Gagal mengambil screenshot!")
                
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")