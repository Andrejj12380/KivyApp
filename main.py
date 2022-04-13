import os
import time
from pprint import pprint
import numpy
import numpy as np
from cv2 import cv2, CV_8U
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window


class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        self.background_down = MDApp.get_running_app().theme_cls.primary_light
        super().__init__(**kwargs)


class TutorialApp(MDApp):
    Window.size = (1080, 720)
    i = 0
    path = r'C:\logs'
    files = os.listdir(path)
    cut = f'{path}/{files[i]}'

    def __init__(self):
        super().__init__()
        self.gridlayout = None
        self.label1 = None
        self.time_msec = None
        self.video = None
        self.start = None
        self.myimage = None
        self.label = None
        self.layout = None

    def nothing(*arg):
        pass

    cv2.namedWindow("settings")  # создаем окно настроек
    cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
    cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
    cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
    crange = [0, 0, 0, 0, 0, 0]

    def button_pressed(self, *args):
        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)
        if self.start.state == 'normal':
            self.start.text = 'Старт'
        else:
            self.start.text = 'Стоп'
        if self.start.state == 'down':
            time_start = time.time()
            ret, frame = self.video.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2XYZ)
            thresh = cv2.inRange(hsv, h_min, h_max)
            # применяем цветовой фильтр
            # ищем контуры и складируем их в переменную contours
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # pre = cv2.drawContours(hsv, contours, -1, (255, 0, 0), 2, cv2.LINE_AA, hierarchy, 0)
            filtered = cv2.drawContours(frame, contours, -2, (0, 255, 0), 1, cv2.LINE_AA, hierarchy, 5)
            # convert it to texture
            buffer = cv2.flip(filtered, 0).tostring()
            texture1 = Texture.create(size=(filtered.shape[1], filtered.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.myimage.texture = texture1
            time_end = time.time()
            time_sec = time_end - time_start
            self.time_msec = time_sec * 1000
            self.label.text = f'{int(self.time_msec)} мс'
            self.label.font_size = 28
            self.label.color = '#00B580'

    def build(self):
        self.layout = MDBoxLayout(orientation="vertical",
                                  md_bg_color=[.0, .9, .9, .1],
                                  spacing=5
                                  )
        self.label = MDLabel(size_hint=(1, .06),
                             halign='center'
                             )
        self.video = cv2.VideoCapture(f'rtsp://admin:123.qwe.@192.168.1.64/H264?ch=1&subtype=')
        Clock.schedule_interval(self.button_pressed, 1.0 / 100.0)
        self.myimage = Image(source='',
                             size_hint=(1, 1))
        self.start = MyToggleButton(background_normal=[.1, .5, .9, .1],
                                    background_down=[.9, .2, .1, .5],
                                    text="",
                                    ripple_color=[.1, .6, .7, .9],
                                    font_size=28,
                                    size_hint=(.08, .07),
                                    pos_hint={'right': 0},
                                    radius=10)
        self.gridlayout = MDGridLayout(cols=2,
                                       rows=1,
                                       row_force_default=True,
                                       row_default_height=40,
                                       col_force_default=True,
                                       col_default_width=535,
                                       size_hint=(.03, .065)
                                       )
        self.start.bind(on_press=self.button_pressed)
        self.gridlayout.add_widget(self.label)
        self.layout.add_widget(self.myimage)
        self.gridlayout.add_widget(self.start)
        self.layout.add_widget(self.gridlayout)

        return self.layout


TutorialApp().run()
