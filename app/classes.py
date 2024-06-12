# classes.py
import os
import re
import json
import shutil
import random
import time
import webbrowser
from tkinter import Tk, filedialog
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.filechooser import FileChooserListView
import yt_dlp as youtube_dl
import threading
from kivymd.uix.boxlayout import BoxLayout
import datetime
from kivy.graphics import Ellipse, Color
from kivymd.uix.textfield import MDTextField
from plyer import notification
from screeninfo import get_monitors
from kivy.core.window import Window
from kivymd.uix.slider import MDSlider
from kivy.clock import Clock
from PIL import Image, ImageDraw

from functions import (get_background_image, get_back_image, get_greeting, get_greet, add_username_to_end,
                       get_localized_date)

monitors = get_monitors()

for monitor in monitors:
    print(f"screen width: {monitor.width}, screen height: {monitor.height}")

KV = """
MDScreenManager:

    MDScreen:
        name: "screen A"
        FloatLayout:
            Image:
                id: background_image
                source: app.background_image_source
                allow_stretch: True
                keep_ratio: False

            Label:
                id: greeting_label
                text: app.greeting_text
                text_color: "black"
                font_size: "40sp"
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                pos_hint: {"center_x": 0.5, "top": 1.3}

            Label:
                id: under_greeting
                text: "Your hands are free now"
                font_size: "14sp"
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                pos_hint: {"center_x": 0.56, "top": 1.26}

            MDTextField:
                id: enter_name
                hint_text: 'Enter your name'
                # hint_text_color: 255, 255, 255, 1
                size_hint: (None, None)
                width: 300
                required: True
                pos_hint: {'center_x': 0.5, 'y': 0.37}
                font_size: '25sp'
                max_text_length: 10                
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                icon_right: "account-check-outline"
                on_text: app.check_button_status()

            MDTextField:
                id: enter_email
                hint_text: 'Enter your email address'
                # hint_text_color: 255, 255, 255, 1
                size_hint: (None, None)
                width: 300
                required: True
                pos_hint: {'center_x': 0.5, 'y': 0.3}
                font_size: '25sp'
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                icon_right: "email-outline"
                on_text: app.check_button_status()

            MDRaisedButton:
                id: submit_button
                text: "submit"
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                # md_bg_color: "white"
                pos_hint: {'center_x': 0.5, 'y': 0.2}
                disabled: not enter_name.text.strip() or not app.is_valid_email(enter_email.text)
                on_release:
                    app.save_username()
                    app.save_email()
                    root.current = "screen B"


    MDScreen:
        name: "screen B"
        FloatLayout:

            MDBottomNavigation:
                panel_color: "#0F1E34"
                text_color_normal: 1, 1, 1, 1
                font_name: "assets/fonts/Montserrat-Medium.ttf"
                font_size: "14sp"

                MDBottomNavigationItem:
                    id: bottom_navigation_1
                    name: 'home'
                    text: app.get_translation("bottom_navigation_1")
                    icon: "assets/icons/home.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: app.back_second
                        allow_stretch: True
                        keep_ratio: False

                    Label:
                        id: greeting_label
                        text: (f"{app.get_translation(app.text_second)}, {app.username}")
                        text_color: "white"
                        font_size: "25sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.34, "top": 1.38}


                    Label:
                        id: date
                        text: app.data
                        text_color: "white"
                        font_size: "14sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.23, "top": 1.34}
                    
                    Label:
                        id: question
                        text: app.get_translation("question")
                        text_color: "white"
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.5, "top": 0.6}
                    

                    MDIconButton:
                        id: mover
                        icon: "assets/icons/exchange.png"
                        pos_hint: {"x": 0.03, "top": 0.98}
                        on_release: 
                            app.move_to()


                MDBottomNavigationItem:
                    id: bottom_navigation_2
                    name: 'download'
                    text: app.get_translation("bottom_navigation_2")
                    icon: "assets/icons/downloads.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: app.back_second
                        allow_stretch: True
                        keep_ratio: False

                    Label:
                        id: greeting_label_second
                        text: (f"{app.get_translation(app.text_second)}, {app.username}")
                        text_color: "white"
                        font_size: "25sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.34, "top": 1.38}

                    Label:
                        id: date_second
                        text: app.data
                        text_color: "white"
                        font_size: "14sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.23, "top": 1.34}

                    MDCard:
                        size_hint: None, None
                        size: 466, 800
                        pos_hint: {'center_x': 0.5, 'center_y': 0.33}
                        radius: [23, 23, 20, 20] 
                        md_bg_color: "#252850"

                    MDCard:
                        size_hint: None, None
                        size: 466, 800
                        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                        radius: [23, 23, 20, 20] 
                        md_bg_color: "#2d3250"

                    MDLabel
                        id: downloader
                        text: app.get_translation("downloader")
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.55, "top": 1.13}

                    MDTextField:
                        id: enter_http
                        hint_text: app.get_translation("enter_http")
                        # hint_text_color: 255, 255, 255, 1
                        size_hint: (None, None)
                        width: 250
                        pos_hint: {'center_x': 0.37, 'y': 0.53}
                        font_size: '20sp'
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        on_text: to_download.disabled = not self.text.strip()                                           

                    MDLabel:
                        id: selected_path_label
                        text: ""
                        font_size: '18sp'
                        theme_text_color: "Custom"
                        text_size: self.width, None
                        text_color: 0.8, 0.8, 0.8, 1
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        size_hint: (0.8, None)
                        pos_hint: {'center_x': 0.5, 'y': 0.44}

                    MDIconButton:
                        id: to_download
                        icon: "assets/icons/download.png"
                        md_bg_color: self.theme_cls.primary_color if not self.disabled else self.theme_cls.disabled_hint_text_color
                        pos_hint: {'center_x': 0.75, 'y': 0.537}
                        on_release:
                            app.download_video_to_folder()

                    MDIconButton:
                        id: select_path_button
                        icon: "folder"
                        md_bg_color: self.theme_cls.primary_color if not self.disabled else self.theme_cls.disabled_hint_text_color
                        pos_hint: {'center_x': 0.89, 'y': 0.537}
                        on_release: 
                            app.open_folder_chooser()

                    MDIconButton:
                        id: mover
                        icon: "assets/icons/exchange.png"
                        pos_hint: {"x": 0.03, "top": 0.98}
                        on_release: 
                            app.move_to()

                    MDBoxLayout:
                        orientation: 'vertical'
                        pos_hint: {'center_x': 0.5, 'center_y': 1.17}
                        padding: '20dp'

                        MDProgressBar:
                            padding: '20dp'
                            id: progress_bar
                            size_hint_y: None
                            height: '4dp'
                            pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                            width: "10"
                            min: 0
                            max: 100
                            value: 0
                            color: app.theme_cls.accent_color

                    MDLabel:                            
                        id: progress_label
                        pos_hint: {'center_x': 0.57, 'center_y': 0.72}
                        text: ''
                        color: app.theme_cls.accent_color

                MDBottomNavigationItem:
                    id: bottom_navigation_3
                    name: 'account'
                    text: app.get_translation("bottom_navigation_3")
                    icon: "assets/icons/user.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: "assets/images/backone.png"
                        allow_stretch: True
                        keep_ratio: False

                    MDLabel:
                        id: head_1
                        text: app.get_translation("head_1")
                        font_size: '30sp'
                        color: app.theme_cls.accent_color
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {'center_x': 0.57, 'center_y': 0.88}

                    MDLabel:
                        id: head_1_1
                        text: app.get_translation("head_1_1")
                        font_size: '18sp'
                        color: app.theme_cls.accent_color
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {'center_x': 0.57, 'center_y': 0.8}

                    # all starts here                              
                    MDBoxLayout
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(100)
                        pos_hint: {'center_y': 0.675}
                        spacing: '10dp'
                        padding: '20dp'                        

                        MDBoxLayout:
                            orientation: 'vertical'
                            id: avatar_container_second
                            pos_hint: {'center_x': 0.3, 'center_y': 0.01}
                            Image:
                                id: avatar_image_second
                                size_hint: None, None
                                pos_hint: {'center_x': 0.5, 'center_y': 0.01}
                                size: 140, 140
                                source: app.set_avatar()
                                allow_stretch: True
                                keep_ratio: True                  

                        # personal info
                        MDBoxLayout:
                            pos_hint: {'center_x': 0.7, 'center_y': 0.5} 
                            orientation: 'vertical'
                            spacing: '20dp'
                            padding: '10dp'
                            width: dp(50)

                            MDLabel:
                                text: app.show_username()  
                                font_style: 'Subtitle1'
                                color: "white"
                                font_size: "20sp"
                                font_name: "assets/fonts/Montserrat-Medium.ttf"

                            MDLabel:
                                id: account_body
                                text: app.get_translation("account_body")
                                font_style: 'Caption'
                                color: "white"
                                font_size: "15sp"
                                font_name: "assets/fonts/Montserrat-Regular.ttf"

                        MDIconButton:
                            size_hint: None, None
                            size: 100, 100
                            pos_hint: {'center_y': 0.5}
                            icon: "assets/icons/icons8-right-32.png"  
                            on_release: 
                                app.edit_profile()

                    MDLabel:
                        id: head_q
                        text: app.get_translation("head_q")
                        font_size: '18sp'
                        color: app.theme_cls.accent_color
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {'center_x': 0.57, 'center_y': 0.55}


                    # Language                    
                    MDLabel:
                        id: preview_text
                        text: app.startup_language()
                        font_style: 'Caption'
                        color: "white"
                        pos_hint: {'center_x': 1.15, 'center_y': 0.45}
                        font_size: "15sp"
                        font_name: "assets/fonts/Montserrat-Regular.ttf"

                    MDBoxLayout:
                        pos_hint: {'center_x': 0.5, 'center_y': 0.45} 
                        orientation: 'horizontal'
                        padding: ['30dp', 0, '20dp', 0]

                        MDLabel:
                            id: change_1
                            text: app.get_translation("change_1")  
                            font_style: 'Subtitle1'
                            color: "white"
                            font_size: "20sp"
                            font_name: "assets/fonts/Montserrat-Medium.ttf"


                        MDIconButton:
                            size_hint: None, None
                            size: 100, 100
                            pos_hint: {'center_y': 0.5}
                            icon: "assets/icons/icons8-right-32.png"  
                            on_release: 
                                app.edit_language()

                    # Notifications
                    MDIconButton:
                        size_hint: (None, None)
                        size: 100, 100
                        pos_hint: {'center_x': 0.92,'center_y': 0.35}
                        icon: "assets/icons/icons8-right-32.png"  
                        on_release: 
                            app.edit_notifications()

                    MDLabel:
                        id: change_2
                        text: app.get_translation("change_2") 
                        pos_hint: {'center_x': 0.27,'center_y': 0.355}
                        font_style: 'Subtitle1'
                        color: "white"
                        size_hint: (0.4, 1)
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"

                    # Help                    
                    MDLabel:
                        id: change_3
                        text: app.get_translation("change_3")  
                        font_style: 'Subtitle1'
                        pos_hint: {'center_x': 0.58,'center_y': 0.26}
                        color: "white"
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"                        

                    MDIconButton:
                        size_hint: None, None
                        size: 100, 100
                        pos_hint: {'center_x': 0.92,'center_y': 0.25}
                        icon: "assets/icons/icons8-right-32.png"  
                        on_release: 
                            app.edit_help()

                    MDIconButton:
                        id: mover
                        icon: "assets/icons/exchange.png"
                        pos_hint: {"x": 0.03, "top": 0.98}
                        on_release: 
                            app.move_to()

    MDScreen:
        name: "NotificationsScreen"
        Image:
            source: "assets/images/backone.png"
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)

        MDLabel:
            id: change_notif_head
            text: app.get_translation("change_notif_head")
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.57, 'center_y': 0.95}
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            id: push_notif
            text: app.get_translation("push_notif")
            pos_hint: {'center_x': 0.57, 'center_y': 0.79}
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDSegmentedButton:
            id: segment1
            pos_hint: {'center_x': 0.5, 'center_y': 0.69}
            size_hint: (0.8, None)

            MDSegmentedButtonItem:
                id: segment1_1
                text: app.get_translation("segment1_1")
                active: app.check_push_notifications('allow')
                on_press:
                    app.change_push_notifications('True')
                     
            MDSegmentedButtonItem:
                id: segment1_2
                text: app.get_translation("segment1_2")
                active: app.check_push_notifications('deny')
                on_press:
                    app.change_push_notifications('False')

        MDLabel:
            id: email_n
            text: app.get_translation("email_n")
            pos_hint: {'center_x': 0.57, 'center_y': 0.59}
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            id: your_email
            text: f'{app.get_translation("your_email")} {app.get_email()}'
            pos_hint: {'center_x': 0.6, 'center_y': 0.55}
            color: "white"
            font_size: "16sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDSegmentedButton:
            id: segment2
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
            size_hint: (0.8, None)
            
            MDSegmentedButtonItem:
                id: segment2_1
                text: app.get_translation("segment2_1")
                active: app.check_email_notifications('allow')
                on_press:
                    app.change_email_notifications('True')
                 
            MDSegmentedButtonItem:
                id: segment2_2
                text: app.get_translation("segment2_2")   
                active: app.check_email_notifications('deny')
                on_press:
                    app.change_email_notifications('False')


        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            id: go_back_1
            text: app.get_translation("go_back_1")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.25, 'center_y': 0.15}
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"       
            on_release: app.go_back()   

    MDScreen:
        name: "languageScreen"
        Image:
            source: "assets/images/backone.png"
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)

        MDLabel:
            id: change_language_head
            text: app.get_translation("change_language_head")
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.57, 'center_y': 0.95}
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDCheckbox:
            group: 'language'
            id: checkbox_english    
            active: app.active_language('English')
            checkbox_icon_size: dp(36)
            pos_hint: {'center_x': 0.57, 'center_y': 0.8}
            size_hint: None, None
            size: dp(48), dp(48)
            on_active: app.set_language('English')

        MDLabel:
            id: english_la
            text: 'English'
            pos_hint: {'center_x': 0.35, 'center_y': 0.8}
            halign: 'center'
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            font_style: 'Body1'

        Image:
            source: 'assets/icons/uk.png'
            size_hint: (70, 70)
            pos_hint: {'center_x': 0.17, 'center_y': 0.8}

        MDCheckbox:
            group: 'language'
            id: checkbox_russian
            active: app.active_language('Russian')
            checkbox_icon_size: dp(36)
            size_hint: None, None
            pos_hint: {'center_x': 0.57, 'center_y': 0.7}
            size: dp(48), dp(48)
            on_active: app.set_language('Russian')

        MDLabel:
            id: label_russian
            text: 'Russian'
            halign: 'center'
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.35, 'center_y': 0.7}
            font_style: 'Body1'

        Image:
            source: 'assets/icons/ru.png'
            size_hint: (70, 70)
            pos_hint: {'center_x': 0.17, 'center_y': 0.7}

        MDCheckbox:
            id: checkbox_german
            group: 'language'
            active: app.active_language('German')
            size_hint: None, None
            checkbox_icon_size: dp(36)
            pos_hint: {'center_x': 0.57, 'center_y': 0.6}
            size: dp(48), dp(48)
            on_active: app.set_language('German')

        MDLabel:
            id: label_german
            text: 'German'
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.35, 'center_y': 0.6}
            halign: 'center'
            font_style: 'Body1'

        Image:
            source: 'assets/icons/germany.png'
            size_hint: (70, 70)
            pos_hint: {'center_x': 0.17, 'center_y': 0.6}
        
        MDCheckbox:
            id: checkbox_es
            group: 'language'
            active: app.active_language('Espanol')
            size_hint: None, None
            checkbox_icon_size: dp(36)
            pos_hint: {'center_x': 0.57, 'center_y': 0.5}
            size: dp(48), dp(48)
            on_active: app.set_language('Espanol')

        MDLabel:
            id: label_es
            text: 'Español'
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.35, 'center_y': 0.5}
            halign: 'center'
            font_style: 'Body1'

        Image:
            source: 'assets/icons/es.png'
            size_hint: (70, 70)
            pos_hint: {'center_x': 0.17, 'center_y': 0.5}

        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            id: go_back_2
            text: app.get_translation("go_back_2")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.25, 'center_y': 0.15}
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"       
            on_release: app.go_back()

    MDScreen:
        name: "HelpScreen"
        Image:
            source: "assets/images/backone.png"
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)

        MDLabel:
            id: help_head_1
            text: app.get_translation("help_head_1")
            pos_hint: {'center_x': 0.35, 'center_y': 0.93}
            font_style: 'Body1'
            size_hint: (0.6, None)
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            id: etc
            text: f"Youtube, Pinterest, TikTok, Twitch, Twitter, Crunchyroll, Steam {app.get_translation('etc')}"
            pos_hint: {'center_x': 0.55, 'center_y': 0.85}
            font_style: 'Body1'
            size_hint: (0.9, None)
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        Image:
            source: 'assets/icons/pdf.png'
            pos_hint: {'center_x': 0.15, 'center_y': 0.67}

        MDFlatButton:
            id: pdf
            text: app.get_translation("pdf")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_size: "16sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.45, 'center_y': 0.67}
            on_release: app.download_policy()

        MDBoxLayout:
            orientation: 'vertical'
            canvas:
                Color:
                    rgba: 1, 1, 1, 1 
                Rectangle:
                    pos: 55, 650  
                    size: 270, 1 

        MDLabel:
            id: help_head_3
            text: app.get_translation("help_head_3")
            pos_hint: {'center_x': 0.55, 'center_y': 0.6}
            font_style: 'Body1'
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            pos_hint: {'center_x': 0.53, 'center_y': 0.5}
            font_style: 'Body1'
            size_hint: (0.9, None)
            color: "white"
            font_size: "14sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"


        MDLabel:
            id: help_head_4
            text: app.get_translation("help_head_4")
            pos_hint: {'center_x': 0.6, 'center_y': 0.35}
            font_style: 'Body1'           
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDFlatButton:
            text: "your.email.example.com"
            theme_text_color: "Custom"
            text_color: 0.85, 0.8, 0.62, 1
            pos_hint: {'center_x': 0.35, 'center_y': 0.32}
            font_style: 'Body1'
            font_size: "16sp"
            size_hint_y: None
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            on_release: app.copy_to_clipboard(self.text)

        MDLabel:
            id: click
            text: app.get_translation("click")
            pos_hint: {'center_x': 0.67, 'center_y': 0.29}
            font_style: 'Body1'
            color: "white"
            font_size: "14sp"
            font_name: "assets/fonts/Montserrat-Regular.ttf"
            size_hint_y: None

        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            id: go_back_3
            text: app.get_translation("go_back_3")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.25, 'center_y': 0.15}
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"       
            on_release: app.go_back()

    MDScreen:
        name: "profileScreen"
        Image:
            source: "assets/images/backone.png"
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)

        MDLabel:
            id: change_acc_head
            text: app.get_translation("change_acc_head")
            font_size: '26sp'
            color: app.theme_cls.accent_color
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.55, 'center_y': 0.95}
        
        BoxLayout:
            orientation: 'vertical'
            id: avatar_container
            pos: 40, 750
            Image:
                id: avatar_image
                size_hint: None, None
                size: 140, 140
                source: app.set_avatar()
                allow_stretch: True
                keep_ratio: True

        MDIconButton:
            icon: "camera"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.24, 'center_y': 0.71}
            on_release: app.upload_avatar()
            size_hint: (None, None)
            size: dp(64), dp(64)

        MDLabel:
            text: app.show_username()
            font_size: '20sp'
            size_hint: (0.5, None)
            color: "white"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.71, 'center_y': 0.84}

        MDLabel:
            text: app.get_email()
            font_size: '20sp'
            size_hint: (0.5, None)
            color: 'white'
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.71, 'center_y': 0.79}

        MDLabel:
            id: change_info
            text: app.get_translation("change_info")
            font_size: '16sp'
            size_hint: (0.5, None)
            color: "white"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.35, 'center_y': 0.6}

        MDTextField:
            id: enter_name_again
            hint_text: app.get_translation("enter_name_again")
            # hint_text_color: 255, 255, 255, 1
            size_hint: (None, None)
            width: 300
            required: True
            pos_hint: {'center_x': 0.5, 'y': 0.48}
            font_size: '25sp'
            max_text_length: 10                
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            icon_right: "account-check-outline"

        MDRaisedButton:
            id: submit_button_again1
            text: app.get_translation("submit_button_again1")
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            # md_bg_color: "white"
            pos_hint: {'center_x': 0.5, 'y': 0.4}
            on_release:
                app.save_username_two()

        MDTextField:
            id: enter_email_again
            hint_text: app.get_translation("enter_email_again")
            # hint_text_color: 255, 255, 255, 1
            size_hint: (None, None)
            width: 300
            required: True
            pos_hint: {'center_x': 0.5, 'y': 0.28}
            font_size: '25sp'
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            icon_right: "email-outline"

        MDRaisedButton:
            id: submit_button_again2
            text: app.get_translation("submit_button_again2")
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            # md_bg_color: "white"
            pos_hint: {'center_x': 0.5, 'y': 0.2}
            on_release:
                app.save_email_again()

        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            id: go_back_4
            text: app.get_translation("go_back_4")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.25, 'center_y': 0.15}
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"       
            on_release: app.go_back()
"""


