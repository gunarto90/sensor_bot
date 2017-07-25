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
    func.read_config()
    ### Print out setting variables
    print(var.variables)
    print(var.apis)
    print(var.jieba)
    out = func.log('test')
    print(str(out))
    
    test_fb()
    test_text_cn()

def test_fb():
    fb_recipient = '1880931025257113'
    message = 'This message is sent from testing.py for a testing purpose only.'
    bot_answer = 'The answer is generated from testing.py just to store the data into database.'
    out = func.log_messenger_db(fb_recipient, message, bot_answer)
    print(str(out))
    out = func.send_message(fb_recipient, message)
    print(str(out))

def test_text_cn():
    out = text_cn.init_jieba()
    print(str(out))
    qa_text_file = './qa_dataset/QA.txt'
    ### TODO: Need to set default
    var.qas["QUESTIONS"], var.qas["ANSWERS"] = text_cn.open_qa_file(qa_text_file)
    var.qas["KEYWORDS"], keyword_set, num_of_keyword = text_cn.extract_keywords(var.qas["QUESTIONS"])
    print(var.qas)

if __name__ == '__main__':
    test_functions()