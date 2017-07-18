#!/usr/bin/python3
### Opening mysql through python
import pymysql

##### MySQL Connection #####
def connect(host, port, db, user, passwd):
    print('Trying to connect to {} has been established (user: {})'.format(host, user))
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8', autocommit=True)
    print('Connection to {} has been established (user: {})'.format(host, user))
    return conn

def close(conn):
    conn.close()

def query(conn, sql):
    result = []
    cur = conn.cursor()
    cur.execute(sql)
    message = 'OK'
    try:
        for row in cur:
            result.append(row)
    except Exception as ex:
        message = str(ex)
    cur.close()
    return result, message

if __name__ == '__main__':
    conn = connect('localhost', 3306, 'lalala', 'fb', 'fb')