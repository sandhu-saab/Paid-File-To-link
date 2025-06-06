from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.command("plan") & filters.private)
async def show_plan_buttons(client, message: Message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🕐 1 Week ₹9", callback_data="plan_week"),
         InlineKeyboardButton("📅 1 Month ₹19", callback_data="plan_month")],
        [InlineKeyboardButton("📅 2 Months ₹29", callback_data="plan_2month"),
         InlineKeyboardButton("📅 3 Months ₹49", callback_data="plan_3month")],
        [InlineKeyboardButton("📆 1 Year ₹99", callback_data="plan_year")]
    ])

    await message.reply_text(
        "💎 Choose a Premium Plan below to get unlimited access:",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("plan_"))
async def plan_buttons(_, query: CallbackQuery):
    plans = {
        "plan_week": ("🕐 1 Week Plan\n\n💰 Price: ₹9", "https://envs.sh/ftM.jpg"),
        "plan_month": ("📅 1 Month Plan\n\n💰 Price: ₹19", "https://envs.sh/ftX.jpg"),
        "plan_2month": ("📅 2 Months Plan\n\n💰 Price: ₹29", "https://envs.sh/ft6.jpg"),
        "plan_3month": ("📅 3 Months Plan\n\n💰 Price: ₹49", "https://envs.sh/ftV.jpg"),
        "plan_year": ("📆 1 Year Plan\n\n💰 Price: ₹99", "https://envs.sh/ftx.jpg")
    }

    plan = plans.get(query.data)
    if plan:
        caption, qr_url = plan
        await query.message.reply_photo(
            photo=qr_url,
            caption=f"""{caption}

📥 *Scan QR or pay using UPI ID*: `abhishek.0307-27@waicici`
👤 *Payee Name*: `Abhishek kumar `
📩 *Send Payment Screenshot to*: [@Tv_serial_wala](https://t.me/Tv_serial_wala)""",
            parse_mode="Markdown"
        )
    await query.answer()
