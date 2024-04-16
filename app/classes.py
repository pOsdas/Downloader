# classes.py
import os
import re
import json
import shutil
import webbrowser
from tkinter import Tk, filedialog
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.filechooser import FileChooserListView
import yt_dlp as youtube_dl
import threading
from kivymd.uix.boxlayout import BoxLayout
import datetime
from screeninfo import get_monitors
from kivy.core.window import Window
from kivymd.uix.slider import MDSlider

from functions import get_background_image, get_back_image, get_data, get_greeting, get_greet

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
                    name: 'home'
                    text: 'home'
                    icon: "assets/icons/home.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: app.back_second
                        allow_stretch: True
                        keep_ratio: False

                    Label:
                        id: greeting_label
                        text: app.text_second
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

                    MDIconButton:
                        id: mover
                        icon: "assets/icons/exchange.png"
                        pos_hint: {"x": 0.03, "top": 0.98}
                        on_release: 
                            app.move_to()


                MDBottomNavigationItem:
                    name: 'download'
                    text: 'download'
                    icon: "assets/icons/downloads.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: app.back_second
                        allow_stretch: True
                        keep_ratio: False

                    Label:
                        id: greeting_label
                        text: app.text_second
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
                        text: 'Download:'
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {"center_x": 0.55, "top": 1.13}

                    MDTextField:
                        id: enter_http
                        hint_text: 'Enter your link'
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
                    name: 'account'
                    text: 'account'
                    icon: "assets/icons/user.png"
                    icon_color_active: "orange"

                    Image:
                        id: background_image
                        source: "assets/images/backone.png"
                        allow_stretch: True
                        keep_ratio: False

                    MDLabel:
                        text: 'Settings'
                        font_size: '30sp'
                        color: app.theme_cls.accent_color
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {'center_x': 0.57, 'center_y': 0.88}

                    MDLabel:
                        text: 'Account'
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
                            canvas:
                                Color:
                                    rgb: 1, 1, 1
                                Ellipse:
                                    pos: 30, 567
                                    size: 140 , 140 
                                    source: app.set_avatar()
                                    angle_start: 0
                                    angle_end: 360                       

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
                                text: 'Personal Info'
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
                        text: 'Settings'
                        font_size: '18sp'
                        color: app.theme_cls.accent_color
                        font_name: "assets/fonts/Montserrat-Medium.ttf"
                        pos_hint: {'center_x': 0.57, 'center_y': 0.55}



                    # Language                    
                    MDLabel:
                        text: 'English'
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
                            text: 'Language'  
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
                        text: 'Notifications' 
                        pos_hint: {'center_x': 0.27,'center_y': 0.355}
                        font_style: 'Subtitle1'
                        color: "white"
                        size_hint: (0.4, 1)
                        font_size: "20sp"
                        font_name: "assets/fonts/Montserrat-Medium.ttf"

                    # Help                    
                    MDLabel:
                        text: 'Help'  
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
            text: 'Choose an Option:'
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.57, 'center_y': 0.95}
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            text: 'Push notifications:'
            pos_hint: {'center_x': 0.57, 'center_y': 0.79}
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDSegmentedButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.69}
            size_hint: (0.8, None)


            MDSegmentedButtonItem:
                text: 'Allow'
                name: 'allow'    
            MDSegmentedButtonItem:
                text: 'Deny'
                name: 'deny'
                active: True

        MDLabel:
            text: 'Notifications by email:'
            pos_hint: {'center_x': 0.57, 'center_y': 0.59}
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            text: f'Your email: {app.get_email()}'
            pos_hint: {'center_x': 0.6, 'center_y': 0.55}
            color: "white"
            font_size: "16sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDSegmentedButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
            size_hint: (0.8, None)
            default_tab: 'deny1'
            MDSegmentedButtonItem:
                text: 'Allow'
                name: 'allow1'      
            MDSegmentedButtonItem:
                text: 'Deny'   
                name: 'deny1'
                active: True 


        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            text: 'Go back'
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
            text: 'Choose language:'
            font_style: 'Subtitle1'
            pos_hint: {'center_x': 0.57, 'center_y': 0.95}
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDCheckbox:
            group: 'language'
            id: checkbox_english    
            active: True       
            checkbox_icon_size: dp(36)
            pos_hint: {'center_x': 0.57, 'center_y': 0.8}
            size_hint: None, None
            size: dp(48), dp(48)
            on_active: app.set_language('English')

        MDLabel:
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
            checkbox_icon_size: dp(36)
            size_hint: None, None
            pos_hint: {'center_x': 0.57, 'center_y': 0.7}
            size: dp(48), dp(48)
            on_active: app.set_language('Russian')

        MDLabel:
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
            size_hint: None, None
            checkbox_icon_size: dp(36)
            pos_hint: {'center_x': 0.57, 'center_y': 0.6}
            size: dp(48), dp(48)
            on_active: app.set_language('German')

        MDLabel:
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

        MDIconButton:
            icon: "arrow-left"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_x': 0.1, 'center_y': 0.15}
            on_release: app.go_back()
            size_hint: (None, None)

        MDFlatButton:
            text: 'Go back'
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
            text: "1. Where can I download the video from?"
            pos_hint: {'center_x': 0.35, 'center_y': 0.93}
            font_style: 'Body1'
            size_hint: (0.6, None)
            color: app.theme_cls.accent_color
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        MDLabel:
            text: "Youtube, Pinterest, TikTok, Twitch, Twitter, Crunchyroll, Steam etc."
            pos_hint: {'center_x': 0.55, 'center_y': 0.85}
            font_style: 'Body1'
            size_hint: (0.9, None)
            color: "white"
            font_size: "20sp"
            font_name: "assets/fonts/Montserrat-Medium.ttf"

        Image:
            source: 'assets/icons/txt.png'
            pos_hint: {'center_x': 0.15, 'center_y': 0.67}

        MDFlatButton:
            text: "Download Privacy Policy"
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
            text: "2. Second point"
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
            text: "If you have any questions:"
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
            text: "press on email!"
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
            text: 'Go back'
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
            text: 'Account info:'
            font_size: '26sp'
            color: app.theme_cls.accent_color
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.55, 'center_y': 0.95}

        MDBoxLayout:
            orientation: 'vertical'
            canvas:
                Color:
                    rgb: 1, 1, 1
                Ellipse:
                    pos: 40, 750
                    size: 140 , 140 
                    source: app.set_avatar()
                    angle_start: 0
                    angle_end: 360

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
            text: 'If you want to change:'
            font_size: '16sp'
            size_hint: (0.5, None)
            color: "white"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            pos_hint: {'center_x': 0.35, 'center_y': 0.6}

        MDTextField:
            id: enter_name_again
            hint_text: 'Enter your name'
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
            text: "submit"
            font_name: "assets/fonts/Montserrat-Medium.ttf"
            # md_bg_color: "white"
            pos_hint: {'center_x': 0.5, 'y': 0.4}
            on_release:
                app.save_username_two()

        MDTextField:
            id: enter_email_again
            hint_text: 'Enter your email address'
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
            text: "submit"
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
            text: 'Go back'
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_image_source = get_background_image()
        self.email = self.username = None
        self.greeting_text = get_greeting()
        self.text_second = get_greet()
        self.back_second = get_back_image()
        self.data = get_data()
        self.window_position = "left"
        self.selected_folder_path = ""

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
        toast("Text copied to clipboard!")

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
                    self.root.ids.progress_label.text = 'Done'
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
                print("Invalid URL provided.")
        except Exception as e:
            self.root.ids.enter_http.helper_text = str(e)
            print(f"An error occurred: {str(e)}")

    # account screen
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

    @staticmethod
    def download_policy():
        pdf_path = 'Privacy Policy.pdf'
        webbrowser.open(pdf_path)

    def set_language(self, language):
        print(f'Language selected: {language}')

    def change_language(self):
        # in future
        pass

    def change_notifications(self):
        # in future
        pass

    @staticmethod
    def upload_avatar():
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select Avatar", filetypes=[("Image files", "*.png *.jpg *.jpeg")])

        if file_path:
            destination_path = os.path.join(os.getcwd(), "assets", "images", "custom_avatar.png")
            shutil.copyfile(file_path, destination_path)
            print(f"Avatar saved to: {destination_path}")
        else:
            print("No file selected.")

    @staticmethod
    def set_avatar():
        assets_folder = os.path.join(os.getcwd(), "assets")
        subfolder_path = os.path.join(assets_folder, "images", "custom_avatar.png")
        if os.path.exists(subfolder_path):
            return "assets/images/custom_avatar.png"
        else:
            return "assets/images/user.png"