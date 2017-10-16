import pymysql
import warnings

warnings.filterwarnings('ignore', category=pymysql.Warning) #or 'error'

DBconnection = pymysql.connect(host='localhost', 
                               user='root',
                               password='there_was_passwd',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
DBcursor = DBconnection.cursor()
db_name = 'pptpclients'
qCREATE_DB = ( 'CREATE DATABASE IF NOT EXISTS %s;\n' 
               'USE %s;' %(db_name, db_name))
#print(qCREATE_DB)
DBcursor.execute(qCREATE_DB)

table_name = 'sessions'

qCREATE_TABLE = ('CREATE TABLE IF NOT EXISTS %s\n'
                 '(username VARCHAR(32) NOT NULL,\n'
                 ' aaausersnmpindex VARCHAR(32) DEFAULT \'\',\n'
                 ' PRIMARY KEY (username)\n'
                 ') ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;' %table_name)

DBcursor.execute(qCREATE_TABLE)

qINSERT_VALUES = ('REPLACE INTO `%s` (username,aaausersnmpindex) VALUES \n' 
                  '("goydoy","9999"),\n'
                  '("satisfaction","22222"),\n'
                  '("kardon","33333");' %table_name )

DBcursor.execute(qINSERT_VALUES)
DBconnection.commit() # what is it ???


qSELECT_USER  = 'SELECT username,aaausersnmpindex FROM %s WHERE username="%s"' %(table_name, username)
DBcursor.execute(qSELECT_USER)
print(DBcursor.fetchone())