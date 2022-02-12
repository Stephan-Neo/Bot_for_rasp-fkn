from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from difflib import Differ, HtmlDiff
from os import path


import requests
from bs4 import BeautifulSoup

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_check = KeyboardButton('проверить изменения 📡')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_check)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=greet_kb)


@dp.message_handler()
async def echo_message(msg: types.Message):
    MESS_MAX_LENGTH = 4096

    if 'проверить изменения' in msg.text:
        # url = 'http://fkn.omsu.ru/academics/schedule1.htm'
        supplement = 'http://fkn.omsu.ru/academics/'
        # page_global = requests.get(url)
        # soup_global = BeautifulSoup(page_global.content, "lxml")
        # soup_global_str = str(BeautifulSoup(page_global.content, "lxml"))
        # wrapper_links = soup_global.find("div", class_='main-content-inner')

        list_links = ["Schedule/schedule1_2.htm", "Schedule/schedule2_2.htm", "Schedule/schedule3_2.htm", "Schedule/schedule4_2.htm"]
        for array_links in list_links:
    
            link = supplement + array_links
            src_file = "source/html/" + array_links
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "lxml")
            rasp = soup.find("div", class_='column')
            page_title = (soup.find("h1", id='page-title')).text
            new_rasp_str = str(rasp)
            
            if not(path.exists(src_file)):
                with open(src_file, "w", encoding='UTF-8') as f:
                    f.close()
            
            with open("source/html/Schedule/G_rasp.html", "w", encoding='UTF-8') as diff_file:
                diff_file.write(new_rasp_str)
            
            now_rasp = open('source/html/Schedule/G_rasp.html', 'r', encoding='UTF-8').read()

            file = open(src_file, 'r', encoding='UTF-8')
            last_rasp = file.read()
            file.close()


            if now_rasp == last_rasp:
                await bot.send_message(msg.from_user.id, '✅ На странице:  ' + str(page_title) + ' ' + link + ' ИЗМЕНЕНИЙ НЕТ')
            else:

                # hd = HtmlDiff()
                # loads = ''
                # with open('source/html/Schedule/G_rasp.html','r', encoding='UTF-8') as load:
                #     loads = load.readlines()
                #     load.close()
                
                # mems = ''
                # with open(src_file, 'r', encoding='UTF-8') as mem:
                #     mems = mem.readlines()
                #     mem.close()

                # with open('source/html/Schedule/differents/differnt.html','a+', encoding='UTF-8') as fo:
                #     fo.write(hd.make_file(loads,mems))
                #     fo.close()

                d = Differ()
                difference = list(d.compare(last_rasp, now_rasp))
                difference = ''.join(difference)
                difference = difference.replace(' ', '')
                difference = difference.replace('-', '📍')
                difference = difference.replace('+', '📌')
                await bot.send_message(msg.from_user.id, '⚠️ На странице:  ' + str(page_title) + ' ' + link + '  ЕСТЬ ИЗМЕНЕНИЯ: ')
                for x in range(0, len(difference), MESS_MAX_LENGTH):
                    mess = difference[x: x + MESS_MAX_LENGTH]
                    await bot.send_message(msg.from_user.id, mess)
            
            file = open(src_file, 'w', encoding='UTF-8')
            file.write(new_rasp_str)
            file.close()



if __name__ == '__main__':
    executor.start_polling(dp)


