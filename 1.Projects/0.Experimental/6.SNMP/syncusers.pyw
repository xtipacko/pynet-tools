#gu stands for Get User's session from BRAS
from pysnmp.hlapi import *
from customsnmpdata import *
from passextr import password
import threading
import timeit
import pymysql
import warnings

mainstart = timeit.default_timer()
warnings.filterwarnings('ignore', category=pymysql.Warning) #or 'error'

def retrive_users(bras,result):
    brasnumber = braslist.index(bras) 
    bulkquery = bulkCmd( SnmpEngine(),
                         usm_user_data,
                         bras,
                         context,
                         0, 22,
                         obj['casnUserId'],
                         obj['casnIpAddr'],
                         lexicographicMode=False)
    for row in bulkquery:
        username = row[3][0][1].prettyPrint()   
        if not username: continue
        if ' ' in username: continue
        aaausersnmpindex = row[3][0][0].prettyPrint()
        aaausersnmpindex = aaausersnmpindex.split('.')[-1]
        result[username] = { 'index':aaausersnmpindex, 'brasip':brasiplist[brasnumber] }#ADD LOCK!
            
def accessallbrases(result, braslist):
    for bras in braslist:
        retrive_users(bras,result)


def replace_users(userdict, cursor, connection):
    for user in userdict:
        qREPLACE = ('REPLACE INTO `%s` (username,aaausersnmpindex,brasip) VALUES \n' 
                    '("%s","%s","%s");' %(table_name, user, userdict[user]['index'], userdict[user]['brasip']))
        cursor.execute(qREPLACE)
    connection.commit()
    
def retrieve_users(cursor):
    qSELECT = 'SELECT username,aaausersnmpindex,brasip FROM `%s`' %table_name
    cursor.execute(qSELECT)
    return cursor.fetchall()

def convert_db_content(db_ses_content):
    result_to_return = {}
    for row in db_ses_content:
        result_to_return[row['username']] = { 'index':row['aaausersnmpindex'], 'brasip':row['brasip'] }
    return result_to_return

if __name__ == '__main__':
    #entry point here
    result = {} # {username:{userip:'__', brasnumber:'__'}}
    previous_result = {}
    usm_user_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3password')
    context = ContextData()
    table_name = 'sessions'
    accessallbrases(result, braslist)
    try:
        connection = pymysql.connect(host='localhost', 
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     database='pptpclients',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            db_ses_content = retrieve_users(cursor)
            previous_result = convert_db_content(db_ses_content)            
            zeroised_users = {user:{'index':'', 'brasip':''} for user in previous_result if user not in result} #zeroise_users = previous_result - result
            result.update(zeroised_users) #result = result + zeroised_users
            replace_users(result, cursor, connection)
    except:
        raise Exception('unknown problem during db access')
    finally:
        connection.close()

    mainstop = timeit.default_timer()
    print('%3fs' %(mainstop - mainstart))

