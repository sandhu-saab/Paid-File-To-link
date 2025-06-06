import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink, is_premium
from datetime import datetime

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Update Channel", url="https://t.me/vj_botz")],
        [InlineKeyboardButton("📜 View Plans", callback_data="show_plans")]
    ])

    welcome_text = (
        f"<b>👋 Welcome {message.from_user.mention}!</b>\n\n"
        f"This is an advanced <b>File to Direct Link Generator Bot</b>.\n\n"
        f"<b>✨ Features:</b>\n"
        f"1. 🔗 Generate Direct Download & Stream Links\n"
        f"2. 🛡 Daily Free Usage Limit for Normal Users\n"
        f"3. 💎 Premium Users Get Unlimited Access\n"
        f"4. 🧾 Use /plan to View or Upgrade to Premium\n\n"
        f"⚠️ Note: Free users can use this once per day.\n"
        f"Use <b>/plan</b> to get unlimited access."
    )

    await client.send_message(
        chat_id=message.from_user.id,
        text=welcome_text,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    user_id = message.from_user.id
    username = message.from_user.mention

    # Check usage for free users
    if not is_premium(user_id):
        last_use = await db.get_last_use(user_id)
        today_str = datetime.now().strftime("%Y-%m-%d")
        if last_use == today_str:
            return await message.reply_text(
                "⚠️ You have already used your daily limit.\n\n"
                "💎 Upgrade to premium for unlimited access using /plan",
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

    await log_msg.reply_text(
        text=f"🔗 Link generated for user ID #{user_id}\n👤 Username: {username}\n📄 File: {name}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=download),
             InlineKeyboardButton('🖥️ Watch Online', url=stream)]
        ])
    )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖥 Stream", url=stream),
         InlineKeyboardButton("📥 Download", url=download)]
    ])

    msg_text = (
        f"<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱!</u></i>\n\n"
        f"<b>📂 File Name:</b> <i>{get_name(log_msg)}</i>\n"
        f"<b>📦 File Size:</b> <i>{humanbytes(get_media_file_size(message))}</i>\n\n"
        f"<b>📥 Download:</b> <i>{download}</i>\n"
        f"<b>🖥 Watch:</b> <i>{stream}</i>\n\n"
        f"<b>🚸 Note:</b> Link will remain until the file is deleted."
    )

    await message.reply_text(
        text=msg_text,
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )
