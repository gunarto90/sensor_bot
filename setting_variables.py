variables = {}
### Global variables
variables["FB_API_URL"] = 'https://graph.facebook.com/v2.6/me/messages'
variables["JSON_FILENAME"] = 'app_setting.json'
variables["DEBUG"] = True

apis = {}
### Credential
apis["USER"] = 'user'
apis["PASS"] = 'pass'
### API settings
apis["API_HOST"] = 'host'
apis["API_PORT"] = 0
### Database settings
apis["DB_HOST"] = 'host'
apis["DB_PORT"] = 0
apis["SCHEMA"] = 'db'
apis["MESSENGER_TABLE"] = 'messenger'

qas = {}
### Text mining variables
qas["QUESTIONS"] = None
qas["ANSWERS"] = None
qas["KEYWORDS"] = None
qas["KEYWORDS_SET"] = None

jieba = {}
jieba["TOPK"] = 20
jieba["WEIGHT_ENABLE"] = False
jieba["ALLOW_POS"] = ()
jieba["STOP_WORDS_FILENAME"] ='jieba_dict/stop_words.txt'
jieba["IDF_FILENAME"] = 'jieba_dict/idf.txt.big'