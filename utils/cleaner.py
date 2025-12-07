

import aiogram
from aiogram import types
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup
import aiocron

import traceback
import aiosqlite


from datetime import datetime

import logging
import asyncio



async def clean_all_chat(message:types.Message , bot:aiogram.Bot):

    chat_id = message.chat.id
    

    for i in range(1, 15):
        try:
            await bot.delete_message(chat_id, message.message_id - i)
        except:
            pass
