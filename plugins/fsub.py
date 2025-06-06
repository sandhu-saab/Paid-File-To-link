import json
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_FILE = "fsub_channels.json"
OWNER_ID = 7459282233  # Replace this with your Telegram user ID

# Load required channels
def load_channels():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Save required channels
def save_channels(channels):
    with open(DB_FILE, "w") as f:
        json.dump(channels, f)

# Check if the user has joined all required channels
async def check_fsub(client, user_id):
    required_channels = load_channels()
    if not required_channels:
        return True  # No channels to check

    for ch in required_channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# Owner command to set required channels
@Client.on_message(filters.command("setfsub") & filters.private)
async def set_fsub_channels(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only the bot owner can set required channels.")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply_text("❗ Usage:\n`/setfsub -1001234567890`", parse_mode="markdown")

    try:
        channels = list(set(int(cid) for cid in parts[1:]))
        save_channels(channels)
        return await message.reply_text(
            f"✅ Force Subscribe Channel(s) Set Successfully!\n\n📢 Channel ID(s):\n`{channels}`",
            parse_mode="markdown"
        )
    except Exception as e:
        return await message.reply_text(f"❌ Error:\n`{e}`", parse_mode="markdown")

# Owner command to delete all required channels
@Client.on_message(filters.command("delfsub") & filters.private)
async def delete_fsub_channels(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only the bot owner can delete required channels.")
    save_channels([])
    await message.reply_text("🗑️ All required force subscribe channels have been removed.")

# User command to manually check status
@Client.on_message(filters.command("fsub") & filters.private)
async def manual_check_fsub(client, message):
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
        return await message.reply_text("✅ You have already joined all required channels. You may now use the bot!")

    buttons = []
    for ch in not_joined:
        try:
            invite_link = await client.export_chat_invite_link(ch)
            buttons.append([InlineKeyboardButton("📢 Join Channel", url=invite_link)])
        except:
            continue

    await message.reply_text(
        "🔒 Please join the following channel(s) to use this bot:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
