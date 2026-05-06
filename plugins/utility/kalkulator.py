import math
from telethon import events
from database import get_prefix
from config import Config

UNIT_CONVERSIONS = {
    "panjang": {
        "m": 1, "km": 1000, "cm": 0.01, "mm": 0.001,
        "inch": 0.0254, "ft": 0.3048, "yard": 0.9144, "mile": 1609.344
    },
    "berat": {
        "kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.453592, "oz": 0.028349
    },
    "suhu": "special",
    "waktu": {
        "detik": 1, "menit": 60, "jam": 3600, "hari": 86400, "minggu": 604800
    }
}

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    # Convert to Celsius first
    if from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert to target
    if to_unit == "F":
        return celsius * 9/5 + 32
    elif to_unit == "K":
        return celsius + 273.15
    return celsius

async def setup(client, user_id):
    prefix = get_prefix(user_id)
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}calc(?:\\s+(.+))?", outgoing=True))
    async def calc_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            help_text = (
                f"<blockquote>🔢 Bantuan Perintah Kalkulator</blockquote>\n\n"
                f"<b><blockquote expandable>Perintah Dasar</blockquote></b>\n\n"
                f"    <b>Hitung ekspresi matematika</b>\n"
                f"        .calc (ekspresi)\n"
                f"    <b>Konversi satuan</b>\n"
                f"        .convert (nilai) (dari) (ke)\n"
                f"    <b>Konversi suhu</b>\n"
                f"        .suhu (nilai) (C/F/K) (C/F/K)\n\n"
                f"    <b>Contoh:</b>\n"
                f"        .calc 2 + 2\n"
                f"        .calc (10 * 5) / 2\n"
                f"        .calc sqrt(16)\n"
                f"        .convert 100 m km\n"
                f"        .suhu 100 C F\n\n"
                f"🤖 INI BOT - @{Config.BOT_USERNAME}",
                parse_mode="html"
            )
            await event.edit(help_text, parse_mode="html")
            return
        
        try:
            # Safe evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "int": int, "float": float})
            
            result = eval(args, {"__builtins__": {}}, allowed_names)
            await event.edit(
                f"🔢 **Kalkulator**\n\n"
                f"**Ekspresi:** `{args}`\n"
                f"**Hasil:** `{result}`"
            )
        except ZeroDivisionError:
            await event.edit("❌ Error: Pembagian dengan nol!")
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}convert(?:\\s+(.+))?", outgoing=True))
    async def convert_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            await event.edit("❌ Format: `.convert (nilai) (dari) (ke)`\nContoh: `.convert 100 m km`")
            return
        
        parts = args.split()
        if len(parts) < 3:
            await event.edit("❌ Format: `.convert (nilai) (dari) (ke)`")
            return
        
        try:
            value = float(parts[0])
            from_unit = parts[1].lower()
            to_unit = parts[2].lower()
            
            # Find category
            result = None
            for category, conversions in UNIT_CONVERSIONS.items():
                if conversions == "special":
                    continue
                if from_unit in conversions and to_unit in conversions:
                    base = value * conversions[from_unit]
                    result = base / conversions[to_unit]
                    break
            
            if result is None:
                await event.edit(f"❌ Tidak bisa konversi `{from_unit}` ke `{to_unit}`!")
                return
            
            await event.edit(
                f"🔄 **Konversi Satuan**\n\n"
                f"**Nilai:** `{value} {from_unit}`\n"
                f"**Hasil:** `{result:.6f} {to_unit}`"
            )
        except ValueError:
            await event.edit("❌ Nilai harus berupa angka!")
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")
    
    @client.on(events.NewMessage(pattern=f"\\{prefix}suhu(?:\\s+(.+))?", outgoing=True))
    async def suhu_handler(event):
        args = event.pattern_match.group(1)
        
        if not args:
            await event.edit("❌ Format: `.suhu (nilai) (C/F/K) (C/F/K)`\nContoh: `.suhu 100 C F`")
            return
        
        parts = args.split()
        if len(parts) < 3:
            await event.edit("❌ Format: `.suhu (nilai) (dari) (ke)`")
            return
        
        try:
            value = float(parts[0])
            from_unit = parts[1]
            to_unit = parts[2]
            
            result = convert_temperature(value, from_unit, to_unit)
            
            await event.edit(
                f"🌡️ **Konversi Suhu**\n\n"
                f"**Nilai:** `{value}°{from_unit.upper()}`\n"
                f"**Hasil:** `{result:.2f}°{to_unit.upper()}`"
            )
        except Exception as e:
            await event.edit(f"❌ Error: `{str(e)}`")