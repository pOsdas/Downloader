# functions.py
import datetime
import json
import os
import random
import calendar


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
    if os.path.isfile('username.json'):
        with open('username.json', 'r') as file:
            data = json.load(file)
        if 'username' in data:
            username = data['username']
            current_time = datetime.datetime.now().time()
            if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
                return f'Good morning, {username}'
            else:
                return f'Good night, {username}'

    else:
        return 'Good night'


def get_data():
    now = datetime.datetime.now()
    day = now.day
    year = now.year
    month_number = now.month
    month_name = calendar.month_name[month_number].lower()
    return f'{day} {month_name}, {year}'
