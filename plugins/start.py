import random
import humanize
from datetime import datetime
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink

# ============ START COMMAND ============ #
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Update Channel", url="https://t.me/vj_botz")],
        [InlineKeyboardButton("💎 View Plans", callback_data="plans")]
    ])

    start_text = f"""
<b>👋 Hello {message.from_user.mention}, welcome to the File2Link Bot!</b>

🚀 <b>This bot helps you generate direct download & stream links for any file you send.</b>

<b>Features:</b>
1. 🎯 Instant direct stream link generation
2. 💎 Premium plans for unlimited usage
3. 🔒 Links don’t expire until deleted
4. ⚡ One-click watch online + fast download
5. 🌐 Built for daily & professional use

📌 For unlimited link generation, consider choosing a premium plan using /plan

<b>Now send me a file to get started!</b>
"""

    await client.send_message(
        chat_id=message.from_user.id,
        text=start_text,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )

# ============ STREAM LINK GENERATOR ============ #
@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    user_id = message.from_user.id

    # Check if user is premium
    is_premium = await db.is_premium(user_id)

    # If not premium, check usage
    if not is_premium:
        already_used = await db.check_today_used(user_id)
        if already_used:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Get Premium", callback_data="plans")]])
            await message.reply_text(
                "🚫 <b>You have already used your free limit today.</b>\n\n"
                "💎 Upgrade to premium for unlimited link generation.\n\n"
                "🛍 Use /plan to view available premium options.",
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
            return
        else:
            await db.update_usage(user_id)  # Mark as used today

    # File handling
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id
    username = message.from_user.mention

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )

    fileName = quote_plus(get_name(log_msg))

    if SHORTLINK is False:
        stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}")
        download = await get_shortlink(f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}")

    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
             InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)]
        ])
    )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖥 Stream", url=stream),
         InlineKeyboardButton("📥 Download", url=download)]
    ])

    msg_text = f"""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>

<b>📂 File name:</b> <i>{get_name(log_msg)}</i>
<b>📦 File size:</b> <i>{humanbytes(get_media_file_size(message))}</i>

<b>📥 Download:</b> <i>{download}</i>
<b>🖥 Watch:</b> <i>{stream}</i>

<b>🚸 Note:</b> Link won't expire till file is deleted.
"""

    await message.reply_text(
        text=msg_text,
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )
