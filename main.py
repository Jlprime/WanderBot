import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice

TELE_API_KEY = '5092859318:AAFYord3EFu5J8iLgAUu6LXL3v6ZBkwS6_0'
GG_API_KEY = 'AIzaSyCu7LN_TJzsVQMbf5kVAh_6HDCfyntTMoE'

bot = telebot.TeleBot(TELE_API_KEY)

bot.set_my_commands([
    BotCommand('start','Initialises the bot')
    BotCommand('a')
    ])
