

import aiogram
from aiogram import F
from aiogram.types import Message , CallbackQuery
from aiogram.filters.command import Command , CommandStart

from aiogram.fsm.context import FSMContext

import aiosqlite


from utils.keyboard import start_menu




help_text = ""

with open("./help.md","r",encoding="utf-8") as r_obj:
    help_text = r_obj.read()

__router__ = aiogram.Router()




@__router__.message(Command('help'))
@__router__.message(F.text & F.text.lower() == "🆘 help")
async def help_handler(message:Message , state:FSMContext, bot:aiogram.Bot ):
    await message.answer(text=help_text, reply_markup=await start_menu(), parse_mode='MarkdownV2' )