from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired

# Replace this with your update/join channel username
FORCE_SUB_CHANNEL = "vj_botz"  # without @

@Client.on_message(filters.command("fsub") & filters.private)
async def fsub(client, message: Message):
    try:
        user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
        if user.status in ["member", "creator", "administrator"]:
            await message.reply_text("✅ You have already joined the update channel.")
        else:
            raise UserNotParticipant  # not a valid member
    except UserNotParticipant:
        await message.reply_text(
            "🔒 You must join our update channel to use this bot.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📢 Join Now", url=f"https://t.me/{FORCE_SUB_CHANNEL}")]]
            )
        )
    except ChatAdminRequired:
        await message.reply_text("⚠️ I don’t have permission to check channel membership. Please make me an admin.")
