import pandas as pd
import tensorflow as tf
import pickle
import numpy as np
import re
from nltk import PorterStemmer
from nltk.tokenize import word_tokenize
import random
import logging
from telegram.ext import *



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')
API_KEY="1802708745:AAHyDe9-j8f_adCyQU_EPt8A1yaAmxW1PnI"
updater = Updater(API_KEY, use_context=True)
dp = updater.dispatcher

class telegrambot:
    def __init__(self):
        self.model=tf.keras.models.load_model('chatbot.h5')
        file=open("allwords.pkl","rb")
        self.allwords=pickle.load(file)
        file.close()
        file1=open("labelencode.pkl","rb")
        self.label=pickle.load(file1)
        file1.close()
        file2=open("Outputresponses.pkl","rb")
        self.outputresponse=pickle.load(file2)
        file2.close()
    def text_preprocessing(self,word):
        ps=PorterStemmer()
        word=re.sub(r'[^\w]', ' ', word)
        word=word_tokenize(word)
        self.words=[]
        for i in word:
            self.words.append(ps.stem(i))
        return self.words
    def bag_of_words(self,words):
        data = np.zeros(len(self.allwords))
        for idx, value in enumerate(self.allwords):
            if value in words:
                data[idx] = 1
        return data
    def predict(self,inp):
        if len(self.model.predict(inp)[self.model.predict(inp)>0.4])>0:
            return self.label.inverse_transform([np.argmax(self.model.predict(inp))]),1
        else:
            text="Chitti: Sorry can't understand"
            return text,0
    # def chatbot(self):
    #     while True:
    #         userinp=input("You:")
    #         userinp=userinp.lower()
    #         if userinp == "exit":
    #             break
    #         word = self.text_preprocessing(userinp)
    #         X=self.bag_of_words(word)
    #         final,true=self.predict(pd.DataFrame([X]))
    #         if true:
    #             print("Chitti:",random.choice(self.outputresponse[final[0]]))
    #         else:
    #             print(final)
    def handle_message(self,update, context):
        text = str(update.message.text).lower()
        word = self.text_preprocessing(text)
        X = self.bag_of_words(word)
        final, true = self.predict(pd.DataFrame([X]))
        if true:
            # print("Chitti:",random.choice(self.outputresponse[final[0]]))
            text=random.choice(self.outputresponse[final[0]])
            update.message.reply_text(text)
        else:
            update.message.reply_text("Sorry Can't understand")

        # logging.info(f'User ({update.message.chat.id}) says: {text}')

        # Bot response
        # response = responses.get_response(text)
        # update.message.reply_text(text)


a=telegrambot()
# a.chatbot()
dp.add_handler(MessageHandler(Filters.text, a.handle_message))

updater.start_polling()
updater.idle()

# userinp="hey how are you"
# word = text_preprocessing(userinp)
# print(bag_of_words(word, allwords).reshape(1,-1).shape)
