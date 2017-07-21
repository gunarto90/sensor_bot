#!/usr/bin/python

import setting_variables as var
import app_function as func
import text_cn

def test():
    message = 'test'
    return message

def test_print(message):
    try:
        print message
        return 'OK'
    except Exception as ex:
        return str(ex)

def test_functions():    
    ### Initialize configuration
    json_filename = 'app_setting.json'
    func.read_config(json_filename)
    ### Print out setting variables
    print(var.variables)
    out = func.log('test')
    print(str(out))
    fb_recipient = '1880931025257113'
    message = 'message123'
    bot_answer = 'answer456'
    out = func.log_messenger_db(fb_recipient, message, bot_answer)
    print(str(out))
    out = func.send_message(fb_recipient, message)
    print(str(out))

if __name__ == '__main__':
    test_functions()