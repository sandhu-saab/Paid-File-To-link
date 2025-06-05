from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

qr_url = "https://your-qr-image-link-here"  # change this to your real QR
payment_link = "https://t.me/yourusername"  # change to your Telegram or UPI link

@Client.on_message(filters.command("plan"))
async def plan_cmd(client, message: Message):
    await message.reply_photo(
        photo=qr_url,
        caption="""📋 *Plan Options:*

🟢 Trial – 7 Days – ₹FREE
🟢 30 Days – ₹XYZ

To upgrade your access, pay using the QR and send payment details.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📤 Send Payment Here", url=payment_link)]]
        )
    )
