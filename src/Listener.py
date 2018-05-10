## -*- coding: utf-8 -*-

from flask import Flask, request
from Scheduler import *

app=Flask(__name__)

@app.route('/api/')
def listener():
    url=request.args.get('url')
    result=Scheduler(url=str(url))
    result_list=result.get_result()
    response=""
    for i in result_list:
        response=response+i.decode()
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
