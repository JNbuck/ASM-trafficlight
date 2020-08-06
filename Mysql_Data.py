import pymysql

def connection(database_key):
    "登录程序"

    mysql = {'host': '', 'port': 3306, 'user': 'root', 'passwd': '', 'db': '', 'charset': 'utf8'}

    if database_key == 'test':
        mysql['host'] = 'localhost'
        mysql['passwd'] = '991229'
        mysql['db'] = 'trafficlight'

    if database_key == 'test1':
        mysql['host'] = '190c8d81.nat123.cc' #该项需要重新修改
        mysql['port'] = 25902   #该项需要重新修改
        mysql['passwd'] = '991229'
        mysql['db'] = 'trafficlight'

    return mysql


