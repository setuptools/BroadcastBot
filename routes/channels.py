

from os import curdir
import aiogram
from aiogram import F
from aiogram.types import Message , CallbackQuery , ChatPhoto, ChatMember
from aiogram.fsm.state import State , StatesGroup 
from aiogram.fsm.context import FSMContext


from aiogram.enums.chat_member_status import ChatMemberStatus

from aiogram.filters.command import Command , CommandStart 
from aiogram.filters import StateFilter


import aiosqlite

from utils.keyboard import __broadcast_menu , __channels_menu , __channels_add_menu , __chanels_edit_menu
from utils.cleaner import clean_all_chat

from middleware.midddleware import clean_commands
from utils.filters import ChannelIdFilter

class Channel(StatesGroup):

    msg_id = State()

    name = State()
    image = State()
    channel_link = State()

    end = State()

    status = State()

    edit = State()
    edit_channel = State()
    edit_page = State()


class ChannelList(StatesGroup):
    page = State()
    channel = State()

__router__ = aiogram.Router()







async def __channels_menu_handler(message:Message,state:FSMContext,bot:aiogram.Bot,page:int=0):
    db = bot.db
    cursor = await db.execute("""SELECT * FROM channels WHERE user_id=?""",(message.from_user.id,))
    rows = await cursor.fetchall()
    channels = [dict(row) for row in rows]


    if page*3 >= len(channels):
        page -= 1

    
    await state.update_data(page=page)
    await message.answer(text=f"""
⭐ Channels menu
📊 Count of channels : <b>{len(channels)}</b>
📄 Page : <b>{page+1}/{int(len(channels)/3)+1}</b>                         
""",
    parse_mode="HTML",
    reply_markup=await __channels_menu(channels,page=page))



async def __channel_menu_handler(message:Message,state:FSMContext,bot:aiogram.Bot , _id:int =0):
    db = bot.db

    cursor = await db.execute("""SELECT * FROM channels WHERE user_id=? AND id=?""",(message.from_user.id,_id))
    rows = await cursor.fetchone()
    channel = dict(rows) if rows else {}

    data = await state.get_data()


    await clean_all_chat(message,bot)
    


    await state.clear()


    await state.set_state(ChannelList.page)
    await state.update_data(channel=channel, page = data.get("page",9))

    text = f"""
📛 <b>Name :</b> <code>{channel["name"]}</code>
🔗 <b>Channel Link :</b> <a href="{channel['channel']}">{channel['channel']}</a>

📊 <b>Status:</b> {'🟢 Active' if channel['active'] == 1 else '🔴 Not active'}

🚩 <b>Registered at:</b> <i>{channel['created_at']}</i>
"""


    if channel.get("image",False):
        await message.answer_photo(
            photo=channel["image"],
            caption=text,
            parse_mode='HTML',
            reply_markup=await __chanels_edit_menu(channel))

    else:
        await message.answer(
            text=text,
            parse_mode='HTML',
            reply_markup=await __chanels_edit_menu(channel))

@__router__.message(Command("channels"))
@__router__.message(F.text & F.text.startswith("⭐ My channels"))
async def channels_menu(message:Message,state:FSMContext,bot:aiogram.Bot):

    data = await state.get_data()
    page = data.get("page")

    if not page:

        await state.clear() 

        await state.set_state(ChannelList.page)
        await state.update_data(page=0)

        await __channels_menu_handler(message,state,bot,0)
    
    else:
        await __channels_menu_handler(message,state,bot,int(page))








@__router__.message(F.text ,StateFilter("ChannelList:page") ,ChannelIdFilter())
async def check_channel(message:Message,state:FSMContext,bot:aiogram.Bot):


    _id = message.text.split(" ")[-1].replace("#","")
    await __channel_menu_handler(message,state,bot,_id)





# CHANNEL EDITING


@__router__.message(F.text & F.text.startswith("✒️ Edit name"))
async def edit_channel_handler(message:Message,state:FSMContext,bot:aiogram.Bot):
    
    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        channel = data.get("channel")
        page = int(data.get("page"))


        if channel:
            await state.set_state(Channel.name)


            msg = await message.answer(text="Send me new name for your channel" , reply_markup=await __channels_add_menu())
            await state.update_data(msg_id=msg , edit = True , edit_channel=channel , edit_page = page)
    
    else:
        return


