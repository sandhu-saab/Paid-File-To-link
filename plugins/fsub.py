from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANNEL = "your_channel_username"

@Client.on_message(filters.command("fsub") & filters.private)
async def fsub(client, message):
    try:
        member = await client.get_chat_member(CHANNEL, message.from_user.id)
        if member.status in ["creator","administrator","member"]:
            return await message.reply_text("✅ You are subscribed!")
    except:
        pass
    await message.reply_text(
        "🔒 Please join our channel to use this bot.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL}")]])
    )
