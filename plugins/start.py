import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink, is_premium
from datetime import datetime
from .fsub import check_fsub

# /start command
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

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Update Channel", url="https://t.me/+DiOcxJnNQXdmNDdl")],
        [InlineKeyboardButton("📞 Contact Owner", url="https://t.me/Sandymaiwait")]
    ])

    welcome_text = (
        f"<b>👋 Welcome {message.from_user.mention}!</b>\n\n"
        f"This is an advanced <b>File to Direct Link Generator Bot</b>.\n\n"
        f"<b>✨ Features:</b>\n"
        f"1. 🔗 Generate Direct Download & Stream Links\n"
        f"2. 🛡 Daily Free Usage Limit for Normal Users\n"
        f"3. 💎 Premium Users Get Unlimited Access\n"
        f"4. 📞 Contact the owner to upgrade to premium\n\n"
        f"⚠️ Note: Free users can use this once per day."
    )

    await client.send_message(
        chat_id=message.from_user.id,
        text=welcome_text,
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )

# file upload handling
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
                "💎 Contact the owner to upgrade.",
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


# ✅ /plan command moved from plan.py to here
@Client.on_message(filters.command("plan") & filters.private)
async def show_plan(client, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/66ac7485a5088c0871b13.jpg",
        caption=(
            "🪪 <b>ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs ♻️</b>\n\n"
            "• 𝟷 ᴡᴇᴇᴋ   - ₹29\n"
            "• 𝟷 ᴍᴏɴᴛʜ  - ₹59\n"
            "• 𝟹 ᴍᴏɴᴛʜs - ₹249\n"
            "• 𝟼 ᴍᴏɴᴛʜs - ₹499\n\n"
            "•─────•─────────•─────•\n"
            "<b>ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs 🎁</b>\n\n"
            "○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs\n"
            "○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n"
            "○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n"
            "○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n"
            "○ ᴜɴʟɪᴍɪᴛᴇᴅ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ\n"
            "○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n"
            "○ ʀᴇǫᴜᴇsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ\n"
            "•─────•─────────•─────•\n\n"
            "✨ <b>UPI ID:</b> <code>lamasandeep821@okicici</code>\n\n"
            "💠 ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ → /myplan\n\n"
            "💢 <b>ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ</b>\n"
            "‼️ <i>ᴀꜰᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ, ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴠᴇʀsɪᴏɴ.</i>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Send Screenshot", url="https://t.me/Sandymaiwait")],
            [InlineKeyboardButton("❌ Close", callback_data="close_plan")]
        ]),
        parse_mode="html"
    )

@Client.on_callback_query(filters.regex("close_plan"))
async def close_plan_callback(client, callback_query):
    await callback_query.message.delete()
