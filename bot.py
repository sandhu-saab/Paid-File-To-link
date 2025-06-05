import asyncio
import logging
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN
from Script import script
from database.users_chats_db import db
from datetime import datetime
from utils import temp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ✅ Create the bot client with plugin root set correctly
app = Client(
    "TechVJBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")  # ✅ This ensures all plugins load
)

async def main():
    await app.start()
    me = await app.get_me()

    # Store in temp for later use
    temp.BOT = app
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    # Log the restart event
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await app.send_message(
        chat_id=LOG_CHANNEL,
        text=script.RESTART_TXT.format(now.split()[0], now.split()[1])
    )

    logging.info(f"Bot Started as {me.first_name} (@{me.username})")

    await idle()
    await app.stop()
    logging.info("Bot Stopped")

if __name__ == '__main__':
    asyncio.run(main())
