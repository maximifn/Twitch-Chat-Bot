# -*- coding: utf-8 -*-
import json,requests,sqlite3
from config import *
from time import sleep
import telebot

bot = telebot.TeleBot(TOKEN)

def bd_update(status):
    conn = sqlite3.connect('arthas_status.db')
    USER_BD = "'" + USER + "'"
    conn.execute("UPDATE STREAM set status_stream = "+status+" where streamer ="+USER_BD)
    conn.commit()
    print("[R_BOT]: Успешно внес изменения в БД")
    return True



def bd_check():
    conn = sqlite3.connect('arthas_status.db')
    cursor = conn.execute("SELECT streamer, status_stream  FROM STREAM")
    print("[R_BOT]: Успешно подключился к БД")

    for row in cursor:
        user = row[0]
        status_stream = row[1]
        return user, status_stream


def sendMessage(chatid):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на твитч", url="https://go.twitch.tv/arthas")
    keyboard.add(url_button)
    bot.send_message(chatid, "Arthas запустил поток, бегом на стрим.", reply_markup=keyboard)


def collectIds():
    conn = sqlite3.connect('arthas_status.db', check_same_thread=False)
    cursor = conn.execute("SELECT chatid FROM users")
    array_ids = []
    for row in cursor:
        array_ids.append(row[0])
    return array_ids


def massSending():
    ids = collectIds()
    for id in ids:
        sendMessage(id)


def connect():
    url = "https://api.twitch.tv/kraken/streams/" + USER + "?client_id=" + CLIENT_ID
    request = requests.get(url)
    status_req = request.status_code
    return status_req, request.json()


def mainTwitch():
    try:
        my_request = connect()
        status_req = my_request[0]
        status = my_request[1]['stream']
        if status is None:
            status = 0
        elif status['stream_type'] == 'live':
            status = 1
        else:
            status = 0
        params = bd_check()
        if status == params[1]:
            print("[R_BOT]: Статус стрима не изменился, ничего не делаю")
        else:
            print("[R_BOT]: Статус стрима изменился, ниачинаю вносить изменения в бд")
            if status_req == 200:
                print('[R_BOT]: Соединение успешно установленно')
                reading = my_request[1]['stream']
                if reading is None:
                    print('[R_BOT]: Стрим ' + USER + ' оффлайн')
                    status = '0'
                    bd_update(status)
                    return status
                else:
                    checkOnline = reading['stream_type']
                    if checkOnline == 'live':
                        status = '1'
                        bd_update(status)
                        print('[R_BOT]: Стрим ' + USER + ' онлайн, отправляю в телеграм')
                        massSending()
                        print('[R_BOT]: Разослал всем и кайфую')
                        return status
            else:
                print('[R_BOT]: Не удалось установить соединение c Twitch Api, попробую чуть позже.')
    except Exception as e:
        print(e)



def mainFunc():
        mainTwitch()
        sleep(10)

while(True):
    mainFunc()