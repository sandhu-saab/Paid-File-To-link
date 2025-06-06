@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    welcome_text = f"""
<b>👋 Welcome {message.from_user.mention}!</b>

🚀 <b>This is an Advanced File-to-Link Generator Bot</b>

Using this bot, you can generate direct streaming and download links for any media file — in seconds!

<b>✨ Features:</b>

1️⃣ <b>Direct Stream Link</b> – Instantly get a link to watch your video file online without downloading.

2️⃣ <b>Fast Download Link</b> – Generate a secure & fast download link for your file.

3️⃣ <b>Unlimited File Support</b> – Send video, document, or file. We'll generate the link for you!

4️⃣ <b>One-Time Free Access</b> – Non-premium users can generate 1 free link every day.

5️⃣ <b>Premium Access</b> – Get unlimited link generation, faster performance, and priority access.

🔐 All links are secure and only accessible by you (unless shared).

💳 <b>To unlock unlimited link generation:</b>
Click the button below or use the <code>/plan</code> command to see available premium options.

"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 View Premium Plans", callback_data="plan")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/vj_botz")]
    ])

    await message.reply_text(
        welcome_text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )
