import random import humanize from Script import script from pyrogram import Client, filters, enums from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery from info import URL, LOG_CHANNEL, SHORTLINK from urllib.parse import quote_plus from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size from TechVJ.util.human_readable import humanbytes from database.users_chats_db import db from utils import temp, get_shortlink, is_premium from datetime import datetime from .fsub import check_fsub

/start command

@Client.on_message(filters.command("start") & filters.incoming) async def start(client, message): if not await check_fsub(client, message.from_user.id): return await message.reply_text( "🔒 You must join the required channels before using this bot.\nSend /fsub to get the links." )

if not await db.is_user_exist(message.from_user.id):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    await client.send_message(
        LOG_CHANNEL,
        script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
    )

text = (
    f"<b>👋 Welcome {message.from_user.mention}!</b>\n\n"
    f"This is an advanced <b>File to Direct Link Generator Bot</b>.\n\n"
    f"<b>✨ Features:</b>\n"
    f"• 🔗 Direct Download & Streaming Links\n"
    f"• 🛡 One Free Use per Day (Normal Users)\n"
    f"• 💎 Unlimited Access for Premium Users\n"
    f"• 📞 Contact owner to upgrade anytime\n\n"
    f"⚠️ Note: Free users can use this bot once per day.\n\n"
    f"<b>💎 Premium Plans:</b>\n"
    f"Unlock premium for faster downloads, unlimited usage, and priority support!\n\n"
    f"<b>📋 Plans:</b>\n"
    f"1. 🆓 Free Trial — Once per day\n"
    f"2. 🕐 1 Week — ₹39\n"
    f"3. 📅 1 Month — ₹69\n"
    f"4. 📅 2 Months — ₹149\n"
    f"5. 📅 3 Months — ₹199\n"
    f"6. 📆 1 Year — ₹499\n\n"
    f"👉 To upgrade, choose a plan below and send payment screenshot to support.\n"
    f"Your premium access will be activated shortly. ✅"
)

rm = InlineKeyboardMarkup([
    [InlineKeyboardButton("🕐 1 Week ₹39", callback_data="plan_week"),
     InlineKeyboardButton("📅 1 Month ₹69", callback_data="plan_month")],
    [InlineKeyboardButton("📅 2 Months ₹149", callback_data="plan_2month"),
     InlineKeyboardButton("📅 3 Months ₹199", callback_data="plan_3month")],
    [InlineKeyboardButton("📆 1 Year ₹499", callback_data="plan_year")],
    [InlineKeyboardButton("📤 Send Payment Screenshot", url="https://t.me/Sandymaiwait")],
    [InlineKeyboardButton("✨ Update Channel", url="https://t.me/+DiOcxJnNQXdmNDdl")]
])

await client.send_message(
    chat_id=message.from_user.id,
    text=text,
    reply_markup=rm,
    parse_mode=enums.ParseMode.HTML
)

file upload handling

@Client.on_message(filters.private & (filters.document | filters.video)) async def stream_start(client, message): user_id = message.from_user.id username = message.from_user.mention

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
    f"<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱!</u></i>\n\n"
    f"<b>📂 File Name:</b> <i>{get_name(log_msg)}</i>\n"
    f"<b>📦 File Size:</b> <i>{humanbytes(get_media_file_size(message))}</i>\n\n"
    f"<b>📥 Download:</b> <i>{download}</i>\n"
    f"<b>🖥 Watch:</b> <i>{stream}</i>\n\n"
    f"<b>🌐 Embed Code:</b>\n<code>{embed_code}</code>\n\n"
    f"<b>🚸 Note:</b> Link will remain until the file is deleted."
)

await message.reply_text(
    text=msg_text,
    quote=True,
    disable_web_page_preview=True,
    reply_markup=rm
)

