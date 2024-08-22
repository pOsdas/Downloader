# main_second.py

from kivy.core.window import Window
import ctypes
from ctypes import wintypes

from classes import YoutubeDownloaderApp

import os
import certifi
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()


def setup_window():
    SPI_GETWORKAREA: int = 48

    rect = wintypes.RECT()

    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    screen_height: int = ctypes.windll.user32.GetSystemMetrics(1)
    taskbar_height: int = screen_height - (rect.bottom - rect.top)
    user32 = ctypes.windll.user32
    screen_width: int = user32.GetSystemMetrics(0)

    window_height: int = screen_height - taskbar_height - 30
    Window.size = (465, window_height)
    Window.left = screen_width - 465
    Window.top = 30

    Window.minimum_width = 465
    Window.maximum_width = 465

    Window.minimum_height = window_height
    Window.maximum_height = window_height


if __name__ == "__main__":
    setup_window()
    YoutubeDownloaderApp().run()
