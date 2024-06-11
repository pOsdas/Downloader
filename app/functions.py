# functions.py
import datetime
import json
import os
import random
from babel.dates import format_date


# First-in text
def get_greeting():
    current_time = datetime.datetime.now().time()
    if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
        return 'Good morning'
    else:
        return 'Good night'


# First-in background
def get_background_image():
    current_time = datetime.datetime.now().time()
    if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
        # Day
        return 'assets/images/first_day.png'
    else:
        # Night
        return 'assets/images/first_night.png'


# Background during entrances > 1
def get_back_image():
    current_time = datetime.datetime.now().time()
    if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
        # Day
        x = random.randint(1, 6)
        return f'assets/images/second{x}.png'
    else:
        # night
        x = random.randint(1, 2)
        return f'assets/images/second_night{x}.png'


# Text during entrances > 1
def get_greet():
    current_time = datetime.datetime.now().time()
    if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
        return 'greeting_m'
    else:
        return 'greeting_n'


def add_username_to_end():
    username = ''
    if os.path.isfile('username.json'):
        with open('username.json', 'r') as file:
            data = json.load(file)
        if 'username' in data:
            username = data['username']
    return username


def get_localized_date(language):
    now = datetime.datetime.now()
    if language == 'English':
        localized_date = format_date(now, format='d MMMM, yyyy', locale='en')
        return localized_date
    elif language == 'Russian':
        localized_date = format_date(now, format='d MMMM, yyyy', locale='ru')
        return localized_date
    elif language == 'German':
        localized_date = format_date(now, format='d MMMM, yyyy', locale='de')
        return localized_date
    elif language == 'Espanol':
        localized_date = format_date(now, format='d MMMM, yyyy', locale='es')
        return localized_date
    else:
        return None

