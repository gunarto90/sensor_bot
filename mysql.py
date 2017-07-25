#!/usr/bin/python3
### Opening mysql through python
import pymysql
import setting_variables as var

##### MySQL Connection #####
def connect(host, port, db, user, passwd):
    if var.variables["DEBUG"]:
        log('Trying to connect to {} has been established (user: {})'.format(host, user))
    conn = None
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8', autocommit=True)
    except Exception as ex:
        if var.variables["DEBUG"]:
            log(str(ex))
        if conn is not None:
            close(conn)
    if var.variables["DEBUG"]:
        log('Connection to {} has been established (user: {})'.format(host, user))
    return conn

def close(conn):
    try:
        conn.close()
        return 'OK'
    except Exception as ex:
        return str(ex)

def query(conn, sql):
    if conn is None:
        return None, "No connection to the mysql server"
    result = []
    cur = conn.cursor()
    cur.execute("set names utf8;")
    cur.execute(sql)
    message = 'OK'
    try:
        for row in cur:
            result.append(row)
    except Exception as ex:
        message = str(ex) + ' (provided sql query was: [' + sql + ']'
    cur.close()
    return result, message

if __name__ == '__main__':
    conn = connect('localhost', 3306, 'lalala', 'fb', 'fb')
    close(conn)