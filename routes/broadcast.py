

import traceback
import aiogram
from aiogram import F
from aiogram.types import Message , CallbackQuery , ChatPhoto , ChatMember
from aiogram.fsm.state import State , StatesGroup 
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto , InlineKeyboardButton , InlineKeyboardMarkup

from aiogram.filters import StateFilter

from aiogram.filters.command import Command , CommandStart



from datetime import datetime
import aiosqlite
import json

from utils.keyboard import __broadcast_menu , __channels_menu , __broadcast_add_menu , __broadcast_cancel_menu
from utils.cleaner import clean_all_chat
from utils.filters import ChannelIdFilter

class Broadcast(StatesGroup):
    
    msg_id = State()
    
    title = State()
    description = State()
    image= State()

    buttons = State()
    date = State()

    end = State()
    
    edit = State()
    edit_broadcast = State()


class BroadCastList(StatesGroup):
    page = State()

    edit = State()
    edit_broadcast = State()

__router__ = aiogram.Router()



async def __broadcast_maker(message:Message, state:FSMContext, bot = aiogram.Bot ):

    await state.set_state(Broadcast.msg_id)
    data = await state.get_data()


    textFirst= "📊 Broadcast maker" if not data.get("edit",False) else "📊 Broadcast editor"
    text= f"""
📊 Broadcast text

{data.get("title","")} 

{data.get("description","")}

{data.get("date","").strftime("%d.%m.%Y %H:%M") if data.get("date",None) else ""}
                         
"""
    
    images = data.get("image")


    keyboard =InlineKeyboardMarkup(
        inline_keyboard=[

        ]
    ) 

    if data.get("buttons",None):

        buttons_line =[]
        for button in data.get("buttons",[]):
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

    



    if images:
        if isinstance(images, list) and len(images) > 1:
            media = [
                InputMediaPhoto(media=photo, caption=text if i == 0 else None)
                for i, photo in enumerate(images)
            ]
            await message.answer_media_group(media=media)
            await message.answer("📊 Broadcast maker", reply_markup=await __broadcast_add_menu(data.get("edit",False)))



        else:

            photo = images[0] if isinstance(images, list) else images

            await message.answer(text=textFirst, reply_markup=await __broadcast_add_menu(data.get("edit",False)))

            if photo["type"] == "photo":
                await message.answer_photo(photo=photo["file_id"],caption=text,reply_markup=keyboard)
            elif photo["type"] == "video" :
                await message.answer_video(video=photo["file_id"],caption=text,reply_markup=keyboard)
            elif photo["type"] == "animation":
                await message.answer_animation(animation=photo["file_id"],caption=text,reply_markup=keyboard)


    else:
        await message.answer(text=textFirst, reply_markup=await __broadcast_add_menu(data.get("edit",False)))
        await message.answer(text=text, reply_markup=keyboard)

async def __broadcast_list_handler(message:Message,state:FSMContext,bot = aiogram.Bot,page:int=0):



    await state.set_state(BroadCastList.page)
    db = bot.db
    
    row = await db.execute("""SELECT * FROM broadcast WHERE user_id=?""",(message.from_user.id,))
    broadcasts = [dict(rw) for rw in await row.fetchall()]

    await message.answer(text=f"""
📊 Broadcast list {len(broadcasts)} broadcasts
    
📄 Page: {page+1}/{int(len(broadcasts)/3)+1}""", reply_markup=await __broadcast_menu(broadcasts,page))

@__router__.message(F.text & F.text.startswith("❌ Cancel") , StateFilter("Broadcast:end","Broadcast:title","Broadcast:description","Broadcast:image","Broadcast:date","Broadcast:buttons"))
async def broadcast_cancel_handler(message:Message,state:FSMContext,bot = aiogram.Bot):

    
    data = await state.get_data()
    await message.delete()

    await __broadcast_maker(message=message, state=state,bot=bot)



@__router__.message(F.text & F.text.startswith("🗑️ Delete") , StateFilter("Broadcast:msg_id"))
async def broadcast_delete_handler(message:Message,state:FSMContext,bot = aiogram.Bot):

    
    data = await state.get_data()
    await message.delete()

    db = bot.db
    await db.execute("DELETE FROM broadcast WHERE id=? AND user_id=?", (data.get("edit_broadcast",""),message.from_user.id))
    await db.commit()

    await __broadcast_list_handler(message,state,bot,0)





