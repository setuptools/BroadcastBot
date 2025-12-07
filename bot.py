

from math import log
from aiogram import Bot , Dispatcher , F
from aiogram.types import Message , CallbackQuery 

from aiogram.filters import CommandStart , Command  , BaseFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv 

from middleware.midddleware import BroadCastMiddleware

import os
import sys
import importlib
import asyncio
import subprocess

import aiosqlite

import logging

from datetime import datetime

load_dotenv()


logging.basicConfig(level=logging.INFO)


class TGBot(Bot):
    def __init__(self, token: str, ) -> None:
        super(TGBot,self).__init__(token)

        self.dp: Dispatcher = Dispatcher(storage=MemoryStorage())

        
        self.server_path = "/server/main.py"

        self._reload_list = [
            "./utils",
            "./middleware"
            ]
        

        self.middleware = BroadCastMiddleware(self)

        self.cycles_task = None
        self.cycles_class = None

    async def _load_cycles(self):
        from utils.broadcast import BroadCast

        if self.cycles_task and not self.cycles_task.done():
            await self.cycles_class.stop()
            self.cycles_task.cancel()
            try:
                await self.cycles_task
            except asyncio.CancelledError:
                pass


        self.cycles_class = BroadCast(self)
        self.cycles_task = asyncio.create_task(self.cycles_class.run())


    async def _load_handlers(self , use_reload:bool = False, init_again: bool = False):
        
        # reloading self._reload_list
        if use_reload:  
            if init_again:
                await self.on_startup()

            self.dp.sub_routers.clear()
            
            for _dir in self._reload_list:
                for file in os.listdir(_dir):
                    if file.endswith(".py"):
                        
                        full_file = _dir.replace("./","") +"." + file[:-3]


                        if full_file in sys.modules:
                            importlib.reload(sys.modules[full_file])
                        else:
                            importlib.import_module(full_file)
            
            self.dp.update.middleware.unregister(self.middleware)
            
            self.middleware = BroadCastMiddleware(self)
            self.dp.update.middleware.register(self.middleware)


        await self._load_cycles()

        for file in os.listdir("./routes"):
            if file.endswith(".py"):
                module_name = f"routes.{file[:-3]}"

                # remove module for import again it
                if module_name in sys.modules and use_reload:
                    del sys.modules[module_name]    
                module = importlib.import_module(module_name)


                if hasattr(module , "__router__"):
                    self.dp.include_router(module.__router__)

                

    async def _register_handler(self):
        


        @self.dp.message(F.text , Command("reload"))
        async def _reload_handler(message:Message):

            
            init_again = False 
            if "init_again" in message.text:
                init_again = True

            await self._load_handlers(True , init_again)
            msg = await message.answer("Reload good")
            await message.delete()
            
            await asyncio.sleep(0.5)
            await msg.delete()            
            



    async def init_db(self):
        

        self.db = await aiosqlite.connect("db.db")
        self.db.row_factory = aiosqlite.Row


        await self.db.execute("""CREATE TABLE IF NOT EXISTS broadcast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT, 
            image TEXt,
            buttons JSON,
            channel TEXT,
                                
            user_id INT,

            send_at INT,
            status BOOLEAN DEFAULT FALSE
        );""")


        await self.db.execute("""CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            active BOOLEAN DEFAULT TRUE ,
            name TEXT,
            channel TEXT , 
            image TEXT,
            bot_in BOOLEAN DEFAULT TRUE,
            user_id INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")

        await self.db.commit()


        return self.db


    async def on_startup(self):

        os.system("cls") if os.system != "nt" else os.system("clear")

        _route_len = [file for file in  os.listdir("./routes") if file.endswith(".py")]

        _bot_info = await self.get_me()
        _text = f"""
| 🤖 Bot id: {_bot_info.id}
| 🤖 Bot name: https://t.me/{_bot_info.username}
|
| 📍 Routes ({len(_route_len)}):
|"""
        print(_text)

        for route in _route_len:
            print(f"|   🔗Route: routes.{route[:-3]} loadeds")

    async def run(self):
        await self.init_db()
        # await self.init_server()
        # atexit.register(partial(self.delete_server))

        await self.on_startup()
        await self._load_handlers()
        await self._register_handler()

        self.dp.update.middleware.register(self.middleware)
        
        await self.dp.start_polling(self)
        
    


if __name__ == "__main__":
    
    async def main():
        try:
            bot = TGBot(os.environ["TOKEN"])
            await bot.run()
        except KeyboardInterrupt:
            print("🌂 Bot closed by user")
        finally:
            if bot.db:
                await bot.db.close()
                print("📊 DB closed")

            if hasattr(bot, "session") and bot.session:
                await bot.session.close()
                print("👤 Session closed")

    asyncio.run(main())




    


    