from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
#from aiogram.utils.markdown import hbold, hlink

#import asyncio
#import aiohttp
#import nest_asyncio

import asyncio
### works 25.10
#asyncio.set_event_loop(asyncio.new_event_loop())


from bot_server import collect_data_in_page, find_wishes, GetSysytemTime, result_to_msg
import data_input as di


bot = Bot(token = di.TOKEN, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot)


###   Start
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["UP", "Staff", "Ping"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)    
    await message.answer("🔥GO!🔥", reply_markup=keyboard)


###   UP store 
@dp.message_handler(Text(equals="UP"))
async def get_UP_data(message: types.Message):
    print( str(GetSysytemTime()), "[bot] :: UP button pressed!") #LOG 
    await message.answer("Please waiting...")

    UP_dataBot = collect_data_in_page(di.UP_url_parks, di.UP_pagination_count)
    UP_resultBot = find_wishes(di.UP_wishes, UP_dataBot) 

    if(UP_resultBot):
        UP_massengesBot = result_to_msg(UP_resultBot)
        for text in UP_massengesBot:
            await message.answer(text)    
    else:              
        await message.answer("Nothing founded in products!")





###   STAFF store 
@dp.message_handler(Text(equals="Staff"))
async def my_func(message: types.Message):
    print( str(GetSysytemTime()), "[bot] :: Staff button pressed!") #LOG 
    await bot.send_message( message.chat.id, 'hi there')




###   PING time    
@dp.message_handler(Text(equals="Ping"))
async def get_ping(message: types.Message):
    print( str(GetSysytemTime()), "[bot] :: Ping button pressed!") #LOG 
    _curTime = str(GetSysytemTime())
    _chat_id = "Chat id: " + str( message.chat.id)
    await message.answer(_curTime)
    await message.answer(_chat_id)



def BotRun():    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    

    #nest_asyncio.apply()
    #get_or_create_eventloop()
         
    #print(GetSysytemTime(), " -=Bot start=-") #LOG
    executor.start_polling(dp, skip_updates = True)
    

    
    
    
if __name__ == "__main__":
    BotRun()