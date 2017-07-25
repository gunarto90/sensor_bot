#!/usr/bin/python
# coding=utf-8
import json
from flask import Flask, request

from app_function import *
import setting_variables as var

import text_cn

def initialize_app():
    app = Flask(__name__)
    def run_on_start(*args, **argv):
        system_init()
    run_on_start()
    return app

app = initialize_app()

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
    # try:
    #     log(var.variables)
    # except Exception as ex:
    #     log(str(ex))
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

                    bot_answer, confidence = text_cn.qa_answering(message_text, var.qas["ANSWERS"], var.qas["KEYWORDS"])
                    # bot_answer = 'OK, roger that'
                    send_message(sender_id, bot_answer)
                    ### Perform analytics here (any logic)
                    log_messenger_db(sender_id, message_text, bot_answer)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass
                if messaging_event.get("optin"):  # optin confirmation
                    pass
                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    return "ok", 200

@app.route('/testing', methods=['GET'])
def testing():
    message = run_testing()
    return message, 200

if __name__ == '__main__':
    ### Initialize webserver
    app.run(port=API_PORT, host=API_HOST, debug=var.variables["DEBUG"])
