from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Editable URLs for your QR image and payment link
qr_url = "https://your-qr-image-link-here"  # update this to your QR image
payment_link = "https://t.me/yourusername"  # update this to your Telegram or UPI link

@Client.on_message(filters.command("plan") & filters.private)
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
