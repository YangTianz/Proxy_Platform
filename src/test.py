# -*- coding: UTF-8 -*-
import json
from urllib import request
from bs4 import BeautifulSoup
if __name__ == '__main__' :

            url="http://localhost/api/?url=https://www.etymonline.com/word/fuck"
            response=request.urlopen(url)
            text=response.read().decode()
            text=json.loads(text)
            print(text)





