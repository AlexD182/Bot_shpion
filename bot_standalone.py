from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data, find_wishes, GetSysytemTime
from time import time, sleep
import json
import os
import data_input as di
import asyncio
import aioschedule

bot = Bot(token = di.TOKEN, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["UP", "Staff", "Ping"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)    
    await message.answer("🔥GO!🔥", reply_markup=keyboard)


    
    
@dp.message_handler(Text(equals="UP"))
async def get_UP_data(message: types.Message):
    await message.answer("Please waiting...")

    UP_data = collect_data(di.UP_url_parks, di.UP_pagination_count)
    UP_result = find_wishes(di.UP_wishes, UP_data)
    card =''
    
    if(UP_result):             
        for el in UP_result:                
            card = str( el['Info'] + "\n" +
                        'Size:  ' + str(el['Size']).replace("[", "").replace("]", "").replace("'", "") +"\n" +
                        'Price:  ' + el['Price'] + "\n") 

            if ("PriceDiscount" in el):
                card += 'Price Discount:  ' + el["PriceDiscount"] + "🔥🔥🔥" + '\n'

            card += di.UP_url + el['id']
            await message.answer(card)        
    else:
        card = "Not found!"
        await message.answer(card)


#PING time    
@dp.message_handler(Text(equals="Ping"))
async def get_ping(message: types.Message):
    _curTime = str(GetSysytemTime())
    await message.answer(_curTime)





@dp.message_handler(Text(equals="Staff"))
async def my_func(message: types.Message):    
    await bot.send_message(message.chat.id, 'hi there')




def main():
    executor.start_polling(dp, skip_updates = True, on_startup=on_startup)
    

    
if __name__ == "__main__":
    main()