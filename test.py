from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase

#added import by KCs
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import qr_scanner
from kivy.clock import Clock
from functools import partial

from kivy.properties import NumericProperty

import os
import cv2
import time
import pyzbar
import csv

#open video capture
#camera = cv2.VideoCapture(0)

#dictioner to store CSV data
container_dict = {}

#import CSV file, save the data into container dict
with open('Container List.csv', newline='') as csvfile:
    csvReader = csv.reader(csvfile, quotechar='|')
    for row in csvReader:
        container_dict[row[0]] = row[1]

print("Container Data: ")
print(container_dict)

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

    containerID = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(MyLayout,self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        #print("Loop")

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

    time = NumericProperty(0)
    sec = NumericProperty(0)
    min = NumericProperty(0)
    startTime = NumericProperty(0)

    def tick(self, *_):
        self.time += 1
        self.min = self.time // 60
        self.sec = self.time % 60

    def startTimer(self, *_):
        self.cb = Clock.schedule_interval(self.tick, 1)

    def resetTimer(self, *_):
        Clock.unschedule(self.cb)
        self.time = 0
        self.min = 0
        self.sec = 0

    #code to capture image and process qr code

    qrscanned = 0
    timeElapsed = 0


    def capture(self, *args):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        #qrstate = self.ids.qrToggle.state

        #if qrstate == "down":
            #self.ids.scanningLabel.text = "Scanner Activated..."
        camera = self.ids['camera']
        camera.export_to_png("saved_imgs/Img_new.png")
        print("Captured Image!")
        barcodeData = qr_scanner.ScanQr("saved_imgs/Img_new.png")

        if barcodeData != 0:

            self.startTime = str(self.sec)
            self.chgID(barcodeData)
            self.chgType(container_dict[str(barcodeData)])
            self.qrscanned = 1
            self.timeElapsed = 1

        else:
            if self.qrscanned == 0:
                self.chgID("No QR Code detected!")
                self.chgType("No QR Code detected!")



    #code to change text of containerID
    def chgID(self, qrID):
        self.ids.containerID.text = "Container ID: " + str(qrID)
        print("Changed ID")
        print(self.ids.containerID.text)

    def chgType(self, qrType):
        self.ids.containerType.text = "Type: " + qrType
        print("Changed type")
        print(self.ids.containerType.text)

    #start clock to ru function at fixed intervals
    def start(self):
        #Clock.unschedule(self.update)
        #Clock.schedule_interval(self.capture, 3)
        #Clock.schedule_interval(self.print_test, 0.01)
        qrstate = self.ids.qrToggle.state
        if qrstate == "down":
            self.capture()

    #function to call when toggle button is pressed
    def toggleBtn(self):
        if self.ids.qrToggle.state == "down":
            self.ids.scanningLabel.text = "Scanner Activated..."
            self.ids.scanningLabel.color = 0,0.7,0,1
        else:
            self.ids.scanningLabel.text = "Scanner De-activated..."
            self.ids.scanningLabel.color = 155, 40, 40, 1


class MyApp(App):
    def build(self):
        mylayout = MyLayout()
        mylayout.start()
        return mylayout



Factory.register('MyLayout', cls=MyLayout)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == "__main__":
    MyApp().run()
