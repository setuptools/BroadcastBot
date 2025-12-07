

import aiogram
from aiogram import F
from aiogram.types import Message , CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State , StatesGroup
from aiogram.filters.command import Command , CommandStart


import aiosqlite


from utils.keyboard import start_menu
from utils.cleaner import clean_all_chat


from routes.broadcast import Broadcast 


__router__ = aiogram.Router()

@__router__.message(CommandStart())
@__router__.message(F.text & F.text.startswith("🏡 Main menu"))
async def start_handler(message:Message,state:FSMContext , bot:aiogram.Bot):

    await state.clear()
    await message.answer("""
👋 Hello, i'am @channels_broadcast_bot. I can send broadcast to your telegram channels! 
To continue press /broadcast or /help""", reply_markup=await start_menu())


    

@__router__.message(F.text == "❌ Cancel")
async def cancel_handler(message:Message,state:FSMContext):
    
    await state.clear()
    await message.answer("""
👋 Hello, i'am @channels_broadcast_bot. I can send broadcast to your telegram channels! 
To continue press /broadcast or /help""", reply_markup=await start_menu())
    