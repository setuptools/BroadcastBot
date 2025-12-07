

import aiogram

import aiosqlite

import logging
import os

import asyncio

from aiogram import  Dispatcher
from aiogram.types import Message , CallbackQuery

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from utils.cleaner import clean_all_chat
from utils.keyboard import start_menu

from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
)


clean_commands = ["/start",
                "/help",
                "/broadcast",
                "❌ Cancel",
                
                
                
                "✒️ Edit name",
                "🖼️ Edit image",
                "🔗 Edit link",
                "🗑 Delete channel",

                "✅ Save",
                "✒️ Title",
                "📃 Description",
                "🔗 Link",
                "🖼️ Image",
                "▶️ Buttons",
                "⏰ Date",
                "🗑️ Delete",

                "⭐ My channels", 
                "📊 Broadcasts", 
                "📊 My broadcast", 
                "⚙️ Settings", 
                "🏡 Main menu",
                "🆘 Help",
                "⬅️ pervious",
                "next ➡️",
                "➕ Add channel",
                "➕ Add broadcast"
                ]


class BroadCastMiddleware(BaseMiddleware):


    def __init__(self,bot):
        super().__init__()

    
        self.bot = bot

        self.logger = logging.getLogger("aiogram")

        self.owners = os.environ.get("OWNERS_ID").split(",")


    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        

        if event and event.message:
            msg: Message = event.message


            if str(msg.from_user.id) not in self.owners:
                asyncio.create_task(clean_all_chat(msg,self.bot))
                await msg.answer(text="❌ You are not owner of this bot!", reply_markup=await start_menu())
                return

            if msg.text in clean_commands:
                asyncio.create_task(clean_all_chat(msg,self.bot))
            

            self.logger.info(f"message from {msg.from_user.username} : {msg.text} (channel: {msg.chat.title} {msg.chat.id})")

        
        elif event and event.callback_query:
            cb: CallbackQuery = event.callback_query


            if str(cb.from_user.id) not in self.owners:
                asyncio.create_task(clean_all_chat(msg,self.bot))
                await cb.answer(text="❌ You are not owner of this bot!")
                return

            self.logger.info(f"callback from {ck.from_user.username} : {ck.data} (channel: {cb.chat.title} {cb.chat.id})")
    

        return await handler(event, data)