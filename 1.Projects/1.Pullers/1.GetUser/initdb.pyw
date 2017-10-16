import pymysql
import warnings
from passextr import password

warnings.filterwarnings('ignore', category=pymysql.Warning) #or 'error'

connection = pymysql.connect(host='localhost', 
                               user='root',
                               password=password,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
db_name = 'pptpclients'
table_name = 'sessions'
qCREATE_DB = ( 'CREATE DATABASE IF NOT EXISTS %s;\n' 
               'USE %s;' %(db_name, db_name))
qCREATE_TABLE = ('CREATE TABLE IF NOT EXISTS %s\n'
                 '(username VARCHAR(32) NOT NULL,\n'
                 ' aaausersnmpindex VARCHAR(32) DEFAULT \'\',\n'
                 ' brasip VARCHAR(32) DEFAULT \'\',\n'
                 ' PRIMARY KEY (username)\n'
                 ') ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;' %table_name)
try:
    with connection.cursor() as cursor:
        cursor.execute(qCREATE_DB)
        cursor.execute(qCREATE_TABLE)
        connection.commit() 
        print(qCREATE_DB)
        print(qCREATE_TABLE)
        print('succesfully')
finally:
    connection.close()