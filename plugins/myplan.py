from pyrogram import Client, filters
from premium import is_premium, get_expiry

@Client.on_message(filters.command("myplan") & filters.private)
async def myplan(client, message):
    uid = message.from_user.id
    if is_premium(uid):
        exp = get_expiry(uid)
        await message.reply_text(f"✅ You are a premium user till {exp}")
    else:
        await message.reply_text("❌ You are not a premium user\nUse /plan to upgrade")
