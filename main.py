import telebot
import config
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from cardclass import cardClass
from cardclasssearch import cardClassSearch
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
    
    if message.chat.type == 'private':
        chat_user = message.chat.first_name
        if not user_info:
            user_info['chat_name'] = chat_user
            welcome_text = f'Hello {chat_user}, welcome to WanderBot!'
            bot.send_message(chat_id=chat_id,text=welcome_text)
    else:
        bot.send_message(chat_id=chat_id,text='Please use this bot in a private chat!')

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
    if action == 'config':
        bot.answer_callback_query(call.id)
        config(call.message)
        return
    
    if action == 'setloc':
        bot.answer_callback_query(call.id)
        set_user_location(call.message)
        return
    
    if action == 'setrad':
        bot.answer_callback_query(call.id)
        set_user_radius(call.message)
        return

    return

@bot.message_handler(commands=['config'])
def config(message):
    '''
    Handles bot settings
    '''
    chat_id = message.chat.id

    button_text = 'Settings'
    buttons = []
    buttons.append(InlineKeyboardButton('Set your location',callback_data='setloc'))
    buttons.append(InlineKeyboardButton('Change search radius',callback_data='setrad'))
    reply_markup = InlineKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

    return

def set_user_radius(message):
    chat_id = message.chat.id
    rad_msg = 'Please enter a radius you would like the search to be within (in km, between 5 - 50).'
    rad_msg_sent = bot.send_message(chat_id=chat_id,text=rad_msg)
    bot.register_next_step_handler(rad_msg_sent, detect_radius)

    return

def detect_radius(message):
    chat_id = message.chat.id
    rad = message.text
    try:
        rad = int(rad)
        if rad < 5 or rad > 50:
            bound_msg = 'The radius is out of bounds! Please type a number between 5 - 50.'
            bound_msg_sent = bot.send_message(chat_id=chat_id,text=bound_msg)
            bot.register_next_step_handler(bound_msg_sent, detect_radius)
            return
        user_location['radius'] = rad
        success_msg = 'Radius successfully set.'
        bot.send_message(chat_id=chat_id,text=success_msg)
        start(message)
    except ValueError:
        error_msg = 'The value you entered was not a number. Please try again.'
        error_msg_sent = bot.send_message(chat_id=chat_id,text=error_msg)
        bot.register_next_step_handler(error_msg_sent, detect_radius)
    
    return

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

    loc_msg = 'Please share with us your location!'
    loc_msg_sent = bot.send_message(chat_id=chat_id,text=loc_msg,reply_markup=keyboard)
    bot.register_next_step_handler(loc_msg_sent,detect_location)

    return 

def detect_location(message):
    first_call = not user_location

    chat_id = message.chat.id

    latitude = message.location.latitude
    longitude = message.location.longitude

    user_location['latitude'] = latitude
    user_location['longitude'] = longitude

    location_text = f'Your location is {latitude}, {longitude}.'
    bot.send_message(chat_id=chat_id,text=location_text)

    if first_call:
        user_location['radius'] = 5000
        first_call_msg = 'Please hold while we provide you with your itinerary...'
        bot.send_message(chat_id=chat_id,text=first_call_msg)
        bot.send_chat_action(chat_id=chat_id,action='typing')
        wander(message)

    return

@bot.message_handler(commands=['wander'])
def wander(message):
    if not user_location:
        set_user_location(message)
        return
    
    chat_id = message.chat.id
    lat = user_location['latitude']
    long = user_location['longitude']
    rad = user_location['radius']

    chat_user = user_info['chat_name']
    city = reverse_geocoder(str(lat),str(long))
    curr_card = cardClass(lat,long,rad)
    
    itinerary(chat_id,chat_user,city,curr_card,'wander')
    post_itinerary(chat_id)

    return

def itinerary(chat_id,chat_user,city,curr_card,caller):
    city = city.title()
    weather = curr_card.weather
    eat_place = curr_card.eatPlace
    visit_place = curr_card.visitPlace
    placelist = [eat_place, visit_place]
    placename = ['dining','visiting']

    intro_msg = f'Hello {chat_user}, here\'s your itinerary for a day in {city}.\nCurrently, the weather is:\n{weather}'

    bot.send_message(chat_id=chat_id,text=intro_msg)
    for idx, place in enumerate(placelist):
        if place:
            bot.send_venue(
            chat_id=chat_id,
            latitude=place['geometry']['location']['lat'],
            longitude=place['geometry']['location']['lng'],
            title=place['name'],
            address=place['vicinity'],
            google_place_id=place['place_id'])
        else:
            notfound_msg = f'It seems like we couldn\'t find any spots for {placename[idx]}. You can reroll to try again.'
            bot.send_message(chat_id=chat_id,text=notfound_msg)

def post_itinerary(chat_id):
    button_text = 'What would you like to do?'
    row_one, row_two = [], []
    row_one.append(InlineKeyboardButton('Change search radius',callback_data='setrad'))
    row_two.append(InlineKeyboardButton('Reroll',callback_data='wander'))
    row_two.append(InlineKeyboardButton('Search',callback_data='search'))
    reply_markup = InlineKeyboardMarkup([row_one,row_two])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

@bot.message_handler(commands=['search'])
def search(message):
    chat_id = message.chat.id
    search_msg = 'Which city do you wish to search in?'
    search_msg_sent = bot.send_message(chat_id=chat_id,text=search_msg)
    bot.register_next_step_handler(search_msg_sent,get_city)

def get_city(message):
    chat_id = message.chat.id
    chat_user = user_info['chat_name']
    city = str(message.text).lower()
    curr_card = cardClassSearch(city)

    if not curr_card.eatPlace and not curr_card.visitPlace:
        invalid_msg = 'No places were found. You might have typed the place name wrongly. Please try a valid city name, or wander within your own city >_<'
        bot.send_message(chat_id,text=invalid_msg)
        post_itinerary(chat_id)
        return
    itinerary(chat_id,chat_user,city,curr_card,'search')
    post_itinerary(chat_id)

bot.infinity_polling()