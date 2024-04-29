import datetime
import logging
import sqlite3

from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import TOKEN
from dad import pas

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

orderslst = []


def validate_time(alarm_time):
    if len(alarm_time) != 6:
        return "Неверный формат, попробуйте снова"
    else:
        if int(alarm_time[0:2]) > 23:
            return "Неверный формат часов, попробуйте снова"
        elif int(alarm_time[3:5]) > 59:
            return "Неверный формат минут, попробуйте снова"
        else:
            return "Верно"


admin = False


async def echo(update, context):
    global admin
    if update.message.text == pas:
        admin = True


async def start(update, context):
    await update.message.reply_text(f'Привет, я бот помощи в покупке телефона!')


async def listt(update, context):
    con = sqlite3.connect("base.sqlite")
    cur = con.cursor()
    sqlite_select_query = """SELECT * from list"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    for row in records:
        update.message.reply_text(f"""Телефон:{row[1]}
        Память: {row[2]}
        Описание: {row[3]}
        Стоимость: {row[4]}""")
    con.commit()
    con.close()


async def help(update, context):
    await update.message.reply_text(f'Задайте вопрос администратору: @mushroom666')


async def makeanorder(update, context):
    await update.message.reply_text('Напишите время встречи в формате"HH:MM"')
    while True:
        # Запрашиваем время установки будильника
        alarm_time = update.message.text

        validate = validate_time(alarm_time)  # присваиваем результаты функции
        if validate != "Верно":
            print(validate)
        else:
            print(f"Вы договорились на {alarm_time}...")
            break

    orderslst.append((int(alarm_time[0:2]), int(alarm_time[3:5])))


async def orders(update, context):
    global admin
    if admin:
        while True:
            now = datetime.now()

            current_hour = now.hour  # Получение текущего часа
            current_min = now.minute  # Получение текущей минуты
            for i in len(orderslst):
                if orderslst[i][0] == current_hour:
                    if orderslst[i][1] == current_min:
                        update.message.reply_text("Встреча")
                        orderslst.pop(i)
                        break


def main():
    app = Application.builder().token(TOKEN).build()
    text_handle = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    app.add_handler(text_handle)
    app.add_handler(CommandHandler('Старт', start))
    app.add_handler(CommandHandler('Помощь', help))
    app.add_handler(CommandHandler('Каталог', listt))
    app.add_handler(CommandHandler('Сделать заказ', makeanorder))
    logger.info('Бот работает')
    app.run_polling()


main()
