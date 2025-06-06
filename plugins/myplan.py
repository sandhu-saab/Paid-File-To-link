from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from premium import is_premium, get_expiry

@Client.on_message(filters.command("myplan") & filters.private)
async def myplan(client, message):
    uid = message.from_user.id

    if is_premium(uid):
        exp = get_expiry(uid)
        text = (
            "💎 <b>Premium Status</b>\n\n"
            "✅ You are a <b>Premium User</b>.\n"
            f"🗓️ <b>Valid Until:</b> <code>{exp}</code>\n\n"
            "🎉 Enjoy all premium features without limits!"
        )
        await message.reply_text(
            text=text,
            parse_mode="html"
        )
    else:
        text = (
            "❌ <b>You are not a Premium User</b>\n\n"
            "💡 Upgrade to unlock:\n"
            "▪️ Direct Downloads\n"
            "▪️ Ad-Free Experience\n"
            "▪️ Unlimited Links\n"
            "▪️ Fast Support\n\n"
            "Use /plan to upgrade now 🔥"
        )
        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📜 View Plans", url="https://t.me/YourBotUsername?start=plan")]]
        )
        await message.reply_text(
            text=text,
            parse_mode="html",
            reply_markup=btn
        )
