import asyncio
import logging
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from Script import script
from utils import temp
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = Client(
    "TechVJBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")  # ✅ Automatically loads all plugin files here
)

@app.on_message()  # to log startup events
async def startup_log(client, message):
    pass

async def main():
    await app.start()
    me = await app.get_me()
    temp.BOT, temp.ME, temp.U_NAME, temp.B_NAME = app, me.id, me.username, me.first_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await app.send_message(LOG_CHANNEL, script.RESTART_TXT.format(now.split()[0], now.split()[1]))
    logging.info("Bot started!")
    await idle()
    await app.stop()
    logging.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