@__router__.message(F.text ,StateFilter("BroadCastList:page") ,ChannelIdFilter())
async def check_channel(message:Message,state:FSMContext,bot:aiogram.Bot):

    await clean_all_chat(message,bot)

    _id = message.text.split(" ")[-1].replace("#","")


    db = bot.db
    cursor = await db.execute("SELECT * FROM broadcast WHERE id=? AND user_id=? ", (_id,message.from_user.id))
    row = dict(await cursor.fetchone())



    await state.set_state(Broadcast.edit)

    image = row.get("image","")


    raw_date = row.get("send_at")  #
    formatted_date = ""

    if isinstance(raw_date, (int, float,str)):  
        dt = datetime.fromtimestamp(int(raw_date))
        formatted_date = dt


    else:
        formatted_date = ""
        

    await state.update_data({
        "edit":True,
        "edit_broadcast":row.get("id",""),
        "title":row.get("title",""),
        "description":row.get("description",""),
        "image":json.loads(image) if image != None else {},
        "buttons":json.loads(row.get("buttons","[]")),
        "user_id":row.get("user_id",""),
        "date":formatted_date,
    })

    await __broadcast_maker(message,state,bot)



@__router__.message(Command('broadcast'))
@__router__.message(F.text & F.text.startswith("📊 My broadcast"))
async def broadcast_handler(message:Message, state:FSMContext,bot = aiogram.Bot):
    

    await state.clear()
    await __broadcast_list_handler(message,state,bot,0)


@__router__.message(F.text & F.text.startswith("➕ Add broadcast"))
async def add_broadcast_handler(message:Message,state:FSMContext,bot = aiogram.Bot):

    await state.clear()

    await state.set_state(Broadcast.msg_id)
    await __broadcast_maker(message=message, state=state,bot=bot)



# list broadvast
@__router__.message(F.text & F.text.startswith("⬅️ pervious") , StateFilter("BroadCastList:page"))
async def channel_pervious(message:Message,state:FSMContext,bot:aiogram.Bot):


    if await state.get_state() == BroadCastList.page:
        data = await state.get_data()
        page = int(data.get("page",0))-1 
        await __broadcast_list_handler(message,state,bot,page if page>=0 else 0)
    
    else:
        return



@__router__.message(F.text & F.text.startswith("next ➡️"), StateFilter("BroadCastList:page"))
async def channel_next(message:Message,state:FSMContext,bot:aiogram.Bot):


    if await state.get_state() == BroadCastList.page:
        data = await state.get_data()
        page = int(data.get("page",0))+1
        await __broadcast_list_handler(message,state,bot,page)
    
    else:
        return


# edit broadcast


@__router__.message(F.text & F.text.startswith("📃 Description"))
async def broadcast_description_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    

    data = await state.get_data()
    await message.delete()

    await state.set_state(Broadcast.description)
    await message.answer(text="""✏️ Enter new description""", reply_markup=await __broadcast_cancel_menu())



@__router__.message(F.text , Broadcast.description)
async def broadcast_new_description_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    await message.delete()

    await state.update_data(description=message.text)
    await __broadcast_maker(message=message, state=state,bot=bot)


@__router__.message(F.text & F.text.startswith("✒️ Title"))
async def broadcast_title_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    

    data = await state.get_data()
    await message.delete()


    await state.set_state(Broadcast.title)
    await message.answer(text="""✏️ Enter new title""" , reply_markup=await __broadcast_cancel_menu())


@__router__.message(F.text , Broadcast.title)
async def broadcast_new_title_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    await message.delete()

    await state.update_data(title=message.text)
    await __broadcast_maker(message=message, state=state,bot=bot)



@__router__.message(F.text & F.text.startswith("▶️ Buttons"))
async def broadcast_buttons_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    
    data = await state.get_data()
    await message.delete()

    await state.set_state(Broadcast.buttons)
    await message.answer(text="""✏️ Enter new buttons (how to add button check in /help)""", reply_markup=await __broadcast_cancel_menu())



@__router__.message(F.text | F.document , Broadcast.buttons)
async def broadcast_new_buttons_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    await message.delete()

    if message.document:
        if not message.document.mime_type.startswith("application/json"):
            await message.answer("❌ Invalid file type. Expected JSON.")
            return
    

        else:
            _file = message.document.file_id
            file = await bot.get_file(_file)
            downloaded= await bot.download_file(file.file_path)
             
            try:
                content =json.loads( downloaded.read().decode("utf-8"))
            except:
                content = "<binary file, cannot decode>"
            

            await state.update_data(buttons = content)
            await __broadcast_maker(message=message, state=state,bot=bot)


    elif message.text:
        try:
            buttons = message.text.split("\n")

            _buttons = []

            for btn_row in buttons:
                _brtn = btn_row.split(",")
                
                
                if len(_brtn)== 1:
                    _btn = btn_row.split("|")
                    _btn = [
                        {
                        "text":_btn[0],
                        "url":_btn[1].strip() if len(_btn)>1 and _btn[1].strip().startswith("http") else "",
                        "callback_data":_btn[1].strip() if len(_btn)>1 and not _btn[1].strip().startswith("http") else ""
                    }
                    ]
                    _buttons.append(_btn)

                else:
                    _btns=[]
                    for __btn in _brtn:
                        _btn = __btn.split("|")
                        _btn = {
                            "text":_btn[0],
                            "url":_btn[1].strip() if len(_btn)>1 and _btn[1].strip().startswith("http") else "",
                            "callback_data":_btn[1].strip() if len(_btn)>1 and not _btn[1].strip().startswith("http") else ""
                        }
                        _btns.append(_btn)

                    _buttons.append(_btns)
            
            print(_buttons)
            await state.update_data(buttons=_buttons)
            await __broadcast_maker(message=message, state=state,bot=bot)

        except Exception as e:
            print(e)
            traceback.print_exc()
            await message.answer("❌ Invalid JSON format.")
            return
            



    





