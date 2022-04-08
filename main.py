import os
from pprint import pprint

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from cv2 import cv2
import numpy

Window.size = (1080, 720)
Window.clearcolor = (150 / 255, 128 / 255, 128 / 255, .3)



class TutorialApp(App):
    i = 0
    path = r'C:\logs'
    files = os.listdir(path)
    cut = f'{path}/{files[i]}'

    def __init__(self):
        super().__init__()
        self.back = None
        self.forward = None
        self.myimage = None
        self.label = None
        self.layout = None

    def button_pressed(self, *args):
        if self.forward.state == 'down':
            TutorialApp.i += 1
            TutorialApp.cut = f'{TutorialApp.path}\\{TutorialApp.files[TutorialApp.i + 1]}'
            self.myimage.source = TutorialApp.cut
            self.label.text = TutorialApp.cut
            self.img = cv2.imread(self.myimage.source)
            self.imgray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
            print('Вперед')
            print(self.imgray)
            Window.shape_mode = 'q.png'
        elif self.back.state == 'down':
            TutorialApp.i -= 1
            TutorialApp.cut = f'{TutorialApp.path}\\{TutorialApp.files[TutorialApp.i - 1]}'
            self.myimage.source = TutorialApp.cut
            self.label.text = TutorialApp.cut

            print('Назад')

    def build(self):
        self.layout = BoxLayout(orientation="vertical",
                                spacing=10
                                )
        self.label = Label(text=f'{TutorialApp.i}',
                           size_hint=(1, .05),
                           outline_color=[255, 255, 255],
                           color=[255, 255, 255],
                           font_size='20sp'
                           )
        self.myimage = Image(source=TutorialApp.cut)
        self.forward = Button(text="Вперед",
                              color=[255, 200, 255],
                              font_size=23,
                              size_hint=(.12, .07),
                              background_color=[128, 128, 128],
                              pos_hint={'right': 1, 'top': -1}
                               )
        self.back = Button(text="Назад",
                                color=[255, 250, 255],
                                font_size=23,
                                size_hint=(.12, .07),
                                background_color=[20, 20, 20],
                                pos_hint={'right': 1, 'top': 0}
                                )
        self.forward.bind(on_press=self.button_pressed)
        self.back.bind(on_press=self.button_pressed)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.myimage)
        self.layout.add_widget(self.forward)
        self.layout.add_widget(self.back)




        return self.layout


TutorialApp().run()
pprint(dir(Window))

# img = cv2.imread(f'{TutorialApp.cut}', -1)
# imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnt = contours[10]
# cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
# cv2.imshow('123', imgray)
# cv2.waitKey(0)