@__router__.message(F.text & F.text.startswith("🖼️ Edit image"))
async def edit_channel_pic_handler(message:Message,state:FSMContext,bot:aiogram.Bot):
    
    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        channel = data.get("channel")
        page = int(data.get("page"))


        if channel:
            await state.set_state(Channel.image)
            msg = await message.answer(text="Send me new image for your channel" , reply_markup=await __channels_add_menu())
            await state.update_data(msg_id=msg , edit = True , edit_channel=channel , edit_page = page)
    
    else:
        return
    


@__router__.message(F.text & F.text.startswith("🔗 Edit link"))
async def edit_channel_link_handler(message:Message,state:FSMContext,bot:aiogram.Bot):
    
    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        channel = data.get("channel")
        page = int(data.get("page"))


        if channel:
            await state.set_state(Channel.channel_link)
            msg = await message.answer(text="Send me new link to your channel" , reply_markup=await __channels_add_menu())
            await state.update_data(msg_id=msg , edit = True , edit_channel=channel , edit_page = page)
    
    else:
        return
    


@__router__.message(F.text & F.text.endswith("status"))
async def edit_channel_status_handler(message:Message,state:FSMContext,bot:aiogram.Bot):
    
    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        channel = data.get("channel")
        page = int(data.get("page"))


        if channel:
            db = bot.db
            await db.execute("""UPDATE channels SET active=? WHERE user_id=? AND id=? """,(not channel["active"],message.from_user.id,channel["id"]))
            await db.commit()
            await __channel_menu_handler(message,state,bot,channel["id"])

    
    else:
        return
    

@__router__.message(F.text & F.text.startswith("🗑 Delete channel"))
async def edit_channel_delete_handler(message:Message,state:FSMContext,bot:aiogram.Bot):
    
    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        channel = data.get("channel")
        page = int(data.get("page"))

        if channel:
            db = bot.db
            await db.execute("""DELETE FROM channels WHERE user_id=? AND id=? """,(message.from_user.id,channel["id"]))
            await db.commit()
            await __channels_menu_handler(message,state,bot,page)

    
    else:
        return



#  LIST CHANNEL
@__router__.message(F.text & F.text.startswith("⬅️ pervious"),StateFilter("ChannelList:page"))
async def channel_pervious(message:Message,state:FSMContext,bot:aiogram.Bot):


    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        page = int(data.get("page",0))-1 
        await __channels_menu_handler(message,state,bot,page if page>=0 else 0)
    
    else:
        return



@__router__.message(F.text & F.text.startswith("next ➡️"), StateFilter("ChannelList:page"))
async def channel_next(message:Message,state:FSMContext,bot:aiogram.Bot):

    if await state.get_state() == ChannelList.page:
        data = await state.get_data()
        page = int(data.get("page",0))+1
        await __channels_menu_handler(message,state,bot,page)
    
    else:
        return

# ADD CHANNELS



@__router__.message(F.text & F.text.startswith("➕ Add channel"))
async def add_channel(message:Message,state:FSMContext, bot:aiogram.Bot):


    await state.set_state(Channel.name)
    msg = await message.answer(text="Send me the name for your channel" , reply_markup=await __channels_add_menu())
    await state.update_data(msg_id=msg)


@__router__.message(Channel.name, F.text & ~F.text.startswith("/"),lambda m: m.text and m.text not in clean_commands)
async def get_name(message:Message,state:FSMContext,bot:aiogram.Bot):

    
    data =await state.get_data()

    if data["msg_id"] and not data.get("edit",False):
        await data["msg_id"].delete()

        await message.delete()



        await state.update_data({"name":message.text})
        await state.set_state(Channel.image)


        msg = await message.answer(text="Send me an image for your channel or input 'skip' for skip this step" , reply_markup=await __channels_add_menu())
        await state.update_data({"msg_id":msg})
    
    else:
        await message.delete()

        db:aiosqlite.Connection = bot.db

        await db.execute("""UPDATE channels SET name=? WHERE user_id=? AND id=?""",(_id,data["edit_channel"]["user_id"],data["edit_channel"]["id"]))
        await db.commit()

        await __channel_menu_handler(message,state,bot,data["edit_channel"]["id"])



@__router__.message((F.photo) |
    (F.text & ~F.text.in_(clean_commands)),
    Channel.image)
