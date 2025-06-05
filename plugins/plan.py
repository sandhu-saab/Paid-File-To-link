from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("plan") & filters.private)
async def show_plan(client, message):
    qr_url = "https://telegra.ph/file/5cd4ef4be4cb84d678c9e.jpg"  # your QR image
    payment_link = "https://t.me/Sandymaiwait"  # your Telegram ID

    caption = (
        "📋 <b>Choose Your Plan:</b>\n\n"
        "🆓 <b>Trial:</b> 1 Day – ₹0 (Once per day only)\n"
        "💸 <b>Paid Plans:</b>\n"
        "▪️ 1 Day – ₹15\n"
        "▪️ 7 Days – ₹29\n"
        "▪️ 1 Month – ₹59\n"
        "▪️ 2 Months – ₹159\n"
        "▪️ 3 Months – ₹299\n"
        "▪️ 1 Year – ₹599\n\n"
        "📤 <b>To Upgrade:</b>\n"
        "Scan the QR below or tap the button to send payment.\n\n"
        "After payment, contact @Sandymaiwait to activate your plan."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Send Payment Here", url=payment_link)]
    ])

    await message.reply_photo(
        photo=qr_url,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="html"
    )
