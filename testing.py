#!/usr/bin/python
# coding=utf-8

import setting_variables as var
import app_function as func
import text_cn
import mysql

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
    func.system_init()
    ### Print out setting variables
    # print var.variables
    # print var.apis
    # print var.jieba
    # out = func.log('test')
    # print str(out)
    
    # test_fb()
    # test_text_cn()
    # test_qa()
    test_mysql()

def test_fb():
    fb_recipient = '1880931025257113'
    message = 'This message is sent from testing.py for a testing purpose only.'
    bot_answer = 'The answer is generated from testing.py just to store the data into database.'
    out = func.log_messenger_db(fb_recipient, message, bot_answer)
    print str(out)
    out = func.send_message(fb_recipient, message)
    print str(out)

def test_text_cn():
    out = text_cn.init_jieba()
    print str(out)
    qa_text_file = './qa_dataset/QA.txt'
    ### TODO: Need to set default
    var.qas["QUESTIONS"], var.qas["ANSWERS"] = text_cn.open_qa_file(qa_text_file)
    var.qas["KEYWORDS"], var.qas["KEYWORDS_SET"], num_of_keyword = text_cn.extract_keywords(var.qas["QUESTIONS"])
    print var.qas

def test_qa():
    qq = ['正常人的血糖應該多少才正常?', 'question', 'test', '當PM2.5達標時，適合外出運動嗎?', '什麼是PM2.5?', '正常人的BMI應該多少才正常?', 'BMI怎麼計算?', 'BMI', 'BMI計算']
    for q in qq:
        a, confidence = text_cn.qa_answering(q)
        print '---'
        print q
        print a
        print confidence

def test_mysql():
    conn = mysql.connect(var.apis["DB_HOST"], var.apis["DB_PORT"], var.apis["SCHEMA"], var.apis["USER"], var.apis["PASS"])
    print conn
    sql = "insert into messenger (sender, message, bot_answer, time, timestamp) values ('1880931025257113', 'Question in testing.py', '你好', '2000-01-01 07:00:00.975645', 1000000000);"
    print sql
    result, message = mysql.query(conn, sql)
    print result
    print message
    mysql.close(conn)

if __name__ == '__main__':
    test_functions()