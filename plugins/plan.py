from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    qr_url = "https://telegra.ph/file/5cd4ef4be4cb84d678c9e.jpg"
    payment_link = "https://t.me/Sandymaiwait"

    text = (
        "📋 *Premium Plans:*\n\n"
        "🟢 1 Day – ₹15\n"
        "🟢 7 Days – ₹29\n"
        "🟢 30 Days – ₹59\n"
        "🟢 60 Days – ₹159\n"
        "🟢 90 Days – ₹299\n"
        "🟢 1 Year – ₹599\n\n"
        "🎁 *Free Trial:* 1 use per day only\n\n"
        "📸 Scan QR or tap below to pay and send proof to admin."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Send Payment Here", url=payment_link)]
    ])

    await message.reply_photo(photo=qr_url, caption=text, reply_markup=keyboard, parse_mode="markdown")
