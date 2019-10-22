from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
#from kivy.uix.camera import Camera
from kivy.core.text import LabelBase
from kivy.uix.recycleview import RecycleView

from kivy.lang import Builder

from kivy.properties import NumericProperty
from kivy.clock import Clock

import time

import os

LabelBase.register(name= "OpenSans",
                   fn_regular= "OpenSans-Regular.ttf"
                   )
LabelBase.register(name= "Fuerte",
                   fn_regular= "Fuerte-Regular.ttf"
                   )
LabelBase.register(name= "Autodestructbb",
                   fn_regular= "Autodestructbb-Regular.ttf"
                   )
LabelBase.register(name= "Mylodon",
                   fn_regular= "Mylodon-Light.otf"
                   )
LabelBase.register(name= "DSDigi",
                   fn_regular= "DS-DIGI.ttf"
                   )
LabelBase.register(name= "DSISO",
                   fn_regular= "DSISO1.otf"
                   )

class Controller(FloatLayout):
    layout_content=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MyLayout(BoxLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    time = NumericProperty(0)
    sec = NumericProperty(0)
    min = NumericProperty(0)

    def tick(self, *_):
        self.time +=1
        self.min = self.time // 60
        self.sec = self.time % 60

    def start(self, *_):
        self.cb = Clock.schedule_interval(self.tick, 1)

    def reset(self, *_):
        Clock.unschedule(self.cb)
        self.time = 0
        self.min = 0
        self.sec = 0

    def __init__(self,**kwargs):
        super(MyLayout,self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", title_font="DSISO", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class MyApp(App):
    def build(self):
        return MyLayout()

Factory.register('MyLayout', cls=MyLayout)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == "__main__":
    MyApp().run()
