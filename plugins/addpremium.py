import json
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("addpremium"))
async def add_premium(client, message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        await message.reply_text("Usage: /addpremium <user_id> <days>")
        return

    user_id, days = parts[1], int(parts[2])
    try:
        with open("premium_users.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    data[user_id] = expiry

    with open("premium_users.json", "w") as f:
        json.dump(data, f, indent=4)

    await message.reply_text(f"✅ User {user_id} added to premium for {days} days (till {expiry}).")
