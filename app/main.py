# main_second.py
from kivy.core.window import Window
import ctypes
from ctypes import wintypes

from classes import YoutubeDownloaderApp

# Window.size = (465, 1000)
# Window.top = 30
# Window.left = 1454
# Window.minimum_width = 465
# Window.minimum_height = 1000
#
# Window.maximum_width = 465
# Window.maximum_height = 1010

SPI_GETWORKAREA = 48

rect = wintypes.RECT()

ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)
taskbar_height = screen_height - (rect.bottom - rect.top)
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)

window_height = screen_height - taskbar_height - 30
Window.size = (465, window_height)
Window.left = screen_width - 465
Window.top = 30

# screen_width = 1920
# window_height = 1032
# screen_height = 1080
# taskbar_width = 48
# app sizes = (465, 1032)
# app top = 30

Window.minimum_width = 465
Window.maximum_width = 465

Window.minimum_height = window_height
Window.maximum_height = window_height

if __name__ == "__main__":
    YoutubeDownloaderApp().run()

