from pyrogram import Client, filters
from premium import set_premium
from datetime import datetime, timedelta

# ✅ Your Telegram ID
ADMIN_ID = 7459282233

@Client.on_message(filters.command("addpremium") & filters.private)
async def add_premium_handler(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply_text("❌ You are not allowed to use this command.")
        return

    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.reply_text("❗ Usage: /addpremium user_id days\n\nExample: /addpremium 123456789 30")
            return

        user_id = int(parts[1])
        days = int(parts[2])
        set_premium(user_id, days)
        expiry = datetime.now() + timedelta(days=days)
        await message.reply_text(f"✅ Premium access added for user `{user_id}` till `{expiry.date()}`", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
