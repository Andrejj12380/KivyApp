import os
import time
from pprint import pprint
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from cv2 import *
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDTextButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout, MDAdaptiveWidget


class TutorialApp(MDApp):
    i = 0
    path = r'C:\logs'
    files = os.listdir(path)
    cut = f'{path}/{files[i]}'

    def __init__(self):
        super().__init__()
        self.times_msecs = None
        self.label1 = None
        self.video = None
        self.imgray = None
        self.img = None
        self.back = None
        self.forward = None
        self.myimage = None
        self.label = None
        self.layout = None

    def button_pressed(self, *args):
        if self.forward.state == 'down' or TutorialApp.i > 0:
            TutorialApp.i += 1
            # TutorialApp.cut = f'{TutorialApp.path}\\{TutorialApp.files[TutorialApp.i + 1]}'
            # self.myimage.source = TutorialApp.cut
            self.label.text = str(TutorialApp.i)
            print('Вперед')
            ret, frame = self.video.read()
            # convert it to texture
            buf1 = cv2.flip(frame, 100)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.myimage.texture = texture1

            if self.back.state == 'down':
                TutorialApp.i = 0
                #     TutorialApp.cut = f'{TutorialApp.path}\\{TutorialApp.files[TutorialApp.i - 1]}'
                #     self.myimage.source = TutorialApp.cut
                #     self.label.text = TutorialApp.cut
                print('Назад')

    def build(self):
        self.layout = MDBoxLayout(orientation="vertical",
                                  md_bg_color=[.0, .9, .9, .1],
                                  spacing=5
                                  )
        self.label = MDLabel(theme_text_color="Custom",
                             text=f'{TutorialApp.i}',
                             size_hint=(1, .06),
                             text_color='#003153',
                             text_size='48sp',
                             halign='center',
                             opacity=.8,
                             )
        self.video = cv2.VideoCapture(f'rtsp://admin:123.qwe.@192.168.1.64/H264?ch=1&subtype=')
        Clock.schedule_interval(self.button_pressed, 1.0 / 300.0)
        self.myimage = Image(source=TutorialApp.cut,
                             pos_hint={'top': 1},
                             size_hint=(1, 1))
        self.forward = MDRaisedButton(theme_text_color='Custom',
                                      text="Старт",
                                      text_color='#223153',
                                      font_size=28,
                                      size_hint=(.12, .07),
                                      md_bg_color=[.1, .5, .9, .1],
                                      radius=5,
                                      pos_hint={'right': 1}
                                      )
        self.back = MDRaisedButton(theme_text_color='Custom',
                                   text="Стоп",
                                   text_color='#223153',
                                   font_size=28,
                                   size_hint=(.12, .07),
                                   md_bg_color=[.9, .2, .1, .3],
                                   radius=5,
                                   pos_hint={'right': 1})
        self.forward.bind(on_press=self.button_pressed)
        self.back.bind(on_press=self.button_pressed)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.myimage)
        self.layout.add_widget(self.forward)
        self.layout.add_widget(self.back)

        return self.layout


TutorialApp().run()
# img = cv2.imread(f'{TutorialApp.cut}', -1)
# imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnt = contours[10]
# cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
# cv2.imshow('123', imgray)
# cv2.waitKey(0)


# cap.release()
# cv2.destroyAllWindows()
