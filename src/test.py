# -*- coding: UTF-8 -*-
import json
from urllib import request
from bs4 import BeautifulSoup
if __name__ == '__main__' :



            url = "http://localhost/status"
            response = request.urlopen(url)
            text = response.read().decode()
            print(text)





