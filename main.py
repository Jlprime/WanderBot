import os
from flask import Flask, request
import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
from cardclass import cardClass
from cardclasssearch import cardClassSearch
from reversegeo import reverse_geocoder
from retrievepics import retrievePics

TOKEN = os.getenv('TOKEN') 

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

user_info = dict()
user_location = dict()

bot.set_my_commands([
    BotCommand('start','Initialises the bot'),
    BotCommand('wander','Find places to go in your city'),
    BotCommand('search','Find places to go in another city'),
    BotCommand('config','Bot settings')
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
        welcome_msg = (
            f'Hello {chat_user}, welcome to WanderBot - a bot for the wanderlust of the indecisive!\n\n'
            '/wander - Find suggested places to go from your current location.\n'
            '/search - Find suggested places to go in any city.\n'
            '/config - Bot settings.\n\n'
            'What would you like to do?'
        )
        
        buttons = []
        buttons.append(InlineKeyboardButton('Wander',callback_data='wander'))
        buttons.append(InlineKeyboardButton('Search by City',callback_data='search'))
        reply_markup = InlineKeyboardMarkup([buttons])

        bot.send_message(chat_id=chat_id,text=welcome_msg,reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=chat_id,text='Please use this bot in a private chat!')
        return

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
        set_user_location(call.message,'config')
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
    if not ('chat_name' in user_info):
        bot.send_message(chat_id=chat_id,text='Please run /start first!')
        return
    
    if user_location.get('latitude') == None:
        curr_loc = 'Unknown'
    else:
        curr_loc = f"{user_location['longitude']}, {user_location['latitude']}"

    if user_location.get('radius') == None:
        curr_rad = 'Unknown'
    else:
        curr_rad = user_location['radius'] / 1000

    button_text = f"Settings\nYour current settings:\nLocation - {curr_loc}\nSearch Radius - {curr_rad} km"
    buttons = []
    buttons.append(InlineKeyboardButton('Set Your Location',callback_data='setloc'))
    buttons.append(InlineKeyboardButton('Change Search Radius',callback_data='setrad'))
    reply_markup = InlineKeyboardMarkup([buttons])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

    return

def set_user_radius(message):
    chat_id = message.chat.id
    if not ('chat_name' in user_info):
        bot.send_message(chat_id=chat_id,text='Please run /start first!')
        return

    rad_msg = 'Please enter a radius you would like the search to be within (in km, between 5 - 50).'
    rad_msg_sent = bot.send_message(chat_id=chat_id,text=rad_msg)
    bot.register_next_step_handler(rad_msg_sent, detect_radius)

    return

def detect_radius(message):
    chat_id = message.chat.id
    rad = message.text
    try:
        rad = round(float(rad))
        if rad < 5 or rad > 50:
            bound_msg = 'The radius is out of bounds! Please type a number between 5 - 50.'
            bound_msg_sent = bot.send_message(chat_id=chat_id,text=bound_msg)
            bot.register_next_step_handler(bound_msg_sent, detect_radius)
            return
        user_location['radius'] = rad * 1000
        success_msg = 'Radius successfully set.'
        bot.send_message(chat_id=chat_id,text=success_msg)
        start(message)
    except (ValueError, TypeError):
        error_msg = 'The value you entered was not a number. Please try again.'
        error_msg_sent = bot.send_message(chat_id=chat_id,text=error_msg)
        bot.register_next_step_handler(error_msg_sent, detect_radius)
    
    return

def set_user_location(message,caller):
    chat_id = message.chat.id
    if not ('chat_name' in user_info):
        bot.send_message(chat_id=chat_id,text='Please run /start first!')
        return

    loc_button = KeyboardButton(
        text='Tap me to share!',
        request_location=True)
    cancel_button = KeyboardButton(
        text='I do not wish to share.'
    )
    reply_markup = ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=True)
    reply_markup.add(loc_button,cancel_button)

    loc_msg = 'Please share with us your location - if you want to, of course!'
    loc_msg_sent = bot.send_message(chat_id=chat_id,text=loc_msg,reply_markup=reply_markup)
    bot.register_next_step_handler(loc_msg_sent,detect_location, caller)

    return 

def detect_location(message,caller):
    chat_id = message.chat.id

    if message.text == 'I do not wish to share.':
        bot.send_message(chat_id=chat_id,text='Understood.')
        return

    if message.location == None:
        error_msg = 'That was not a location. Please try again.'
        bot.send_message(chat_id=chat_id,text=error_msg)
        set_user_location(message,caller)
        return

    latitude = message.location.latitude
    longitude = message.location.longitude

    user_location['latitude'] = latitude
    user_location['longitude'] = longitude

    # location_text = f'Your location is {latitude}, {longitude}.'
    # bot.send_message(chat_id=chat_id,text=location_text)

    if caller == 'wander':
        wander(message)
        return
    if caller == 'config':
        bot.send_message(chat_id=chat_id,text='Done!')
        return
    
    return

@bot.message_handler(commands=['wander'])
def wander(message):
    if not user_location.get('latitude') or not user_location.get('longitude'):
        set_user_location(message,'wander')
        return
    
    user_location.setdefault('radius',5000)
    chat_id = message.chat.id
    bot.send_chat_action(chat_id=chat_id,action='typing')
    if not ('chat_name' in user_info):
        bot.send_message(chat_id=chat_id,text='Please run /start first!')
        return

    lat = user_location['latitude']
    long = user_location['longitude']
    rad = user_location['radius']
    chat_user = message.chat.first_name

    city = reverse_geocoder(str(lat),str(long))
    curr_card = cardClass(lat,long,rad)
    
    itinerary(chat_id,chat_user,city,curr_card)
    post_itinerary(chat_id)

    return

def itinerary(chat_id,chat_user,city,curr_card):
    city = city.title()
    weather = (curr_card.weather[0]).lower()
    temp = curr_card.weather[1]
    eat_place = curr_card.eatPlace
    visit_place = curr_card.visitPlace
    visit_place2 = curr_card.visitPlace2
    placelist = [visit_place, eat_place, visit_place2]
    placename = ['dining','a place to visit','another place to visit']
    
    caption_msg = (
        f"Hey {chat_user},\nHere\'s your itinerary for a day in <b>{city}</b>.\n\n"
        f"<b>{city}</b> is currently experiencing <b>{weather}</b> with a temperature of <b>{temp:.1f}°C</b>.\n\n"
        f"<b><u>Our suggestions:</u></b>\n"
        f"You can start by visiting {visit_place['name']}. ({visit_place['rating']}☆ / 5☆)\n\n"
        f"After which, you may grab some refreshments at {eat_place['name']}. ({eat_place['rating']}☆ / 5☆)\n\n"
        f"To end your day, you can visit {visit_place2['name']}. ({visit_place2['rating']}☆ / 5☆)\n\n"
        f"Enjoy!"
    )

    visit_img = InputMediaPhoto(retrievePics(visit_place['photos'][0]['photo_reference']),caption=caption_msg,parse_mode='HTML')
    eat_img = InputMediaPhoto(retrievePics(eat_place['photos'][0]['photo_reference']))
    visit_img2 = InputMediaPhoto(retrievePics(visit_place2['photos'][0]['photo_reference']))
    imgs = [visit_img,eat_img,visit_img2]

    bot.send_media_group(chat_id=chat_id,media=imgs)

    for idx, place in enumerate(placelist):
        if place != {}:
            bot.send_venue(
            chat_id=chat_id,
            latitude=place['geometry']['location']['lat'],
            longitude=place['geometry']['location']['lng'],
            title=place['name'],
            address=place['vicinity'],
            google_place_id=place['place_id'])
        else:
            notfound_msg = f"It seems like we couldn't find any spots for {placename[idx]}. You can reroll to try again."
            bot.send_message(chat_id=chat_id,text=notfound_msg)

def post_itinerary(chat_id):
    button_text = 'What would you like to do next?'
    row_one, row_two = [], []
    row_one.append(InlineKeyboardButton('Change Search Radius',callback_data='setrad'))
    row_two.append(InlineKeyboardButton('Reroll',callback_data='wander'))
    row_two.append(InlineKeyboardButton('Search by City',callback_data='search'))
    reply_markup = InlineKeyboardMarkup([row_one,row_two])
    bot.send_message(chat_id=chat_id,text=button_text,reply_markup=reply_markup)

@bot.message_handler(commands=['search'])
def search(message):
    chat_id = message.chat.id
    if not ('chat_name' in user_info):
        bot.send_message(chat_id=chat_id,text='Please run /start first!')
        return

    search_msg = 'Which city do you wish to get suggestions for?'
    search_msg_sent = bot.send_message(chat_id=chat_id,text=search_msg)
    bot.register_next_step_handler(search_msg_sent,get_city)

def get_city(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id=chat_id,action='typing')
    chat_user = user_info['chat_name']
    if message.text == None or message.text.isalpha() == False:
        unknownerr_msg = 'There was an error due to an invalid message. Please try the command again.'
        bot.send_message(chat_id,text=unknownerr_msg)
        return
    else:
        city = str(message.text).title()
        curr_card = cardClassSearch(city)

    if curr_card.weather == [] :
        invalid_msg = 'No places were found. You might have typed the city name wrongly.\nPlease try a valid city name, or wander around your current location >_<'
        bot.send_message(chat_id,text=invalid_msg)
        post_itinerary(chat_id)
        return
    itinerary(chat_id,chat_user,city,curr_card)
    post_itinerary(chat_id)

@server.route('/'+TOKEN,methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://wander-bot.herokuapp.com/'+TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))