from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data, find_wishes, GetSysytemTime

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
    await message.answer("Please waiting...")

    UP_data = collect_data(di.UP_url_parks, di.UP_pagination_count)
    UP_result = find_wishes(di.UP_wishes, UP_data)
    
    
    if(UP_result):
        card =''             
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


###   PING time    
@dp.message_handler(Text(equals="Ping"))
async def get_ping(message: types.Message):
    _curTime = str(GetSysytemTime())
    _chat_id = "Chat id: " + str( message.chat.id)
    await message.answer(_curTime)
    await message.answer(_chat_id)




@dp.message_handler(Text(equals="Staff"))
async def my_func(message: types.Message):
    await bot.send_message( message.chat.id, 'hi there')




def main():
    print(GetSysytemTime(), "   Bot start")
    executor.start_polling(dp, skip_updates = True)
    

    
if __name__ == "__main__":
    main()