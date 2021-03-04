import telebot
import config
from telebot import types
import requests
import re

bot= telebot.TeleBot(config.config['telegram_token'])
@bot.message_handler(commands=['exchange'])
def user_exchange(message):
    # rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg = bot.send_message(message.chat.id, 'якщо ти дуже розумний і хочеш випробувати усі мої супер здібності, тобі сюди..')
    # bot.register_next_step_handler(msg, currency_exchange)

@bot.message_handler(commands=['start'])
def start_user(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rmk.add(types.KeyboardButton('Погода'),types.KeyboardButton('Курс валют'))
    msg = bot.send_message(message.chat.id, 'Я супер бот, вмію робити багато крутих штук, тому не тягни кота за яйц... хвіст і тицьни кнопку телепню..якщо ти дурень і не розумієш, що відбувається, то йди гуляй. Дурням допоможе /help',reply_markup=rmk)
    bot.register_next_step_handler(msg, user_answer)

@bot.message_handler(commands=['help'])
def help_user(message):
    rmk = types.InlineKeyboardMarkup()
    rmk.add(types.InlineKeyboardButton('Повідомлення до творця ', url= 'telegram.me/Rostishka13'))
    bot.send_message(message.chat.id, 'ок, курс молодого бійця.\n Команда /start - розпочинає головний функціонал бота. Далі сам розберешся\n Команда /help - видодить деяку допоміжну інформацію, так сказати для дебілів \n Команда /history - показує історію переписок з коханкою',
        reply_markup=rmk)
def user_exchange(message):
    # rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(message.chat.id, 'якщо ти дуже розумний і хочеш випробувати усі мої супер здібності...')

def user_answer(message):
    if message.text == 'Курс валют':
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        rmk.add(types.KeyboardButton('Список'), types.KeyboardButton('Калькулятор'))
        msg = bot.send_message(message.chat.id,'Володарю, що бажаєш зробити?',
                               reply_markup=rmk)
        bot.register_next_step_handler(msg, user_finally_answer)
    elif message.text == 'Погода':
        msg = bot.send_message(message.chat.id, 'Ще погоду тобі подавай, падло...Напиши мені своє місце проживання')
        bot.register_next_step_handler(msg, user_weather)
    # else:
    #     bot.send_message(message.chat.id, 'я такого ще не вмію, йди звідси..')
def user_finally_answer(message):
    if message.text == 'Список':
        msg = bot.send_message(message.chat.id, 'Який курс, я шо тобі обмінник якийсь чи що?!!!? Введи валюту вже..чекаю ж (USD, PLN, CAD....)')
        bot.register_next_step_handler(msg, user_currency)
    elif message.text == 'Калькулятор':
        msg = bot.send_message(message.chat.id,
                               'рахую вже, не псіхуй')
        bot.register_next_step_handler(msg, currency_calc)

def currency_calc(message):
    user_msg = message.text.upper()
    number = int(re.findall(r'\d+',user_msg)[0])
    currency = re.findall(r'[a-zA-Z]{3,}', user_msg)
    currency_range = requests.get('https://api.exchangeratesapi.io/latest').json()['rates']
    try:
        bot.send_message(message.chat.id, f' якщо перевести {number} одиниць {currency[0]}  в {currency[1]} вийде: {round(number*currency_range[currency[1]],2)} ')
        print(f' якщо перевести {number} одиниць {currency[0]} вийде {number*currency_range[currency[1]]} ')
    except:
        bot.send_message(message.chat.id, 'воу-воу, тримай себе в руках. Я такої валюти ще не чув')

def user_currency(message):
    currency = message.text.upper()
    try:
        resp = requests.get(f'https://api.exchangeratesapi.io/latest?base={currency}&symbols=USD,EUR,GBP,PLN,JPY,RUB').json()
        for key, value in resp['rates'].items():
            bot.send_message(message.chat.id, f' {currency} --> {key}: {round(value,2)}  ')
    except:
        bot.send_message(message.chat.id, f'Телепню, такої валюти як {currency} не існує....')

def user_weather(message):
    city = message.text.lower()
    try:
        params = {'APPID': config.config['weather_token'], 'q': city, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(config.config['url_weather'], params=params)
        weather = result.json()
        bot.send_message(message.chat.id, "В місці " + str(weather["name"]) + " температура " + str(
            float(weather["main"]['temp'])) + "\n" +
                         "Максимальна температура " + str(float(weather['main']['temp_max'])) + "\n" +
                         "Мінімальна температура " + str(float(weather['main']['temp_min'])) + "\n" +
                         "Швидкість вітру " + str(float(weather['wind']['speed'])) + "\n" +
                         "Тиск " + str(float(weather['main']['pressure'])) + "\n" +
                         "Вологість " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "Видимість " + str(weather['visibility']) + "\n")
    except:
        bot.send_message(message.chat.id, 'Трясця, ти в якій жопі живеш, синоптик юа не бачить твого міста...')
bot.polling(none_stop=True, interval=0)



