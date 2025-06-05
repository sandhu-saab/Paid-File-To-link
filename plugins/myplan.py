import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("myplan"))
async def myplan(client, message: Message):
    user_id = str(message.from_user.id)
    try:
        with open("premium_users.json", "r") as f:
            data = json.load(f)
        if user_id in data:
            expiry = datetime.strptime(data[user_id], "%Y-%m-%d")
            days_left = (expiry - datetime.now()).days
            if days_left >= 0:
                await message.reply_text(f"You are a premium user ✅\nYour access expires in {days_left} days (on {expiry.date()}).")
                return
        await message.reply_text("You are not a premium user ❌\nUse /plan to upgrade your access.")
    except:
        await message.reply_text("Error reading premium data.")
