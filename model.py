import json
import nltk
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import keras
from keras.layers import Dense
from keras.models import Sequential
import re
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import tensorflow as tf




class text_cleaning:
    def __init__(self):
        self.data=json.load(open("intent.json"))
        self.output_respones={}
        for intend in self.data["intends"]:
            self.output_respones[intend["tags"]]=[i for i in intend["response"]]
        file=open("Outputresponses.pkl","wb")
        pickle.dump(self.output_respones,file)
        file.close()

    def text_processing(self):
        ps=PorterStemmer()
        self.allwords = []
        intent_op = []
        text = []
        for intend in self.data["intends"]:
            # print(intend["tags"])
            inte = intend["tags"]
            for p in intend["patterns"]:
                intent_op.append(inte)
                li = []
                p = re.sub(r'[^\w]', ' ', p)
                p = word_tokenize(p)
                for val in p:
                    valu = ps.stem(val.lower())
                    li.append(valu)
                    self.allwords.append(valu)
                text.append(" ".join(li))
        # print(text)
        # # print(allwords)
        # print(intent_op)
        self.df = pd.DataFrame({"Text": text, "Intent": intent_op})

    def labelencode(self):
        labelencode=LabelEncoder()
        Y=labelencode.fit_transform(self.df["Intent"])
        file=open("labelencode.pkl","wb")
        pickle.dump(labelencode,file)
        file.close()


        return Y,labelencode


    def bag_of_words(self,words,allwords):
        words = word_tokenize(words)

        data = np.zeros(len(allwords))
        for idx, value in enumerate(allwords):
            if value in words:
                data[idx] = 1

        return data


    def Xtrain(self):
        file=open("allwords.pkl","wb")
        pickle.dump(list(self.allwords),file)
        file.close()

        Xbag=[]
        for i in self.df["Text"]:
            Xbag.append(self.bag_of_words(i,self.allwords))
        return pd.DataFrame(Xbag)

    def test(self,data,allwords):
       return self.bag_of_words(data,allwords)



class Neural_net:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def NN(self):
        self.model=Sequential()
        self.model.add(Dense(units=1000,activation="relu",kernel_initializer="he_uniform",input_dim=self.x.shape[1]))
        self.model.add(Dense(units=50,activation="relu",kernel_initializer="he_uniform"))
        self.model.add(Dense(units=self.y.shape[0],activation="softmax"))
        self.model.compile(metrics=["accuracy"],loss="sparse_categorical_crossentropy")
    def fit(self):
        self.NN()
        self.model.fit(self.x,self.y,epochs=20)

    def model_save(self):
        self.model.save("chatbot.h5")

    def predict(self,X):
        yp=self.model.predict(X)
        return np.armax(yp)
if __name__=="__main__":
    textclean=text_cleaning()
    textclean.text_processing()
    Y,label=textclean.labelencode()
    X=textclean.Xtrain()
    model=Neural_net(X,Y)
    model.fit()
    model.model_save()
