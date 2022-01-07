import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from geolocation import location

TELE_API_KEY = '5092859318:AAFYord3EFu5J8iLgAUu6LXL3v6ZBkwS6_0'
GG_API_KEY = 'AIzaSyCu7LN_TJzsVQMbf5kVAh_6HDCfyntTMoE'

bot = telebot.TeleBot(TELE_API_KEY)

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places to go near you'),
    BotCommand('search','Find places at a specified city')
    ])

@bot.message_handler(commands=['start'])
def start(message):
    """
    Welcome message
    Pinpoint user location
    """

    chat_id = message.chat.id
    
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
    else:
        chat_user = message.chat.title
  
    welcome_text = f'Hi {chat_user}, welcome to WanderBot!'
    user_loc = location()
    location_text = f'Your location is {user_loc}'
    button_text = 'What would you like to do?'

    wanderButton = InlineKeyboardButton('Wander',callback_data='goto wander')
    searchButton = InlineKeyboardButton('Search',callback_data='goto search')

    bot.send_message(chat_id=chat_id,text=welcome_text)
    bot.send_message(chat_id=chat_id,text=location_text)

@bot.message_handler(commands=['wander'])
def wander():
    pass

@bot.message_handler(commands=['search'])
def search():
    pass

bot.infinity_polling()