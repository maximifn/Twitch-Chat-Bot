# -*- coding: utf-8 -*-
import datetime
import sqlite3
import telebot
from config import *

conn = sqlite3.connect('arthas_status.db', check_same_thread=False)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def add_user_to_base(message):
    id_user = message.chat.id
    date = datetime.date.today()
    cursor = conn.execute("SELECT chatid FROM users WHERE chatid = "+str(id_user))
    dublicate_counter = 0
    for row in cursor:
        dublicate_counter += 1
    if dublicate_counter > 0:
        isDub = True
    else:
        isDub = False
    if isDub == 1:
        bot.send_message(id_user, 'Вы уже в базе данных, нахуя вы ломитесь?')
    else:
        bot.send_message(message.chat.id, 'RoflanEbalo, когда Arthas запустит поток, я тебя оповещу.')
        conn.execute("INSERT INTO users VALUES(" + str(id_user) + "," + str(date) + ")")
        conn.commit()






if __name__ == '__main__':
    bot.polling(none_stop=True)