import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink, is_premium
from datetime import datetime
from .fsub import check_fsub


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await check_fsub(client, message.from_user.id):
        return await message.reply_text(
            "🔒 You must join the required channels before using this bot.\nSend /fsub to get the links."
        )

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    text = (
        f"<b>👋 Welcome {message.from_user.mention}!</b>\n\n"
        f"This is an advanced <b>File to Direct Link Generator Bot</b>.\n\n"
        
    )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("🕐 1 Week ₹9", callback_data="plan_week"),
         InlineKeyboardButton("📅 1 Month ₹19", callback_data="plan_month")],
        [InlineKeyboardButton("📅 2 Months ₹29", callback_data="plan_2month"),
         InlineKeyboardButton("📅 3 Months ₹49", callback_data="plan_3month")],
        [InlineKeyboardButton("📆 1 Year ₹99", callback_data="plan_year")],
        [InlineKeyboardButton("✨ Update Channel", url="https://t.me/movieupdatewithak01")]
    ])

    await client.send_message(
        chat_id=message.from_user.id,
        text=text,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )


# ✅ /plan command will also show the same premium plans
@Client.on_message(filters.command("plan") & filters.private)
async def plan_command(client, message):
    await start(client, message)


# Callback query for buttons
@Client.on_callback_query(filters.regex("plan_"))
async def send_qr_code(client, callback_query: CallbackQuery):
    plan_map = {
        "plan_week": ("🕐 1 Week Plan", "₹9"),
        "plan_month": ("📅 1 Month Plan", "₹19"),
        "plan_2month": ("📅 2 Months Plan", "₹29"),
        "plan_3month": ("📅 3 Months Plan", "₹49"),
        "plan_year": ("📆 1 Year Plan", "₹99")
    }

    plan_key = callback_query.data
    plan_info = plan_map.get(plan_key, ("❓ Unknown Plan", "N/A"))
    plan_title, price = plan_info

    caption = (
        f"{plan_title}\n"
        f"💰 Price: {price}\n\n"
        f"📥 Scan this QR to pay\n"
        f"📌 UPI ID: abhishek.0307-27@waicici\n"
        f"👤 Payee Name: Abhishek Kumar\n\n"
        f"📩 After payment, send screenshot to @Tv_serial_wala"
    )

    await callback_query.message.reply_photo(
        photo="https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Send Screenshot", url="https://t.me/tv_serial_wala")]
        ])
    )
    await callback_query.answer()


# Handle document or video upload
@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    user_id = message.from_user.id
    username = message.from_user.mention

    if not await check_fsub(client, user_id):
        return await message.reply_text(
            "🔒 You must join the required channels before using this bot.\nSend /fsub to get the links."
        )

    if not is_premium(user_id):
        last_use = await db.get_last_use(user_id)
        today_str = datetime.now().strftime("%Y-%m-%d")
        if last_use == today_str:
            return await message.reply_text(
                "⚠️ You have already used your daily limit.\n\n"
                "💎 Contact the owner to upgrade. or Send me again /start",
                quote=True
            )
        await db.set_last_use(user_id, today_str)

    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )

    name = quote_plus(get_name(log_msg))
    if SHORTLINK:
        stream = await get_shortlink(f"{URL}watch/{log_msg.id}/{name}?hash={get_hash(log_msg)}")
        download = await get_shortlink(f"{URL}{log_msg.id}/{name}?hash={get_hash(log_msg)}")
    else:
        stream = f"{URL}watch/{log_msg.id}/{name}?hash={get_hash(log_msg)}"
        download = f"{URL}{log_msg.id}/{name}?hash={get_hash(log_msg)}"

    embed_code = f"<iframe src=\"{stream}\" width=\"100%\" height=\"500\" frameborder=\"0\" allowfullscreen></iframe>"

    await log_msg.reply_text(
        text=f"🔗 Link generated for user ID #{user_id}\n👤 Username: {username}\n📄 File: {filename}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=download),
             InlineKeyboardButton('🖥️ Watch Online', url=stream)]
        ])
    )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖥 Stream", url=stream),
         InlineKeyboardButton("📥 Download", url=download)],
        [InlineKeyboardButton("🌐 Embed Code", url=f"https://t.me/share/url?url={quote_plus(embed_code)}")]
    ])

    msg_text = (
        f"<i><u>𝐂𝐨𝐧𝐠𝐫𝐚𝐭𝐬 👏 𝐘𝐨𝐮𝐫 𝐋𝐢𝐧𝐤 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝!</u></i>\n\n"
        f"<b>File :</b> <i>{get_name(log_msg)}</i>\n"
        f"<b>📦 File Size:</b> <i>{humanbytes(get_media_file_size(message))}</i>\n\n"
        f"<b>📥 Download Link👇:</b> <i>{download}</i>\n"
        f"<b>🖥 Watch Link👇:</b> <i>{stream}</i>\n\n"
        f"<b>🌐 Embed Code:</b>\n<code>{embed_code}</code>\n\n"
        f"<b>🚸 Note:</b> Link will remain until the file is deleted."
    )

    await message.reply_text(
        text=msg_text,
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )
