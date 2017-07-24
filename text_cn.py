#!/usr/bin/python
# coding=utf-8
import jieba
import jieba.analyse
import codecs
import setting_variables as var
from app_function import *

# default_message = "找不到符合的答案"

def init_jieba(stop_words_filename=None, idf_filename=None):
    if stop_words_filename is None:
        stop_words_filename = var.jieba["STOP_WORDS_FILENAME"]
    if idf_filename is None:
        idf_filename = var.jieba["IDF_FILENAME"]
    try:
        jieba.analyse.set_stop_words(stop_words_filename)
        jieba.analyse.set_idf_path(idf_filename)
    except Exception as ex:
        return str(ex)
    return 'OK'

def open_qa_file(filename):
    question_set = []
    answer_set = []
    i = 0
    with codecs.open(filename,'r',encoding='utf8') as fr:
        for line in fr:
            text = line.strip()
            if i % 2 == 0:
                question_set.append(text)
            else:
                answer_set.append(text)
            i += 1
    return question_set, answer_set

def segment(question):
    topK = var.jieba["TOPK"]
    withWeight = var.jieba["WEIGHT_ENABLE"]
    allowPOS = var.jieba["ALLOW_POS"]
    words = jieba.analyse.extract_tags(question, topK=topK, withWeight=withWeight, allowPOS=allowPOS)
    return words

def extract_keywords(question_set):
    keyword_set = [] 
    num_of_keyword = []
    keywords = []

    for i in range(len(question_set)):
        words = segment(question_set[i])
        keyword_set.append(words)
        num_of_keyword.append(len(words))
        keywords.extend(words)

    return keywords, keyword_set, num_of_keyword

def qa_answering(sentence, answer_db=None, keyword_set_db=None):
    if answer_db is None:
        answer_db=var.qas["ANSWERS"]
    if keyword_set_db is None:
        keyword_set_db=var.qas["KEYWORDS"]
    scores = {}
    words = segment(sentence)
    for word in words:
        for i in range(len(keyword_set_db)):
            if word in keyword_set_db[i]:
                found = scores.get(i)
                if found is None:
                    found = 0
                found += 1.0 / len(keyword_set_db[i])
                scores[i] = found
    index = max(scores, key=scores.get)
    # value = max(scores, key=scores.get)
    return answer_db[index]

if __name__ == '__main__':
    ### Initialize configuration
    read_config()
    ### Initialize jieba
    init_jieba()

    qa_text_file = './qa_dataset/QA.txt'
    ### TODO: Need to set default
    var.qas["QUESTIONS"], var.qas["ANSWERS"] = open_qa_file(qa_text_file)
    var.qas["KEYWORDS"], keyword_set, num_of_keyword = extract_keywords(var.qas["QUESTIONS"])

    qq = ['正常人的血糖應該多少才正常?']
    for q in qq:
        a = qa_answering(q)
        print a