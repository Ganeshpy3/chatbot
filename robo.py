import pyttsx3
import datetime
import time
from selenium import webdriver
engine=pyttsx3.init()
class Bot:
    def __init__(self,username):
        self.Botname="chitti"
        self.username=username
        print("\nSome of the features may not work,it is in beta")

    def run(self):
        """ test1"""
        file1 = open("admin.txt", "r+")
        file2 = open("user.txt", "r+")
        text = file1.read()
        dic = (eval(text))
        dic2 = eval(file2.read())
        dic.update(dic2)
        file1.close()
        # print(dic)

        while True:
            a = input()
            for key , values in dic.items():
                if a.lower() in values:
                    print(key)
                    engine.say(key)
                engine.setProperty("rate",180)
                engine.setProperty("volume",0.9)
                engine.runAndWait()
                if a == "open google":
                    driver = webdriver.Chrome("chromedriver.exe")
                    driver.get("https://www.google.com/")
                    break
    def train(self,a):
        """"test 2"""
        file2 = open("user.txt", "r+")
        dic2 = eval(file2.read())
        dic2.update(a)
        file2.close()
        file=open("user.txt", "w+")
        file.write(str(dic2))
        file.close()


robo=Bot(input("enter your name"))

robo.run()

