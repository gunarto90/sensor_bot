#!/usr/bin/python

def test():
    message = 'test'
    return message

def test_print(message):
    try:
        print message
        return 'OK'
    except Exception as ex:
        return str(ex)

if __name__ == '__main__':
    test()