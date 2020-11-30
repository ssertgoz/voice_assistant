import tkinter
import time
from PIL import Image, ImageTk
import numpy
import cv2
import copy
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import random
import sys
import perona




class assistant_app():
    def __init__(self):
        self.commands = ["ekle", "sil", "göster", "oku"]
        self.adjectives = ["baba", "reis", "üstad", "sahip", "efendim"]
        self.dayDictionary = {"pazartesi":"monday", "salı":"tuesday", "çarşamba":"wednesday", "perşembe":"thursday", "cuma":"friday", "cumartesi":"saturday", "pazar":"sunday"}


        #self.readFile()
        #self.writeToFile(self.readFile())
        #self.addMission("serdar","1250","mondayday")
        #self.setupList()
        #self.start()
        #self.deleteMission("serdar","1850", "sunday")


    def creatWindow(self):


        self.window.destroy()
        self.setupList()
    def setupList(self):
        missionFileList = self.readFile()
        day_count = 1
        x_cordinate = self.X_DEFOULT
        y_cordinate = self.Y_DEFOULT
        for day in missionFileList:
            missions = day[1]
            for missions_details in missions:
                if missions_details[0] == "":
                    mission_name = ""
                    mission_time = ""
                else:
                    mission_name = missions_details[0]
                    mission_time = missions_details[1]
                self.canvas.create_image(self.X_DEFOULT, self.Y_DEFOULT, image=self.img2, anchor=tkinter.NW)
                self.canvas.create_text(self.X_DEFOULT+5, self.Y_DEFOULT+5, text=mission_name, font=("Times New Roman", 8, "bold"),anchor=tkinter.NW)
                self.canvas.create_text(self.X_DEFOULT+100, self.Y_DEFOULT+5, text=mission_time[0:2]+"\n"+ mission_time[2:4], font=("Times New Roman", 10, "bold"), anchor=tkinter.NW)
                self.Y_DEFOULT += self.Y_DISTANCE
            self.X_DEFOULT += self.X_DISTANCE
            self.Y_DEFOULT = y_cordinate

    def writeToFile(self, sourceList):
        file = open("komutlar.txt", "w")
        count = 0
        mainText = ""
        for i in sourceList:
            datas = ""
            for j in range(0,len(i[1])):
                if i[1][j][0] != "":
                    i[1][j] = i[1][j][0] +"/"+ i[1][j][1]
                    if j == len(i[1])-1:
                        datas += i[1][j]
                    elif j != len(i[1])-1:
                        datas += i[1][j]+","
            sourceList[sourceList.index(i)][1] = datas
            sourceList[count] = sourceList[count][0] + ":" + sourceList[count][1] + "\n"
            # if len(sourceList)-1 != count:
            #     sourceList[count] = sourceList[count][0] + ":" +sourceList[count][1]+ "\n"
            # else:
            #     sourceList[count] = sourceList[count][0] + ":" + sourceList[count][1]
            mainText += sourceList[count]
            count +=1
        file.write(mainText)
        file.close()

    def readFile(self):
        file = open("komutlar.txt", "r")
        lines = file.readlines()
        file.close()
        tempList = []
        for line in range(0,len(lines)):
            splittedLine = lines[line].split(":")
            if splittedLine[1][(len(splittedLine[1])-2): len(splittedLine[1])] != "":
                splittedLine[1] = splittedLine[1][:(len(splittedLine[1])-1)]
           #datas = copy.deepcopy(tempList) #its not necessary
            datas = splittedLine[1].split(",")
            for i in range(0,len(datas)):
                datas[i] = datas[i].split("/")
            splittedLine[1] = datas
            tempList.append(splittedLine)
            #print(splittedLine)
        return tempList # it contains lists which its first item is day and second
                        # item is a list that contain lists which its first item is "mission name"
                        # and second item is "mission time"

    def addMission(self, missionName, missionTime, missionDay):
        missionFileList = self.readFile()
        missionDay = self.dayDictionary[missionDay]
        print(missionDay)
        tempList = []
        lastList = copy.deepcopy(missionFileList)
        missionList = copy.deepcopy(tempList)
        missionList.append(missionName)
        missionList.append(missionTime)
        for day in missionFileList:
            if day[0] == missionDay:
                if day[1][0][0] == "":
                    lastList[lastList.index(day)][1][0] = missionList
                else:
                    for i in day[1]:
                        if int(missionTime) > int(i[1]):
                            if len(day[1])-1 == day[1].index(i):
                                lastList[lastList.index(day)][1].append(missionList)

                        else:
                            lastList[lastList.index(day)][1].insert(day[1].index(i),missionList)
        self.writeToFile(lastList)

    def deleteMission(self, missionName, missionTime, missionDay):
        missionFileList = self.readFile()
        coppiedList = copy.deepcopy(missionFileList)
        missionDay = self.dayDictionary[missionDay]
        for day in missionFileList:
            if day[0] == missionDay:
                for mission in day[1]:
                    if mission[0] == missionName and mission[1] == missionTime:
                        coppiedList[missionFileList.index(day)][1].pop(day[1].index(mission))

        self.writeToFile(coppiedList)

    def speak(self, text):
        tts = gTTS(text, lang="tr")
        fileName = "voice.mp3"
        tts.save(fileName)
        playsound.playsound(fileName)
        os.remove(fileName)

    def findCommand(self, text):
        command = ""
        text = str(text)
        text = text.lower()
        wordList = text.split(" ")
        for word in wordList:
            if word in self.commands:
                command = word
                break
        return command

    def doCommand(self, text):
        missionName = ""
        missionTime = ""
        missionDay = ""
        iptal = False

        if text == "ekle":

            while not iptal:
                self.speak("Görevin adını söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev adı {}. onaylıyormusun {}".format(temp,self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionName = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            while not iptal:
                self.speak("Görevin gününü söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev günü {}. onaylıyormusun {}".format(temp, self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionDay = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            while not iptal:
                self.speak("Görevin saatini söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev saati {}. onaylıyormusun {}".format(temp, self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionTime = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            if iptal:
                self.speak("İptal ettim {}".format(self.chooseAdjective()))
            else:
                self.addMission(missionName,missionTime,missionDay)
                self.speak("görev eklendi {}".format(self.chooseAdjective()))
        if text == "sil":

            while not iptal:
                self.speak("Görevin adını söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev adı {}. onaylıyormusun {}".format(temp, self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionName = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            while not iptal:
                self.speak("Görevin gününü söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev günü {}. onaylıyormusun {}".format(temp, self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionDay = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            while not iptal:
                self.speak("Görevin saatini söyleyebilirmisin {}".format(self.chooseAdjective()))
                temp = self.listen()
                self.speak("görev saati {}. onaylıyormusun {}".format(temp, self.chooseAdjective()))
                temp2 = self.listen()
                if temp2 == "evet":
                    missionTime = temp
                    break
                elif temp2 == "hayır":
                    self.speak("tamam tekrar dinliyorum o zaman")
                elif temp2 == "":
                    self.speak("duyamadım")
                elif temp2 == "iptal":
                    iptal = True
                else:
                    self.speak("anlamadım")
            if iptal:
                self.speak("İptal ettim {}".format(self.chooseAdjective()))
            else:
                self.deleteMission(missionName, missionTime, missionDay)
                self.speak("görev silindi {}".format(self.chooseAdjective()))

    def listen(self):
        firstTime = time.time()
        finish = False
        data = ""
        while not finish:
            lastTime = time.time()
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                try:
                    data = r.recognize_google(audio, language="tr-tr")
                    data = data.lower()
                except sr.UnknownValueError:
                    pass
            if (lastTime-firstTime) > 5:
                finish = True
        print(data)
        return data
    def start(self):
        self.setupList()
        print("başladı")
        while True:
            r = sr.Recognizer()
            data = ""
            with sr.Microphone() as source:
                audio = r.listen(source)
                try:
                    data = r.recognize_google(audio, language="tr-tr")
                    data = data.lower()
                    print(data)
                    if data == "köle":
                        print("girdi")
                        self.speak("Dinliyorum {}".format(self.chooseAdjective()))
                        self.doCommand(self.listen())
                except sr.UnknownValueError:
                    pass


    def chooseAdjective(self):
        num = random.randint(0,len(self.adjectives)-1)
        return self.adjectives[num]

perona.close()
#sys.exit()
#Ui = UI()




