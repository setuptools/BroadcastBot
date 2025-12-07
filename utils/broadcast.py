

from email.mime import image
from inspect import trace
import aiogram
from aiogram import types
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup
import aiocron

import traceback
import aiosqlite

import json

from datetime import datetime

import logging
import asyncio

class BroadCast():
    def __init__(self, bot:aiogram.Bot ) -> None:
        self.bot = bot
        self.logger= logging.getLogger("broadcastbot")

        self.db:aiosqlite.Connection =bot.db

        self.tasks = []
    


    async def send_broadcast(self):
        

        while True:

            try:
                cur_broads = await self.db.execute('SELECT * FROM broadcast')
                broadcasts = await cur_broads.fetchall()

        


                for broadcast in broadcasts:

                    now = datetime.now()
                    if now.timestamp() >= broadcast['send_at']:
                        broadcast =dict(broadcast)
                        cur_channels = await self.db.execute('SELECT * FROM channels WHERE user_id=? AND active=1',(broadcast['user_id'],))
                        channels = await cur_channels.fetchall()


                        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

                        _buttons = json.loads(broadcast.get("buttons",[]))

                        if _buttons:
                            buttons_line =[]
                            for button in _buttons:
                                if len(button)>=2 and isinstance(button,list):
                                    for btn in button:
                                        buttons_line.append(InlineKeyboardButton(
                                            text=btn["text"],
                                            url=btn.get("url",""),
                                            callback_data = btn.get("callback_data","")))
                                    
                                    keyboard.inline_keyboard.append(buttons_line)
                                    buttons_line=[]
                                
                                else:

                                    keyboard.inline_keyboard.append([InlineKeyboardButton(
                                        text=button[0]["text"],
                                        url=button[0].get("url",""),
                                        callback_data = button[0].get("callback_data",""))])

    


                        for channel in channels:
                            channel=dict(channel)


                            _id = "@"+channel['channel'] if not channel["channel"].isdigit() else int("-100"+channel['channel'])

                            image_type = json.loads(broadcast.get("image",{})).get("type",None) 
                            image = json.loads(broadcast.get("image",{}))

                            if image_type == "photo":
                                photo = image
                                await self.bot.send_photo(_id, photo['file_id'], caption=broadcast['description'],parse_mode="html",reply_markup=keyboard)
                            
                            elif image_type == "video":
                                video = image
                                await self.bot.send_video(_id, video['file_id'], caption=broadcast['description'],parse_mode="html",reply_markup=keyboard)
                            
                            elif image_type == "animation":
                                animation = image
                                await self.bot.send_animation(_id, animation['file_id'], caption=broadcast['description'],parse_mode="html",reply_markup=keyboard)

                            else:
                                await self.bot.send_message(_id, broadcast['description'], parse_mode='HTML', reply_markup=keyboard)
                        

                        await self.db.execute('''DELETE FROM broadcast WHERE id=?''', (broadcast['id'],))
                        await self.db.commit()
                

                await asyncio.sleep(3)
            
            except Exception as a:
                print(a)
                traceback.print_exc()
                await asyncio.sleep(3)

        

    async def run(self):


        task_funcs = [self.send_broadcast]
        self.tasks = [asyncio.create_task(f()) for f in task_funcs]
        await asyncio.gather(*self.tasks, return_exceptions=True)
    

    async def stop(self):
        for t in self.tasks:
            if not t.done():
                t.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)