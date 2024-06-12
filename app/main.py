# main_second.py
from kivy.core.window import Window

from classes import YoutubeDownloaderApp

Window.size = (465, 1010)
Window.top = 30
Window.left = 1454
Window.minimum_width = 465
Window.minimum_height = 1010

Window.maximum_width = 465
Window.maximum_height = 1010

if __name__ == "__main__":
    YoutubeDownloaderApp().run()

