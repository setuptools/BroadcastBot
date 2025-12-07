



import aiogram
from aiogram.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , ReplyKeyboardRemove , KeyboardButton 

import aiosqlite






async def start_menu() -> ReplyKeyboardMarkup:



    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⭐ My channels")],
        [KeyboardButton(text="📊 My broadcast")],
        [KeyboardButton(text="🆘 Help")],
        
    ],
    resize_keyboard=True,
    one_time_keyboard=False)

    return keyboard



async def __channels_menu(channels:list=[],page:int =0) -> ReplyKeyboardMarkup:



    channels_buttons=[
        KeyboardButton(text=f"{channel['name']} #{channel['id']}")
        for channel in channels[page*3:(page+1)*3]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=[

        channels_buttons,

        [KeyboardButton(text="➕ Add channel")],
        [KeyboardButton(text="⬅️ pervious"), KeyboardButton(text="next ➡️")] if channels != [] and len(channels) > 3 else [],

        [KeyboardButton(text="🏡 Main menu")]
    ],resize_keyboard=True,one_time_keyboard=False)
    return keyboard


async def __chanels_edit_menu(channel:dict={}) -> ReplyKeyboardMarkup:
    
    status = "✅" if channel.get("active",0) == 1 else "❌"

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✒️ Edit name"), KeyboardButton(text="🖼️ Edit image"),KeyboardButton(text="🔗 Edit link")],
        [KeyboardButton(text=f"{status} status")],
        [KeyboardButton(text="🗑 Delete channel")],
        [KeyboardButton(text="⭐ My channels")]
    ],resize_keyboard=True,one_time_keyboard=False)

    return keyboard

async def __channels_add_menu() -> ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="❌ Cancel")]
    ],resize_keyboard=True,one_time_keyboard=False)

    return keyboard


async def __broadcast_cancel_menu() -> ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="❌ Cancel")]
    ],resize_keyboard=True,one_time_keyboard=False)

    return keyboard



async def __broadcast_menu(broadcasts:list=[],page:int =0) -> ReplyKeyboardMarkup:

    broadcasts_buttons=[
        KeyboardButton(text=f"{broadcast['title']} #{broadcast['id']}")
        for broadcast in broadcasts[page*3:(page+1)*3]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [*broadcasts_buttons],
        [KeyboardButton(text="➕ Add broadcast")],
        [KeyboardButton(text="⬅️ pervious"), KeyboardButton(text="next ➡️")] if broadcasts != [] and len(broadcasts) > 3 else [],
        [KeyboardButton(text="🏡 Main menu")]
    ],resize_keyboard=True,one_time_keyboard=False)

    return keyboard



async def __broadcast_add_menu(edit:bool=False) -> ReplyKeyboardMarkup:

    keyboard = ReplyKeyboardMarkup(keyboard=[

        [KeyboardButton(text="✒️ Title"), KeyboardButton(text="📃 Description")],

        [KeyboardButton(text="🖼️ Image"), KeyboardButton(text="▶️ Buttons")],
        [KeyboardButton(text="⏰ Date")],

        [KeyboardButton(text="✅ Save")],
        [KeyboardButton(text="🗑️ Delete")] if edit else [],
        [KeyboardButton(text="❌ Cancel")]
    ],resize_keyboard=True,one_time_keyboard=False)

    return keyboard


