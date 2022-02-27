from PyQt5 import QtCore, QtGui, QtWidgets, QtCore, Qt
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
import requests
import pickle
from PyQt5.Qt import *
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from playsound import playsound



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1075)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1920, 1070))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/NGBTR/Desktop/ПРАЭКТ/Novy_Kholst.png"))
        self.label_2.setObjectName("label_2")
        self.vivod = QtWidgets.QLineEdit(self.centralwidget)
        self.vivod.setGeometry(QtCore.QRect(700, 40, 520, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)

        
        self.vivod.setFont(font)
        self.vivod.setText("")
        self.vivod.setReadOnly(True)
        self.vivod.setObjectName("vivod")
        self.vivod.setAlignment(Qt.AlignCenter)

        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(700, 170, 420, 600))
        self.label.setText("")
        self.label.setObjectName("label")

        pixmap = QPixmap('Одежда.jpg')

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # настройки
        opts = {
            "alias": ('юпи','юпик','юбик','гуппи', 'юбки', 'yuppie'),
            "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
            "cmds": {
                "Gard1": ("подбери вещи", 'что сегодня одеть'),
                "Gard2": ("какая сегодня погода", "сколько градусов на улице"),
                "ctime": ('текущее время','сейчас времени','который час', 'сколько время'),
                "stupid1": ('как я выгляжу','как я','как я тебе'),
                "Dialog": ('привет', 'здравствуй'),
                "Dialog1": ('какой цвет мне к лицу', 'какой цвет мне подойдёт'),
                "Dialog2": ('пока', 'до встречи')
            }
        }

        # функции
        def speak(what):
            print( what )
            speak_engine.say( what )
            speak_engine.runAndWait()
            speak_engine.stop()

        def callback(recognizer, audio):
            try:
                voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
                print("[log] Распознано: " + voice)
            
                if voice.startswith(opts["alias"]):
                    # обращаются к Юпи
                    cmd = voice

                    for x in opts['alias']:
                        cmd = cmd.replace(x, "").strip()
                    
                    for x in opts['tbr']:
                        cmd = cmd.replace(x, "").strip()
                    
                    # распознаем и выполняем команду
                    cmd = recognize_cmd(cmd)
                    execute_cmd(cmd['cmd'])

            except sr.UnknownValueError:
                print("[log] Голос не распознан!")
            except sr.RequestError as e:
                print("[log] Неизвестная ошибка, проверьте интернет!")

        def recognize_cmd(cmd):
            RC = {'cmd': '', 'percent': 0}
            for c,v in opts['cmds'].items():

                for x in v:
                    vrt = fuzz.ratio(cmd, x)
                    if vrt > RC['percent']:
                        RC['cmd'] = c
                        RC['percent'] = vrt
            
            return RC

        def execute_cmd(cmd):
            if cmd == 'ctime':
                # сказать текущее время
                now = datetime.datetime.now()
                #print("Сейчас " + str(now.hour) + ":" + str(now.minute))
                self.vivod.setText("Сейчас " + str(now.hour) + ":" + str(now.minute))
                speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
                
       
            elif cmd == 'stupid1':
                # комплименты
                #a=["вы сегодня прекрасны", "вы выглядите сегодня велеколепно", 'вы как всегда великолепны', 'вы великолепны', 'вы просто ангел во плоти']
                #b=random.randint(0,len(a)-1)
                #c=a[b]
                #self.vivod.setText(c)
                playsound("Untitled.mp3")

            elif cmd == 'Dialog':
                k=['привет','здравствуй']
                l=random.randint(0, len(k)-1)
                j=k[l]
                self.vivod.setText(j)
                speak(j)

            elif cmd == 'Dialog1':
                h=['синий','красный','чёрный','белый']
                o=random.randint(0, len(h)-1)
                y=h[o]
                self.vivod.setText("я думаю, что тебе сегодня подойдёт " + y)
                speak("я думаю что тебе сегодня подойдёт " + y)
            
            elif cmd == "Gard1":
                APPID = "e38598d21a9a17fa8db23c46ad122f0b"  
                URL_BASE = "http://api.openweathermap.org/data/2.5/"


                def current_weather(q: str = "Chicago", appid: str = APPID) -> dict:
                    """https://openweathermap.org/api"""
                    return requests.get(URL_BASE + "weather", params=locals()).json()


                def weather_forecast(q: str = "Kolkata, India", appid: str = APPID) -> dict:
                    """https://openweathermap.org/forecast5"""
                    return requests.get(URL_BASE + "forecast", params=locals()).json()


                def weather_onecall(lat: float = 55.68, lon: float = 12.57, appid: str = APPID) -> dict:
                    """https://openweathermap.org/api/one-call-api"""
                    return requests.get(URL_BASE + "onecall", params=locals()).json()


                if __name__ == "__main__":
                    from pprint import pprint

                while True:
                    location = "Moscow"            
                    
                    try:
                        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                         params={'id': "524901", 'units': 'metric', 'lang': 'ru', 'APPID': "e38598d21a9a17fa8db23c46ad122f0b"})
                        data = res.json()
                        temp = float( data['main']['temp'])
                        if temp >=10 and data['weather'][0]['description']=="пасмурно":
                            print("Пасмурно, надень:")
                        elif temp <=3.0:
                            self.vivod.setText('Сегодня холодно, присмотритесь к этому варианту')
                            speak('Сегодня холодно, присмотритесь к этому варианту')
                            self.label.setPixmap(pixmap)
                            self.label.resize(pixmap.width(), pixmap.height())
                        elif temp>=3 and temp <=10:
                            self.vivod.setText('Сегодня прохладно, присмотритесь к этому варианту')
                            speak('Сегодня прохладно, присмотритесь к этому варианту')
                            
                        elif temp >=11 and temp <= 20:
                            print("Тепло, надень:")
                        elif temp >=20:
                            print("Жарко, надень:")
                    except Exception as f:
                        print("Exception (weather):", f)
                        pass
                    else:
                        break
                    break
                
            elif cmd == "Gard2":
                s_city = "Moscow,RU"
                city_id = 524901
                appid = "e38598d21a9a17fa8db23c46ad122f0b"
                try:
                    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                    data = res.json()
                    d = data['main']['temp']
                    d = int(d)
                    d = d//1
                    d = str(d)
                    d = d.replace("-", "минус ")
                    s = data['weather'][0]['description']
                    
                    speak(d)
                    speak(s)
                        
                        
                except Exception as e:
                    print("Exception (weather):", e)
                    pass


            elif cmd == 'Dialog2':
                q = ['пока', 'до встречи', 'хорошего дня']
                p=random.randint(0, len(q)-1)
                v=q[p]
                self.vivod.setText(v)
                speak(v)
                        
                        

                        
            else:
                print('Команда не распознана, повторите!')

        # запуск
        r = sr.Recognizer()
        m = sr.Microphone(device_index = 1)

        with m as source:
            r.adjust_for_ambient_noise(source)

        speak_engine = pyttsx3.init()

        # Только если у вас установлены голоса для синтеза речи!
        #voices = engine.getProperty('voices')
        #engine.setProperty('voice', voices[2].id)

        # forced cmd test
        #speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

        #speak("Добрый день, Павел")
        #speak("Юпи слушает")

        stop_listening = r.listen_in_background(m, callback)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
