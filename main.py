import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice

TELE_API_KEY = '5092859318:AAFYord3EFu5J8iLgAUu6LXL3v6ZBkwS6_0'
GG_API_KEY = 'AIzaSyCu7LN_TJzsVQMbf5kVAh_6HDCfyntTMoE'

bot = telebot.TeleBot(TELE_API_KEY)

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places near you!'),
    BotCommand('search','Search by city')
    ])

@bot.message_handler(commands=['start'])
def start(message):
  """
  Command that welcomes the user and configures the initial setup
  """

  message_text = "Hi"
  print('Received message:', message_text)

  bot.reply_to(message, message.text)


@bot.message_handler(commands=['search'])
def search():
    pass

bot.infinity_polling()