#!/usr/bin/python

import app_function as func

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
    out = func.log('test')
    print(str(out))
    out = func.log_messenger_db('sender789', 'message123', 'answer456')
    print(str(out))
    out = func.send_message('recipient_id789', 'message123')
    print(str(out))

if __name__ == '__main__':
    test()