from pyrogram import Client, filters
from premium import add_premium

ADMIN_IDS = [123456789]  # ← replace with your numeric Telegram ID

@Client.on_message(filters.command("addpremium") & filters.user(ADMIN_IDS) & filters.private)
async def add_premium_cmd(client, message):
    parts = message.text.split()
    if len(parts) != 3 or not parts[2].isdigit():
        return await message.reply_text("Usage: /addpremium <user_id> <days>")
    target, days = int(parts[1]), int(parts[2])
    add_premium(target, days)
    await message.reply_text(f"✅ {target} upgraded for {days} days.")
