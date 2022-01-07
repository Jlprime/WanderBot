import telebot
import config
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from cardclass import cardClass
from reversegeo import reverse_geocoder

bot = telebot.TeleBot(config.TELE_API_KEY)

user_info = dict()
user_location = dict()

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places to go near you'),
    BotCommand('search','Find places at a specified city')
    ])

@bot.message_handler(commands=['start'])
def start(message):
    """
    Initialising the bot
    """

    chat_id = message.chat.id
    user_info['chat_id'] = chat_id
    
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
        user_info['chat_name'] = chat_user
    else:
        bot.send_message(chat_id=chat_id,text='Please use this bot in a private chat!')
  
    welcome_text = f'Hello {chat_user}, welcome to WanderBot!'
    bot.send_message(chat_id=chat_id,text=welcome_text)

    button_text = 'What would you like to do?'

    buttons = []
    buttons.append(InlineKeyboardButton('Wander',callback_data='wander'))
    buttons.append(InlineKeyboardButton('Search',callback_data='search'))
    reply_markup = InlineKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

    return

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  """
  Handles callback queries to execute their respective functions
  """

  action = call.data
  
  if action == 'wander':
      bot.answer_callback_query(call.id)
      wander(call.message)
      return

  if action == 'search':
      bot.answer_callback_query(call.id)
      search(call.message)
      return
  
  return

@bot.message_handler(commands=['config'])
def set_user_location(message):
    chat_id = message.chat.id

    keyboard = ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True)
    loc_button = KeyboardButton(
        text='Tap me!',
        request_location=True)
    keyboard.add(loc_button)

    asking_msg = bot.send_message(chat_id=chat_id,text='Please share with us your location!',reply_markup=keyboard)

    bot.register_next_step_handler(asking_msg,detect_location)

    return 

def detect_location(message):
    chat_id = message.chat.id

    latitude = message.location.latitude
    longitude = message.location.longitude

    user_location['latitude'] = latitude
    user_location['longitude'] = longitude

    location_text = f'Your location is {latitude}, {longitude}.\nPlease hold while we provide you with your itinerary...'

    bot.send_message(chat_id=chat_id,text=location_text)
    wander(message)

    return


def extract_location(message):
    pass

@bot.message_handler(commands=['wander'])
def wander(message):
    if not user_location:
        set_user_location(message)
        return
    
    chat_id = message.chat.id
    lat = user_location['latitude']
    long = user_location['longitude']
    rad = 5000

    
    chat_user = user_info['chat_name']
    city = reverse_geocoder(str(lat),str(long))
    curr_card = cardClass(lat,long,rad)
    weather = curr_card.weather

    intro_msg = f'Hello {chat_user}, here\'s your itinerary for a day in {city}.\nCurrently, the weather is:\n{weather}'
    bot.send_message(chat_id=chat_id,text=intro_msg)
    inter_msg = 'Here are the recommended places to dine and visit:'
    bot.send_message(chat_id=chat_id,text=inter_msg)
    bot.send_venue(
        chat_id=chat_id,
        latitude=curr_card.eatPlace['geometry']['location']['lat'],
        longitude=curr_card.eatPlace['geometry']['location']['lng'],
        title='EATERY'+curr_card.eatPlace['name'],
        address=curr_card.eatPlace['vicinity'],
        google_place_id=curr_card.eatPlace['place_id'])

    return

@bot.message_handler(commands=['search'])
def search(message):
    pass

bot.infinity_polling()