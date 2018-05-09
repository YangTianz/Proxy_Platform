## -*- coding: utf-8 -*-

from flask import Flask, request
from Scheduler import *

app=Flask(__name__)

@app.route('/api/')
def listener():
    url=request.args.get('url')
    result_list=Scheduler(url=url)
    return result_list


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
