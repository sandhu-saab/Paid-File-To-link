from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

@Client.on_callback_query(filters.regex("plan_"))
async def plan_buttons(_, query: CallbackQuery):
    plans = {
        "plan_week": ("🕐 1 Week Plan\n\n💰 Price: ₹39", "https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg"),
        "plan_month": ("📅 1 Month Plan\n\n💰 Price: ₹69", "https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg"),
        "plan_2month": ("📅 2 Months Plan\n\n💰 Price: ₹149", "https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg"),
        "plan_3month": ("📅 3 Months Plan\n\n💰 Price: ₹199", "https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg"),
        "plan_year": ("📆 1 Year Plan\n\n💰 Price: ₹499", "https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg")
    }

    plan = plans.get(query.data)
    if plan:
        caption, qr_url = plan
        await query.message.reply_photo(
            photo=qr_url,
            caption=f"""{caption}

📥 *Scan QR or pay using UPI ID*: `kingvj@ybl`
👤 *Payee Name*: `VJ King`
📩 *Send Payment Screenshot to*: [@Sandymaiwait](https://t.me/Sandymaiwait)""",
            parse_mode="Markdown"
        )
    await query.answer()
