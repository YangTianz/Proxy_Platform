# -*- coding: UTF-8 -*-

from urllib import request
from bs4 import BeautifulSoup
if __name__ == '__main__' :

            url="https://www.etymonline.com/word/fuck"
            response=request.urlopen(url)
            text=response.read()
            soup=BeautifulSoup(text,"html.parser")
            sentence=""
            laji=[]
            for shit in soup.find_all('section', class_="word__defination--2q7ZH"):
                laji.append(shit)
            i=0
            for fuck in soup.find_all(class_="word__name--TTbAA"):
                sentence=sentence+fuck.get_text()+"\n"
                now=laji[i]
                for j in now.find_all('p'):
                    sentence = sentence + j.get_text()
                sentence=sentence+"\n"

                i=i+1
            print(sentence)




