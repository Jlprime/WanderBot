import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice

TELE_API_KEY = '5092859318:AAFYord3EFu5J8iLgAUu6LXL3v6ZBkwS6_0'
GG_API_KEY = 'AIzaSyCu7LN_TJzsVQMbf5kVAh_6HDCfyntTMoE'

bot = telebot.TeleBot(TELE_API_KEY)

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places near you!')])

@bot.message_handler(commands=['start'])
def start(message):
  """
  Command that welcomes the user and configures the initial setup
  """

  chat_id = message.chat.id

  if message.chat.type == 'private':
    chat_user = message.chat.first_name
  else:
    chat_user = message.chat.title
  
  message_text = f'Hi {chat_user}'

  bot.reply_to(message, message_text)