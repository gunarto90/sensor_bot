#!/usr/bin/python
import os
import sys
import json

import datetime
import time

import requests
from flask import Flask, request
from mysql import *
from setting_variables import *
from testing import test

app = Flask(__name__)

def read_config(json_filename):
    ### API global variables
    global HOST, API_PORT
    ### Database global variables
    global DB_PORT, DATABASE, USER, PASS, MESSENGER_TABLE
    ### Misc. variables
    global DEBUG
    ### Read the json config file
    with open(json_filename) as data_file:
        data = json.load(data_file)
        ### Read the config from the json file
        USER = data['USERNAME']
        PASS = data['PASSWORD']
        HOST = data['API_HOST']
        API_PORT = data['API_PORT']
        DB_PORT = data['DB_PORT']
        DATABASE = data['DATABASE']
        MESSENGER_TABLE = data['TABLE']['messenger']
        DEBUG = data['DEBUG']

@app.route('/', methods=['GET'])
@app.route('/welcome')
@app.route('/help')
@app.route('/hello')
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    hello_message = """
    Hello World <br/>
    This server is built on heroku server.
    """

    return hello_message, 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "roger that!")
                    ### Perform analytics here (any logic)
                    log_messenger_db(sender_id, message_text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass
                if messaging_event.get("optin"):  # optin confirmation
                    pass
                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    return "ok", 200

@app.route('/testing', methods=['GET'])
def testing():
    message = test()
    return message, 200

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
    r = requests.post(FB_API_URL, params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def log_messenger_db(sender, message):
    conn = None
    err_message = 'OK'
    try:
        sql = "insert into {} (sender, message, time, timestamp) values ('{}', '{}', '{}', {})".format(MESSENGER_TABLE, sender, message, datetime.datetime.now(), int(time.time()))
        log(sql)
        conn = connect(HOST, DB_PORT, DATABASE, USER, PASS)
        result, err_message = query(conn, sql)
        log(err_message)
    except Exception as ex:
        log('cannot access database: ' + str(ex))
    finally:
        if conn != None:
            conn.close()
    return err_message

if __name__ == '__main__':
    json_filename = 'mysql_setting.json'
    read_config(json_filename)
    ### App variables
    app.run(port=API_PORT, host=HOST, debug=DEBUG)