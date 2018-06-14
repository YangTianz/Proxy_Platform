# -*- coding: UTF-8 -*-
import json
from urllib import request
from bs4 import BeautifulSoup




if __name__ == '__main__' :

            url="http://localhost/api/?url=https://www.etymonline.com/word/fuck&&session=True"
            response=request.urlopen(url)
            text=response.read().decode()
            print(text)

            url = "http://localhost/status"
            response = request.urlopen(url)
            text = response.read().decode()
            print(text)





