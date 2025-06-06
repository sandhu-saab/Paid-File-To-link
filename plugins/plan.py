from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# /plan command
@Client.on_message(filters.command("plan") & filters.private)
async def show_plan(client, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/66ac7485a5088c0871b13.jpg",  # Your QR code
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

# Close button action
@Client.on_callback_query(filters.regex("close_plan"))
async def close_plan_callback(client, callback_query):
    await callback_query.message.delete()
