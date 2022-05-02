import datetime
import requests
from flask import request




defaultDay = 0

def getCurrent():
    global defaultDay
    current = datetime.date.today() + datetime.timedelta(days=defaultDay)
    if request.method == 'GET':
        if request.args.get('arrow') == '1':
            current = datetime.date.today() + datetime.timedelta(days=defaultDay-1)
            defaultDay -= 1
            if defaultDay <= 0:
                defaultDay = 0
        elif request.args.get('arrow') == '2':
            current = datetime.date.today() + datetime.timedelta(days=defaultDay + 1)
            defaultDay += 1
            if defaultDay > 7:
                defaultDay = 0
    return current, defaultDay