@__router__.message(F.text & F.text.startswith("🖼️ Image"))
async def broadcast_image_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    
    
    data = await state.get_data()
    await message.delete()

    await state.set_state(Broadcast.image)
    await message.answer(text="""🖼️ Send new photo""", reply_markup=await __broadcast_cancel_menu())


@__router__.message(F.photo | F.video | F.animation, Broadcast.image)
async def broadcast_collect_media(message: Message, state: FSMContext, bot=aiogram.Bot):
    # удаляем сообщение пользователя
    await message.delete()

    data = await state.get_data()
    user_id = message.from_user.id

    media_list = data.get("image", "")

    if message.photo:
        media_list = {"type":"photo","file_id":message.photo[-1].file_id}

    elif message.video:
        media_list = {"type": "video", "file_id": message.video.file_id}
    elif message.animation:
        media_list = {"type": "animation", "file_id": message.animation.file_id}

    else:
        await message.answer("❌ Unsupported media type")
        return

    await state.update_data(image=media_list)
    await __broadcast_maker(message=message, state=state, bot=bot)










@__router__.message(F.text & F.text.startswith("⏰ Date"))
async def broadcast_date_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    
    
    data = await state.get_data()
    await message.delete()

    await state.set_state(Broadcast.date)
    await message.answer(text="""⏰ Send new date""", reply_markup=await __broadcast_cancel_menu())

@__router__.message(F.text , Broadcast.date)
async def broadcast_new_date_handler(message:Message,state:FSMContext,bot = aiogram.Bot):
    await message.delete()
    
    user_input = message.text.strip()
    now = datetime.now()

    data = await state.get_data()

    if data.get("msg_id",None):
        await data["msg_id"].delete()
    
    broadcast_date = None
    
    try:
        broadcast_date = datetime.strptime(user_input, "%d.%m.%Y %H:%M")
    except ValueError:
        try:
            broadcast_date = datetime.strptime(user_input, "%d.%m.%Y")
        except ValueError:
            try:
                broadcast_date = datetime.strptime(user_input, "%H:%M")
                broadcast_date = broadcast_date.replace(
                    year=now.year, month=now.month, day=now.day
                )
            except ValueError:
                msg= await message.answer("❌ Value error. User input must be in format DD.MM.YYYY or DD.MM.YYYY HH:MM or HH:MM")
                await state.update_data(msg_id=msg)
                return
    
    if broadcast_date < now:
        msg= await message.answer("❌ Date is less than current time")
        await state.update_data(msg_id=msg)
        return
    

    await state.update_data(date=broadcast_date)
    await __broadcast_maker(message=message, state=state, bot=bot)



@__router__.message(F.text & F.text.startswith("✅ Save"))
async def broadcast_save_handler(message:Message,state:FSMContext,bot = aiogram.Bot):

    
    data = await state.get_data()
    await message.delete()



    if data.get("date",None) and data.get("description",None):

        db = bot.db

        await state.clear()


        await state.set_state(BroadCastList.page)


        if not data.get("edit",False):

            db:aiosqlite.Connection = bot.db
            await db.execute("INSERT INTO broadcast (title, description, image, buttons, channel, user_id, send_at, status) VALUES (?,?,?,?,?,?,?,?)",(
                data.get("title",""),
                data.get("description",""),
                json.dumps(data.get("image",[])),
                json.dumps(data.get("buttons",[])),
                message.chat.id ,
                message.from_user.id,
                data.get("date",None).timestamp(),
                False
            ))
            await db.commit()
        
        else:
            db:aiosqlite.Connection = bot.db
            await db.execute("UPDATE broadcast SET title=?, description=?, image=?, buttons=?, channel=?, user_id=?, send_at=?, status=? WHERE id=? AND user_id=?",(
                data.get("title",""),
                data.get("description",""),
                json.dumps(data.get("image",[])),
                json.dumps(data.get("buttons",[])),
                message.chat.id ,
                message.from_user.id,
                data.get("date",None).timestamp(),
                False, 
                data.get("edit_broadcast",""),
                message.from_user.id
            ))
            await db.commit()

        
        row = await db.execute("""SELECT * FROM broadcast WHERE user_id=?""",(message.from_user.id,))
        broadcasts = [dict(rw) for rw in await row.fetchall()]

        await message.answer(text="✅ Broadcast saved", reply_markup=await __broadcast_menu(broadcasts,0))
    
    else:
        await message.answer("❌ Please, enter a date/description for channel messaging")
        await __broadcast_maker(message=message, state=state, bot=bot)











    




