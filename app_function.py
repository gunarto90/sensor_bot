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
import text_cn
from testing import *

def run_testing():
    message = test()
    test_functions()
    return message

def system_init():
    ## Initialize configuration
    read_config()
    ### Initialize jieba
    text_cn.init_jieba()
    ### Initialize qa
    qa_text_file = './qa_dataset/QA.txt'
    var.qas["QUESTIONS"], var.qas["ANSWERS"] = text_cn.open_qa_file(qa_text_file)
    var.qas["KEYWORDS"], var.qas["KEYWORDS_SET"], num_of_keyword = text_cn.extract_keywords(var.qas["QUESTIONS"])

def read_config(json_filename=None):
    if json_filename is None:
        json_filename = var.variables["JSON_FILENAME"]
    ### Read the json config file
    with open(json_filename) as data_file:
        data = json.load(data_file)
        ### Read the config from the json file
        var.apis["USER"] = data['USERNAME']
        var.apis["PASS"] = data['PASSWORD']
        var.apis["API_HOST"] = data['API_HOST']
        var.apis["API_PORT"] = data['API_PORT']
        var.apis["DB_HOST"] = data['DB_HOST']
        var.apis["DB_PORT"] = data['DB_PORT']
        var.apis["SCHEMA"] = data['DATABASE']
        var.apis["MESSENGER_TABLE"] = data['TABLE']['messenger']
        var.variables["DEBUG"] = data['DEBUG']

def log(message):  # simple wrapper for logging to stdout on heroku	
    message = unicode(message, 'utf-8')
    print message
    sys.stdout.flush()
    return 'OK'

def log_messenger_db(sender, message, bot_answer):
    conn = None
    err_message = 'OK'
    try:
        sql = "insert into {} (sender, message, bot_answer, time, timestamp) values ('{}', '{}', '{}', '{}', {})".format(var.apis["MESSENGER_TABLE"], sender, message, bot_answer, datetime.datetime.now(), int(time.time()))
        log(sql)
        conn = mysql.connect(var.apis["DB_HOST"], var.apis["DB_PORT"], var.apis["SCHEMA"], var.apis["USER"], var.apis["PASS"])
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
        "access_token": os.environ["HEROKU_FB_PAGE_ACCESS_TOKEN"]
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
    r = requests.post(var.variables["FB_API_URL"], params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    return data