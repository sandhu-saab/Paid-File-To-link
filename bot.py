# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, asyncio, logging.config, pytz
from pathlib import Path
from datetime import date, datetime
from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script
from aiohttp import web
from plugins import web_server
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

# ✅ Import your plan command/plugin file here
import plugins.plan

# Setup logging
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

# ✅ Correct bot initialization that loads plugin callbacks
TechVJBot = Client(
    "TechVJBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}  # ✅ This enables all plugin commands
)

async def start():
    print('\nInitializing Your Bot...')
    await initialize_clients()

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    # Log restart info
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await TechVJBot.send_message(
        chat_id=LOG_CHANNEL,
        text=script.RESTART_TXT.format(today, time)
    )

    # Start web server
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()

    await idle()

if __name__ == '__main__':
    TechVJBot.start()  # Must start the bot first
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
