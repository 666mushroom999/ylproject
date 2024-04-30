import asyncio
import random
from datetime import datetime

import requests

from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram import F, Router

router = Router()

kompl = ['Не грусти, солнышко', 'Кто грустит тот трансвестит']
veryfun = ['''Режиссер возвращается домой пьяный и орет:
— Так быстро таз, я буду блевать!
Жена приносит таз.
Режиссер:
— Все унесите, концепция поменялась я укакался.''',
           '''Встречаются двое друзей:
— Привет! Что такой грустный?
Зуб болит!
— Так сходи к стоматологу!
Да боюсь я их!
— Ну, тогда иди на станцию, привяжи нитку к зубу и к поезду.
Поезд дернет, и нормально!
Через пару дней встречаются опять:
— Ну, как дела? Как зуб?
Сесть стук оторвал!
— Шесть зубов?!
Не! Сесть вагонов! А субы мне все масынист повыбивал!''',
           '''Наезжает начальник тюрьмы на надзирателя:
           — Как это так получилось, что у тебя из десятой камеры зек сбежал?
           Тот почесываясь говорит.
           Да так вот и сбежал. Двери отпер.
           — Чем же он их отпер?
           Ясное дело, ключом.
           — А ключ у него откуда?
           Да мой это ключ!
           — Украл он его у тебя?
           Не, он не вор! Он его честно в карты выиграл!
           
           ''']
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
star = []
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
clava = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мне грустно')],
    [KeyboardButton(text='Мне очень грустно'), KeyboardButton(text='Мне оооооочень грустно')],
], resize_keyboard=True, input_field_placeholder='Выберите команду')
logger = logging.getLogger(__name__)
count = 0


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.username}, тебе грустно?', reply_markup=clava)


@dp.message(F.text == 'Мне грустно')
async def weather(message: Message):
    await message.answer(random.choice(kompl))


@dp.message(F.text == 'Мне очень грустно')
async def help(message: Message):
    await message.answer(f'Смех - лучший способ справляться с грустью, лови шутейку: \n {random.choice(veryfun)}')


@dp.message(F.text == 'Мне оооооочень грустно')
async def l(message: Message):
    await message.answer(f'''Солнышко, если тебе прям очень грустно, то я думаю лучше тебе поговорить со специалистами.
Позвони по номеру: 8-800-2000-122 Это бесплатно и тебе точно помогут)''')


@dp.message(Command('w'))
async def tr(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    if len(command.args.split()):
        name_country = ''.join(command.args.split())
    if len(command.args.split()) > 1:
        name_country = ' '.join(command.args.split())
    smiles = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }
    try:
        re = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={name_country}&appid={name_country}&units=metric"
        )
        data = re.json()
        real_temp = round(data['main']['temp'])
        feel_temp = round(data['main']['feels_like'])
        now_time = str(datetime.now())[:19]
        country = data['sys']['country']
        sunrise = (str(datetime.fromtimestamp(data['sys']['sunrise'])))[11:]
        sunset = (str(datetime.fromtimestamp(data['sys']['sunset'])))[11:]
        wind = data['wind']['speed']
        if real_temp > 0:
            real_temp = f'+{real_temp}'
        if feel_temp > 0:
            feel_temp = f'+{feel_temp}'
        main_weather = data['weather'][0]['main']
        if main_weather in smiles:
            wsmile = smiles[main_weather]
        else:
            wsmile = 'Нипон'
        await message.answer(f"***{now_time}*** \n"
                             f"Город:{name_country} Страна:{country} \n"
                             f"Погода: {wsmile} \n"
                             f"Температура воздуха: {real_temp}°С \n"
                             f"Ощущается как: {feel_temp}°С \n"
                             f"Время рассвета: {sunrise} \n"
                             f"Время заката: {sunset} \n"
                             f"Скорость ветра: {wind} м/c \n"
                             f"Хорошего дня! 🥰"
                             )
    except:
        await message.answer('Вы ввели несуществующий город')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
