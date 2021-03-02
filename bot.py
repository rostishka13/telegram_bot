import telebot
import config
from telebot import types
import requests

bot= telebot.TeleBot(config.config['telegram_token'])
@bot.message_handler(commands=['start'])
def start_user(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rmk.add(types.KeyboardButton('Погода'),types.KeyboardButton('Курс валют'))
    msg = bot.send_message(message.chat.id, 'Я супер бот, вмію робити багато крутих штук, тому не тягни кота за яйц... хвіст і тицьни кнопку телепню..',reply_markup=rmk)
    bot.register_next_step_handler(msg, user_answer)

def user_answer(message):
    if message.text == 'Курс валют':
        msg = bot.send_message(message.chat.id, 'Який курс, я шо тобі обмінник якийсь чи що?!!!? Введи валюту вже..чекаю ж')
        bot.register_next_step_handler(msg, user_currency)
    elif message.text == 'Погода':
        msg = bot.send_message(message.chat.id, 'Ще погоду тобі подавай, падло...Напиши мені своє місце проживання')
        bot.register_next_step_handler(msg, user_weather)
    else:
        bot.send_message(message.chat.id, 'я такого ще не вмію, йди звідси..')


def user_currency(message):
    currency = message.text.upper()
    try:

        resp = requests.get(f'https://api.exchangeratesapi.io/latest?base={currency}&symbols=USD,EUR,GBP,PLN,JPY,RUB').json()
        for key, value in resp['rates'].items():
            bot.send_message(message.chat.id, f' {currency} --> {key}: {round(value,2)}  ')


    except:
            # bot.register_next_step_handler('Телепню, такої валюти як {currency} не існує....', user_currency)
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




@bot.message_handler(commands=['help'])
def help_user(message):
    pass
bot.polling(none_stop=True, interval=0)



# @bot.message_handler(commands=['application'])
# def application(message):
#     rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     rmk.add(types.KeyboardButton('yes'), types.KeyboardButton('no'))
#     msg = bot.send_message(message.chat.id, 'would you like to register', reply_markup=rmk)
#     bot.register_next_step_handler(msg, user_answer)
#
# def user_answer(message):
#     if message.text == 'yes':
#         msg = bot.send_message(message.chat.id, 'Введіть дані')
#
#         bot.register_next_step_handler(msg, user_req)
#
#     elif message.text == 'no':
#         bot.send_message(message.chat.id, 'good, fuck off')
#     else:
#         bot.send_message(message.chat.id, 'lol')
#
#
# def user_req(message):
#     bot.send_message(message.chat.id, message.text)

# @client.message_handler(commands=['start'])
# def get_user_info(message):
#     markup_inline = types.InlineKeyboardMarkup()
#     item_currency = types.InlineKeyboardButton(text='Курс валют', callback_data='currency')
#     item_weather = types.InlineKeyboardButton(text = 'Погоду', callback_data='weather')
#     markup_inline.add(item_weather, item_currency)
#     client.send_message(message.chat.id, 'Я супер бот, що бажаєте дізнатися?',reply_markup=markup_inline)
# @client.callback_query_handler(func = lambda call: True)
# def get_answer(call):
#     if call.data == 'currency':
#
#         # client.send_message(call.message.chat.id, 'input some currency')
#         markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)  # цей параметр робить нашу клавіатуру меншою
#         Main_list = types.KeyboardButton('Main list')
#         Full_list = types.KeyboardButton('Full list')
#         markup_reply.add(Main_list, Full_list)
#         client.send_message(call.message.chat.id, 'Натисніть на одну з кнопок',
#                                  reply_markup=markup_reply)
#
#     elif call.data == 'weather':
#         pass
#
# @client.message_handler(content_types=['text'])
# def get_text(message):
#     if message.text == 'Main list':
#         response = requests.get(f'https://api.exchangeratesapi.io/latest?base=USD&symbols=USD,EUR,GBP,PLN,JPY,RUB').json()
#         for key, value in response['rates'].items():
#             client.send_message(message.chat.id, f' USD -->{key}: {round(value,2)}')
#
#     elif message.text =='Full list':
#         response = requests.get('https://api.exchangeratesapi.io/latest?base=USD').json()
#         for key, value in response['rates'].items():
#             client.send_message(message.chat.id, f' USD -->{key}: {round(value,2)}')

# # @client.message_handler(commands=['start'])
# def get_user_info(message):
#     markup_inline = types.InlineKeyboardMarkup()
#     item_currency = types.InlineKeyboardButton(text = 'Курс валют', callback_data= 'currency')
#     item_weather = types.InlineKeyboardButton(text = 'Погоду', callback_data='weather')
#     markup_inline.add(item_weather, item_currency)
#     client.send_message(message.chat.id, 'Я супер бот, що бажаєте дізнатися?',reply_markup=
#                         markup_inline)
# # створюємо функцію, що обробляє запит
# @client.callback_query_handler(func= lambda call: True)
# def answer(call):
#     if call.data == 'currency':
#         #створюємо клавіатуру
#
#         markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True) # цей параметр робить нашу клавіатуру меншою
#         item_EUR = types.KeyboardButton('EUR')
#         item_USD = types.KeyboardButton('USD')
#         markup_reply.add(item_EUR, item_USD)
#         client.send_message(call.message.chat.id, 'Натисніть на одну з кнопок, або введіть валюту',
#                             reply_markup=markup_reply)
#     elif call.data == 'weather':
#
#          markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
#          Current_weather_data = types.KeyboardButton('Current Weather')
#          Weather_forecast_data = types.KeyboardButton(' Daily Forecast 16 days')
#          markup_reply.add(Current_weather_data, Weather_forecast_data)
#          client.send_message(call.message.chat.id, 'Натисніть на одну з кнопок',
#                              reply_markup=markup_reply)
#
# @client.message_handler(content_types=['text'])
# def get_text(message):
#     # try:
#     #     client.send_message(message.chat.id, 'Введи валюту....:')
#     #     currency_name  = message.text.upper()
#     #     response = requests.get(f'https://api.exchangeratesapi.io/latest?base={currency_name}&symbols=USD,EUR,GBP,PLN,JPY,RUB').json()
#     #     for key, value in response['rates']:
#     #         client.send_message(message.chat.id, f'{currency_name} -> {key}: {round(value,2)}')
#     # except:
#     #     client.send_message(message.chat.id, 'Такої валюти не існує, мудак')
#
#     if message.text == 'EUR':
#         response = requests.get(f'https://api.exchangeratesapi.io/latest?base=EUR').json()['rates']
#         for key, value in response.items():
#             client.send_message(message.chat.id, f' {key} -> EUR: {round(value,2)}')
#     elif message.text == 'USD':
#         response = requests.get(f'https://api.exchangeratesapi.io/latest?base=USD').json()['rates']
#         for key, value in response.items():
#             client.send_message(message.chat.id, f' {key} -> USD: {round(value,2)}')
#     elif message.text == 'Current Weather':
#         params = {'APPID': config.config['weather_token'], 'q': config.config['city_name'], 'units': 'metric', 'lang': 'ru'}
#         result = requests.get(config.config['url_weather'], params=params)
#         weather = result.json()
#         client.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(
#             float(weather["main"]['temp'])) + "\n" +
#                          "Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
#                          "Минимальная температура " + str(float(weather['main']['temp_min'])) + "\n" +
#                          "Скорость ветра " + str(float(weather['wind']['speed'])) + "\n" +
#                          "Давление " + str(float(weather['main']['pressure'])) + "\n" +
#                          "Влажность " + str(int(weather['main']['humidity'])) + "%" + "\n" +
#                          "Видимость " + str(weather['visibility']) + "\n" +
#                          "Описание " + str(weather['weather'][0]["description"]) + "\n\n" )
#     elif message.text == 'Daily Forecast 16 days':
#         pass
#
#
#
# client.polling(none_stop = True, interval = 0)
