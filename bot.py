import sys, glob, importlib, logging, logging.config, pytz, asyncio, os, gc
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, idle 
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
TechVJBot.start()
loop = asyncio.get_event_loop()

# --- MEMORY CLEANER (Bedelkii Auto Restart) ---
# Tani waxay nadiifineysaa Memory-ga iyadoon Bot-ka damin
async def memory_cleaner():
    while True:
        await asyncio.sleep(1800) # 30 daqiiqo kasta
        n = gc.collect()
        logging.info(f"♻️ Memory Cleaned: {n} objects collected.")
# ---------------------------------------------

async def start():
    print('\n')
    print('Initalizing Your Bot')
    bot_info = await TechVJBot.get_me()
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Tech VJ Imported => " + plugin_name)
    
    # KICINTA PING SERVER (Waa Muhiim)
    try:
        asyncio.create_task(ping_server())
    except Exception as e:
        print(f"Ping server error: {e}")

    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    
    # WEB SERVER SETUP
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    server_port = int(PORT) # Hubi in PORT uu yahay lambar
    await web.TCPSite(app, bind_address, server_port).start()
    print(f"✅ Web Server Started on {bind_address}:{server_port}")
    
    # --- Start Memory Cleaner ---
    asyncio.create_task(memory_cleaner())
    # ----------------------------
    
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
