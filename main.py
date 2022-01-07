import telebot
import config
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

bot = telebot.TeleBot(config.TELE_API_KEY)

user_info = dict()

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places to go near you'),
    BotCommand('search','Find places at a specified city')
    ])

@bot.message_handler(commands=['start'])
def start(message):
    """
    Welcome message
    """

    chat_id = message.chat.id
    
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
    else:
        chat_user = message.chat.title
  
    welcome_text = f'Hi {chat_user}, welcome to WanderBot!'
    bot.send_message(chat_id=chat_id,text=welcome_text)

    button_text = 'What would you like to do?'

    buttons = []
    buttons.append(InlineKeyboardButton('Wander',callback_data='1'))
    buttons.append(InlineKeyboardButton('Search',callback_data='2'))
    reply_markup = InlineKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

    return

def set_user_location(message):
    keyboard = ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True)
    loc_button = KeyboardButton(
        text='Tap me!',
        request_location=True)
    keyboard.add(loc_button)

    bot.send_message(message.chat.id, 'Please share with us your location!',reply_markup=keyboard)

    return 

@bot.message_handler(content_types=['location'])
def extract_location(message):

    chat_id = message.chat.id

    user_info['latitude'] = message.location.latitude
    user_info['longitude'] = message.location.longitude

    location_text = f"Your location is {user_info['latitude']}, {user_info['longitude']}"

    bot.send_message(chat_id=chat_id,text=location_text)

    return

@bot.message_handler(commands=['wander'])
def wander():
    pass

@bot.message_handler(commands=['search'])
def search():
    pass

bot.infinity_polling()

