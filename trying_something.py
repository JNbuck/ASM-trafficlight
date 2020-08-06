import numpy
from keras import backend as K
import pymysql

#打开数据库（主机地址，用户名，用户密码，数据库名）
db = pymysql.connect(host = 'localhost',user = 'root',password = '991229',db = 'trafficlight')

#使用cursor（）方法创建游标
cursor = db.cursor()

effect_row = cursor.execute("select * from address ")
print(cursor.fetchmany(4))

cursor.close()
db.close()