async def skip_image(message:Message,state:FSMContext,bot:aiogram.Bot):

    
    data =await state.get_data()


    if data["msg_id"] and not data.get("edit",False):
        await data["msg_id"].delete()


        if message.text:
            if message.text.lower() == "skip":
                await state.update_data(image=None)


            elif message.text.lower() != "skip":
                if not message.photo:
                    await message.delete()
                    msg = await message.answer(text="Please send me photo or input 'skip'",reply_markup=await __channels_add_menu())
                    await state.update_data(msg_id=msg)
                    return

        else:
            await state.update_data(image=message.photo[-1].file_id)


        await message.delete()
        await state.set_state(Channel.channel_link)
        msg = await message.answer(text="Send me the link of your channel")
        await state.update_data(msg_id=msg)


    else:
        await message.delete()

        image = None
        if message.text:
            if message.text.lower() == "skip":
                image = None


            elif message.text.lower() != "skip":
                if not message.photo:
                    await message.delete()
                    msg = await message.answer(text="Please send me photo or input 'skip'",reply_markup=await __channels_add_menu())
                    await state.update_data(msg_id=msg)
                    return

        else:
            image=message.photo[-1].file_id

        db:aiosqlite.Connection = bot.db
        await db.execute("""UPDATE channels SET image=? WHERE user_id=? AND id=?""",(image,data["edit_channel"]["user_id"],data["edit_channel"]["id"]))
        await db.commit()

        await __channel_menu_handler(message,state,bot,data["edit_channel"]["id"])



@__router__.message(Channel.channel_link , lambda m: m.text and m.text not in clean_commands)
async def get_channel_link(message:Message,state:FSMContext,bot:aiogram.Bot):

    
    data =await state.get_data()
    await data["msg_id"].delete()
    await message.delete()

    if message.text.startswith("@") or message.text.startswith("https://t.me/") or message.text.startswith("https://telegram.me/"):
        
        if data["msg_id"] and not data.get("edit",False):


            chat_identifier = message.text.strip().replace("@", "").split("/")[-1]
            await state.update_data(channel_link=chat_identifier)
            data = await state.get_data()
            

            db: aiosqlite.Connection = bot.db 
            cursor = await db.execute("""SELECT * FROM channels WHERE user_id=? """, (message.from_user.id,))
            rows = await cursor.fetchall()
            channels = [dict(row) for row in rows] 

            
            try:
                _id = "@"+chat_identifier if not chat_identifier.isdigit() else int("-100"+chat_identifier)
                channel = await bot.get_chat(_id)
                member = await bot.get_chat_member(chat_id=_id, user_id=message.from_user.id)
    
  

                if not any(row["channel"]==data["channel_link"] for row in channels) and member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    await db.execute("""INSERT INTO channels (name,channel,image,bot_in,user_id) VALUES (?, ?, ?, ?, ?)""",(
                        data["name"],_id,data["image"],False , message.from_user.id))
                
                    await db.commit()

                    await clean_all_chat(message,bot)



                    cursor = await db.execute("""SELECT * FROM channels WHERE user_id=? """, (message.from_user.id,))
                    rows = await cursor.fetchall()
                    channels = [dict(row) for row in rows] 


                    if not data["image"]:
                        await message.answer(text=f"✅ Your channel has been added successfully\n\nName : {data['name']}\nLink : {data['channel_link']}", 
                                            reply_markup=await __channels_menu(channels,0))
                    

                    else:
                        await bot.send_photo(chat_id=message.chat.id,
                                            caption=f"✅ Your channel has been added successfully\n\nName : {data['name']}\nLink : {data['channel_link']}",
                                            photo=data["image"],
                                            reply_markup=await __channels_menu(channels,0))

                    await state.clear()
                    await state.set_state(ChannelList.page)


                elif member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    msg = await message.answer(text="❌ You are not admin in this channel. Fix it and try again",reply_markup=await __channels_add_menu())
                    await state.update_data(msg_id=msg)
                
                else:
                    msg = await message.answer(text="❌ This channel is already exists in your list ",reply_markup=await __channels_add_menu())
                    await state.update_data(msg_id=msg)

                    return   

            except Exception as e:
                print(e)
                msg = await message.answer("❌ Cant get this channel. Please check and try again.", reply_markup=await __channels_add_menu())
                await state.update_data(msg_id=msg)
                return
            

        else:

            chat_identifier = message.text.strip().replace("@", "").split("/")[-1]
            _id = "@"+chat_identifier if not chat_identifier.isdigit() else int("-100"+chat_identifier)

            db:aiosqlite.Connection = bot.db
            await db.execute("""UPDATE channels SET channel=? WHERE user_id=? AND id=?""",(_id,data["edit_channel"]["user_id"],data["edit_channel"]["id"]))
            await db.commit()

            await __channel_menu_handler(message,state,bot,data["edit_channel"]["id"])


    else:
        
        msg= await message.answer(text="Invalid channel link",reply_markup=await __channels_add_menu())
        await state.update_data(msg_id=msg)

        return
        


