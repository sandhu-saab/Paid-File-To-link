import asyncio
import logging
import threading
from datetime import datetime

from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from Script import script
from utils import temp

# FastAPI Web Server for Koyeb Health Check
from fastapi import FastAPI
import uvicorn

web_app = FastAPI()

@web_app.get("/")
async def root():
    return {"status": "ok"}  # Koyeb health check response

def run_web():
    uvicorn.run(web_app, host="0.0.0.0", port=8080, log_level="warning")

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Pyrogram Client with plugin support
app = Client(
    "TechVJBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

# Optional startup event log
@app.on_message()
async def startup_log(client, message):
    pass  # Remove or customize if needed

# Main bot function
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

# Run bot and web server
if __name__ == "__main__":
    threading.Thread(target=run_web).start()  # Start health check web server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