# Download path selection
class CustomFileChooser(FileChooserListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rootpath = 'D:/'
        self.dirselect = True


class DownloadFolderChooser:
    def __init__(self, callback):
        self.callback = callback
        self.file_path = ""

    def select_folder(self):
        root = Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select path to download")
        root.destroy()

        if folder_path:
            self.file_path = folder_path
            self.callback(self.file_path)

    def open(self):
        self.select_folder()

    def callback(self, selected_path):
        print(f"Selected folder: {selected_path}")


class ProgressBar(MDSlider):
    pass


# First-in main background
class YoutubeDownloader(BoxLayout):
    def __init__(self, background_image=None, greeting=None, **kwargs):
        super().__init__(**kwargs)

        if background_image:
            self.ids.background_image.source = background_image

        if greeting:
            self.ids.greeting_label.text = greeting


# Core
class YoutubeDownloaderApp(MDApp):
    my_text = StringProperty("Initial text")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_image_source = get_background_image()
        self.email = None
        self.greeting_text = get_greeting()
        self.text_second = get_greet()
        self.username = add_username_to_end()
        self.back_second = get_back_image()
        self.data = get_localized_date(self.startup_language())
        self.window_position = "left"
        self.selected_folder_path = ""
        self.language_text = self.startup_language()

    def build(self):
        # Theme customization
        current_time = datetime.datetime.now().time()
        if datetime.time(6, 0) <= current_time < datetime.time(18, 0):
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.primary_hue = "500"
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.primary_hue = "300"

        return Builder.load_string(KV)

    def on_start(self):
        if os.path.exists("username.json"):
            self.root.current = "screen B"
            print('Screen B')

    def save_username(self):
        self.username = self.root.ids.enter_name.text
        self.write_username()
        print(f"Username saved", self.username)

    def save_username_two(self):
        self.username = self.root.ids.enter_name_again.text
        self.write_username()
        print(f"Username saved", self.username)

    def write_username(self):
        username_file = "username.json"
        with open(username_file, "w") as f:
            data = {"username": self.username}
            json.dump(data, f)

    @staticmethod
    def copy_to_clipboard(text):
        Clipboard.copy(text)

    @staticmethod
    def show_username():
        if os.path.isfile('username.json'):
            with open('username.json', 'r') as file:
                data = json.load(file)
            if 'username' in data:
                username = data['username']
                return username
        else:
            return 'loading...'

    @staticmethod
    def get_email():
        if os.path.isfile('email.json'):
            with open('email.json', 'r') as file:
                data = json.load(file)
            if 'email' in data:
                email = data['email']
                return email
        else:
            return 'loading...'

    def save_email(self):
        self.email = self.root.ids.enter_email.text
        self.write_email()
        print(f"Email address saved", self.email)

    def save_email_again(self):
        self.email = self.root.ids.enter_email_again.text
        self.write_email()
        print(f"Email address saved", self.email)

    def write_email(self):
        email_file = "email.json"
        with open(email_file, "w") as f:
            data = {"email": self.email}
            json.dump(data, f)

    # 1455
    def move_to(self):
        if self.window_position == "right":
            Window.left = 0
            self.window_position = "left"
        elif self.window_position == "left":
            Window.left = monitor.width - Window.width
            self.window_position = "right"

    @staticmethod
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def check_button_status(self):
        enter_name = self.root.ids.enter_name.text.strip()
        enter_email = self.root.ids.enter_email.text.strip()
        submit_button = self.root.ids.submit_button

        valid_email = self.is_valid_email(enter_email)
        submit_button.disabled = not enter_name or not enter_email or not valid_email

    def open_folder_chooser(self):
        folder_chooser = DownloadFolderChooser(callback=self.set_selected_folder_path)
        folder_chooser.open()

    def set_selected_folder_path(self, folder_path):
        self.selected_folder_path = folder_path
        self.root.ids.selected_path_label.text = folder_path

    @staticmethod
    def save_url_to_file(url):
        with open("downloaded_url.txt", "w", encoding='utf-8') as file:
            file.write(url)

    @staticmethod
    def load_url_from_file():
        with open("downloaded_url.txt", "r", encoding='utf-8') as file:
            return file.read().strip()

    def download_video(self, url):
        try:
            self.root.ids.enter_http.helper_text = "Video download in progress"
            ydl_opts = {
                'format': 'best',
                'outtmpl': self.selected_folder_path + '%(title)s.%(ext)s',
                'progress_hooks': [self.on_progress]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.ids.enter_http.helper_text = "Video downloaded successfully"
            self.send_windows_notification('Success')
            print("Video downloaded successfully")

        except Exception as e:
            self.root.ids.enter_http.helper_text = str(e)
            print(f"An error occurred: {str(e)}")

    def on_progress(self, data):
        if data['status'] == 'downloading':
            total_bytes = data.get('total_bytes')
            bytes_received = data.get('downloaded_bytes')
            if total_bytes and bytes_received:
                progress = (bytes_received / total_bytes) * 100
                if progress == 100.0:
                    self.root.ids.progress_label.text = self.get_translation("download_done")
                    self.root.ids.progress_bar.value = progress
                else:
                    print(f"Progress: {progress:.2f}%")
                    self.root.ids.progress_label.text = f'{progress:.2f}%'
                    self.root.ids.progress_bar.value = progress

    def download_video_to_folder(self):
        url = self.root.ids.enter_http.text
        self.save_url_to_file(url)
        try:
            url = self.load_url_from_file()
            if url:
                download_thread = threading.Thread(target=self.download_video, args=(url,))
                download_thread.start()
            else:
                self.root.ids.enter_http.helper_text = "Invalid URL provided."
                self.send_windows_notification("Invalid URL provided.")
                print("Invalid URL provided.")
        except Exception as e:
            self.root.ids.enter_http.helper_text = str(e)
            self.send_windows_notification("An error occurred while downloading the video")
            print(f"An error occurred: {str(e)}")

    # account screen switches
    def edit_profile(self):
        self.root.current = "profileScreen"

    def edit_language(self):
        self.root.current = "languageScreen"

    def edit_notifications(self):
        self.root.current = "NotificationsScreen"

    def edit_help(self):
        self.root.current = "HelpScreen"

    def go_back(self):
        self.root.current = "screen B"

    # end of switches

    @staticmethod
    def download_policy():
        pdf_path = 'Privacy Policy.pdf'
        webbrowser.open(pdf_path)

    def set_language(self, language):
        language_file = "set_language.json"
        with open(language_file, "w") as f:
            data = {"language": language}
            json.dump(data, f)
        print(f'Language selected: {language}')
        self.update_language_text()
        self.update_text_elements()

    def update_language_text(self):
        new_language = self.startup_language()
        self.language_text = new_language
        self.root.ids.preview_text.text = self.language_text

    @staticmethod
    def change_push_notifications(notif):
        notif_file = "set_push_notification.json"
        with open(notif_file, "w") as f:
            data = {"notif_push": notif}
            json.dump(data, f)

    def check_push_notifications(self, button_name):
        print(f'check_push_notifications: {button_name}')
        if os.path.exists('set_push_notification.json'):
            with open('set_push_notification.json', "r") as json_file:
                data = json.load(json_file)
                value = data.get("notif_push")
            if value == "True":
                if button_name == 'allow':
                    return True
                elif button_name == 'deny':
                    return False
            elif value == "False":
                if button_name == 'allow':
                    return False
                elif button_name == 'deny':
                    return True
        else:
            print("push notifications haven't been clicked yet")
            if button_name == 'allow':
                return False
            elif button_name == 'deny':
                return True

    @staticmethod
    def change_email_notifications(notif):
        notif_file = "set_email_notification.json"
        with open(notif_file, "w") as f:
            data = {"notif_email": notif}
            json.dump(data, f)

    def check_email_notifications(self, button_name):
        if os.path.exists('set_email_notification.json'):
            with open('set_email_notification.json', "r") as json_file:
                data = json.load(json_file)
                value = data.get("notif_email")
            if value == "True":
                if button_name == 'allow':
                    return True
                elif button_name == 'deny':
                    return False
            elif value == "False":
                if button_name == 'allow':
                    return False
                elif button_name == 'deny':
                    return True
        else:
            print("notifications by email haven't been clicked yet")
            if button_name == 'allow':
                return False
            elif button_name == 'deny':
                return True

    def upload_avatar(self):
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select Avatar", filetypes=[("Image files", "*.png *.jpg *.jpeg")])

        if file_path:
            destination_path = os.path.join(os.getcwd(), "assets", "images", "custom_avatar.png")
            shutil.copyfile(file_path, destination_path)
            print(f"Avatar saved to: {destination_path}")
            self.update_avatar()
        else:
            print("No file selected.")

    def set_avatar(self):
        assets_folder = os.path.join(os.getcwd(), "assets")
        subfolder_path = os.path.join(assets_folder, "images", "custom_avatar.png")
        if os.path.exists(subfolder_path):
            self.make_image_round(subfolder_path)
            return subfolder_path
        else:
            return os.path.join(assets_folder, "images", "user.png")

    @staticmethod
    def make_image_round(image_path):
        image = Image.open(image_path).convert("RGBA")

        min_side = min(image.size)
        size = (min_side, min_side)

        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        output_image = Image.new("RGBA", size)

        left = (image.size[0] - min_side) // 2
        top = (image.size[1] - min_side) // 2
        right = left + min_side
        bottom = top + min_side

        cropped_image = image.crop((left, top, right, bottom))
        output_image.paste(cropped_image, (0, 0), mask)
        output_image.save("assets/images/custom_avatar.png")

    def update_avatar(self):
        # first
        avatar_source = self.set_avatar()
        avatar_image = self.root.ids.avatar_image
        avatar_image.source = avatar_source
        avatar_image.reload()

        # second
        avatar_source_second = self.set_avatar()
        avatar_image_second = self.root.ids.avatar_image_second
        avatar_image_second.source = avatar_source_second
        avatar_image_second.reload()

    @staticmethod
    def active_language(to_check):
        if os.path.exists('set_language.json'):
            with open('set_language.json', "r") as json_file:
                data = json.load(json_file)
                language_value = data.get("language")
                if to_check == language_value:
                    return True
                else:
                    return False
        else:
            if to_check == 'English':
                return True
            else:
                return False

    @staticmethod
    def startup_language():
        if os.path.exists('set_language.json'):
            with open('set_language.json', "r") as json_file:
                data = json.load(json_file)
                language_value = data.get("language")
                return language_value
        else:
            return 'English'

    def send_windows_notification(self, message, timeout=8):
        if os.path.exists('set_push_notification.json'):
            with open('set_push_notification.json', "r") as json_file:
                data = json.load(json_file)
                value = data.get("notif_push")
                print('Yep')
                if value == "True":
                    notification.notify(
                        title="Downloader",
                        message=message,
                        app_icon="assets/icons/app-ico.ico",
                        timeout=timeout,
                    )

    def get_translation(self, key):
        file_path = "languages.json"
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            language = self.startup_language()
            return data.get(language, {}).get(key)

    def update_text_elements(self):
        source = "Youtube, Pinterest, TikTok, Twitch, Twitter, Crunchyroll, Steam "
        ids = [
            'bottom_navigation_1', 'question', 'bottom_navigation_2', 'greeting_label', 'downloader', 'enter_http',
            'bottom_navigation_3', 'head_1', 'head_1_1', 'account_body', 'head_q', 'change_1',
            'change_2', 'change_3', 'change_notif_head', 'push_notif', 'segment1_1', 'segment1_2', 'email_n',
            'your_email', 'segment2_1', 'segment2_2', 'go_back_1', 'go_back_2', 'go_back_3', 'go_back_4',
            'change_language_head', 'help_head_1', 'etc', 'pdf', 'help_head_3', 'help_head_4', 'click', 'go_back',
            'change_acc_head', 'change_info', 'enter_name_again', 'submit_button_again1',
            'enter_email_again', 'submit_button_again2'
        ]

        etc_translations = {"etc.", "и т.д.", "usw.", "etc."}

        your_email_translations = {"Ваша электронная почта:", "Tu correo:", "Ihre E-Mail-Adresse:", "Your email:"}

        for element_id in ids:
            element = self.root.ids.get(element_id)
            if element:
                translation = self.get_translation(element_id)
                if isinstance(element, MDTextField):
                    element.hint_text = translation if translation is not None else ""
                else:
                    if translation in etc_translations:
                        element.text = source + translation if translation is not None else ""
                    elif translation in your_email_translations:
                        element.text = translation + " " + self.get_email() if translation is not None else ""
                    else:
                        element.text = translation if translation is not None else ""

        self.update_greeting_and_date()

    def update_greeting_and_date(self):
        greeting_key = get_greet()
        greeting_text = self.get_translation(greeting_key)
        date_text = get_localized_date(self.startup_language())

        self.root.ids.greeting_label.text = f"{greeting_text}, {self.username}"
        self.root.ids.greeting_label_second.text = f"{greeting_text}, {self.username}"
        self.root.ids.date.text = date_text
        self.root.ids.date_second.text = date_text
