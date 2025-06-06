import json
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_FILE = "fsub_channels.json"
OWNER_ID = 6046055058  # Replace with your Telegram user ID


def load_channels():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_channels(channels):
    with open(DB_FILE, "w") as f:
        json.dump(channels, f)


async def check_fsub(client, user_id):
    """
    ✅ Used in start.py to check if a user has joined the required channels.
    """
    required_channels = load_channels()
    if not required_channels:
        return True

    for ch in required_channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


@Client.on_message(filters.command("setfsub") & filters.private)
async def set_fsub_channels(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only the bot owner can set required channels.")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply_text(
            "❗ Usage:\n`/setfsub -1001234567890 -1009876543210`",
            parse_mode="markdown"
        )

    try:
        channels = []
        for cid in parts[1:]:
            if not cid.startswith("-100"):
                return await message.reply_text(
                    f"❌ Invalid channel ID `{cid}`. Use full format like `-100xxxxxxxxxx`.",
                    parse_mode="markdown"
                )
            channels.append(int(cid))

        save_channels(channels)
        return await message.reply_text(
            f"✅ Force Subscription channels updated:\n`{channels}`",
            parse_mode="markdown"
        )

    except Exception as e:
        return await message.reply_text(f"❌ Error:\n`{e}`", parse_mode="markdown")


@Client.on_message(filters.command("delfsub") & filters.private)
async def delete_fsub_channels(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only the bot owner can delete required channels.")

    save_channels([])
    await message.reply_text("🗑️ All required channels have been removed.")


@Client.on_message(filters.command("fsub") & filters.private)
async def manual_check_fsub(client, message):
    """
    🔁 Manual command for users to check and join required channels.
    """
    user_id = message.from_user.id
    required_channels = load_channels()
    not_joined = []

    for ch in required_channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not not_joined:
        return await message.reply_text("✅ You have joined all required channels. You can use the bot now.")

    buttons = []
    for ch in not_joined:
        try:
            invite_link = await client.export_chat_invite_link(ch)
            buttons.append([InlineKeyboardButton("📢 Join Channel", url=invite_link)])
        except:
            continue

    buttons.append([InlineKeyboardButton("🔁 I've Joined", callback_data="check_fsub")])

    await message.reply_text(
        "🔒 Please join the following channel(s) to use this bot:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex("check_fsub"))
async def recheck_subscription(client, callback_query):
    """
    🔁 Callback when user clicks "I've Joined" after subscribing
    """
    user_id = callback_query.from_user.id
    required_channels = load_channels()
    not_joined = []

    for ch in required_channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not not_joined:
        await callback_query.message.edit("✅ You have joined all required channels. You can now use the bot.")
    else:
        await callback_query.answer("❗ You still haven’t joined all required channels.", show_alert=True)
