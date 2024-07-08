from asyncio import run

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import requests
from bs4 import BeautifulSoup as BS


t = requests.get('https://sinoptik.ua/погода-ташкент')
html_t = BS(t.content, 'html.parser')

for el in html_t.select('#content'):
    min = el.select('.temperature .min')[0].text
    max = el.select('.temperature .max')[0].text
    t_min = min[4:]
    t_max = max[5:]
    print(t_min, t_max)
    print(min, max)


def city():
    return [
        [InlineKeyboardButton("Tashkent", callback_data=f"01")]
    ]


def back():
    return [
        InlineKeyboardButton("Orqaga", callback_data=f"back")
    ]


def inline_hendlerlar(update, context):
    query = update.callback_query
    data = query.data.split("_")

    if data[0] == "01":
        query.message.edit_text(f"BUgun Toshkent shahrida ob-havo o'zgarib turadi min {t_min}\n max {t_max}\n bo'lishi kutilmoqda", reply_markup=InlineKeyboardMarkup(back()))
    elif data[0] == 'back1':
        query.message.edit_text(f"Bu yerdan shahr yoki villoyatni tanla", reply_markup=InlineKeyboardMarkup(city()))


def start(update, context):
    user = update.message.from_user
    update.message.reply_trext(f"""Salom {user.first_name} \nBu yerdan Shahar """)


def main():
    Token = "6494683170:AAHejVExCp1lHzJZHI0JPkvvXE1tfeJPq0o"
    updater = Updater(Token, True)
    updater.dispacher.and_handler(CommandHandler("start", start()))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()