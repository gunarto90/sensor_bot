#!/usr/bin/python
# coding=utf-8
import jieba
import jieba.analyse
import codecs
import setting_variables as var
import testing
import app_function as func

default_message = "找不到符合的答案"

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

def qa_answering(sentence, answer_db=None, keywords_db=None):
    if answer_db is None:
        answer_db=var.qas["ANSWERS"]
    if keywords_db is None:
        keywords_db=var.qas["KEYWORDS_SET"]
    words = segment(sentence)
    given_answer, confidence = get_answer(words, answer_db, keywords_db, algo='frequency')
    return given_answer, confidence

def get_answer(words, answer_db, keywords_db, algo='frequency'):
    scores = {}
    given_answer = default_message
    confidence = 0.0
    # print words, len(words)
    for word in words:
        for i in range(0, len(keywords_db)):
            if word in keywords_db[i]:
                found = scores.get(i)
                if found is None:
                    found = 0
                if algo == 'frequency':
                    found += 1.0
                elif algo == 'ratio':
                    found += 1.0 / len(keywords_db[i])
                else:
                    found += 1.0
                scores[i] = found
            # if scores.get(i) is not None:
            #     print keywords_db[i], len(keywords_db[i]), scores[i]

    if len(scores) > 0:
        index = max(scores, key=scores.get)
        given_answer = answer_db[index]
        if algo == 'frequency':
            confidence = scores[index]
        elif algo == 'ratio':
            confidence = scores[index]*100
        else:
            confidence = scores[index]
    else:
        given_answer = default_message
        confidence = 100.0
    return given_answer, confidence

if __name__ == '__main__':
    ### Initialize configuration
    func.system_init()
    testing.test_qa()