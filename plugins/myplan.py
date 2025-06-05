import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("myplan") & filters.private)
async def myplan(client, message: Message):
    user_id = str(message.from_user.id)

    try:
        with open("premium_users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    if user_id in data:
        try:
            expiry = datetime.strptime(data[user_id], "%Y-%m-%d")
            days_left = (expiry - datetime.now()).days

            if days_left >= 0:
                await message.reply_text(
                    f"✅ You are a premium user!\n"
                    f"Your access expires in {days_left} day(s) (on {expiry.date()})."
                )
            else:
                await message.reply_text(
                    "❌ Your premium access has expired.\nUse /plan to renew your subscription."
                )
        except Exception as e:
            await message.reply_text("⚠️ Error while reading expiry date.")
    else:
        await message.reply_text(
            "❌ You are not a premium user.\nUse /plan to upgrade your access."
        )
