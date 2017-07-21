#!/usr/bin/python
# coding=utf-8
import os
import sys
import datetime
import time
import json
import requests

import mysql
import setting_variables as var
from testing import *

def run_testing():
    message = test()
    test_functions()
    return message

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()
    return 'OK'

def log_messenger_db(sender, message, bot_answer):
    conn = None
    err_message = 'OK'
    try:
        sql = "insert into {} (sender, message, bot_answer, time, timestamp) values ('{}', '{}', '{}', '{}', {})".format(var.MESSENGER_TABLE, sender, message, bot_answer, datetime.datetime.now(), int(time.time()))
        log(sql)
        conn = mysql.connect(var.DB_HOST, var.DB_PORT, var.SCHEMA, var.USER, var.PASS)
        result, err_message = mysql.query(conn, sql)
        log(err_message)
    except Exception as ex:
        log('cannot access database: ' + str(ex))
    finally:
        if conn != None:
            mysql.close(conn)
    return err_message


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post(var.FB_API_URL, params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    return data