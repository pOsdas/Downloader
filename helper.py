# helper.py

import json
import os
import sqlite3


def create_username(username) -> None:
    username_file = "username.json"
    with open(username_file, "w") as f:
        data = {"username": username}
        json.dump(data, f)


def create_email(email) -> None:
    email_file = "username.json"
    with open(email_file, "w") as f:
        data = {"email": email}
        json.dump(data, f)


def skip_first_screen() -> None:
    if not os.path.isfile('user.json'):
        print("login with skipping first screen? Y/n")
        answer: str = input()
        if answer == "Y" or answer == "y":
            create_username("None")
            create_email("None@example.com")


def show_db():
    conn = sqlite3.connect("downloaded_videos.db")
    c = conn.cursor()
    c.execute('''
        SELECT * FROM downloads
    ''')
    conn.commit()
    conn.close()

