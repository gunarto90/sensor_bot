#!/usr/bin/python
import jieba
import jieba.analyse

def init_jieba(stop_words_filename, idf_filename):
    jieba.analyse.set_stop_words(stop_words_filename)
    jieba.analyse.set_idf_path(idf_filename)


def extract_keywords(question_set):
    keyword_set = [] 
    num_of_keyword = []
    keywords = []

    for i in range(len(question_set)):
        words = jieba.analyse.extract_tags(question_set[i], topK=topK, withWeight=withWeight, allowPOS=allowPOS)
        keyword_set.append(words)
        num_of_keyword.append(len(words))
        keywords.extend(words)
    # print(keywords)
    # print(keyword_set)

    return keywords, keyword_set, num_of_keyword

if __name__ == '__main__':
    ### Initialize jieba
    stop_words_filename = 'jieba_dict/stop_words.txt'
    idf_filename = 'jieba_dict/idf.txt.big'
    init_jieba(stop_words_filename, idf_filename)