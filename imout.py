import requests
import pymysql
import datetime
import time
import os
import simplejson as json

crontable = []
outputs = []


def getdbconfig():
    with open('plugins/teamslackbot/dbconfig.conf') as data_file:
        dbconf = json.load(data_file)
        dbinfo = {}
        dbinfo['host'] = dbconf['Host']
        dbinfo['user'] = dbconf['User']
        dbinfo['passwd'] = dbconf['Password']
        dbinfo['dbname'] = dbconf['DB Name']
        dbinfo['slacktoken'] = dbconf['Slack Token']
        print(dbinfo['slacktoken'])
    return dbinfo
    
def getrealname(s):
    info = getdbconfig()
    r = requests.get(info['slacktoken'])
    user = s
    userdump = json.loads(r.content)
    for member in userdump['members']:
        if member['id'] == user:
            membername = member['real_name']
            return membername

def process_message(data):
     if data['text'].startswith("!imout"):
        info = getdbconfig()
        db = pymysql.connect(info['host'], info['user'], info['passwd'], info['dbname'])
        cursor = db.cursor()
        uid = ""
        whosout = ""
        username = str(data['user'])
        realname = getrealname(username)
        print(realname)
        try:
            sql = "SELECT * FROM games WHERE datetime > '%d' ORDER BY datetime ASC" % (time.time())
            cursor.execute(sql)
            results = cursor.fetchall()
            results = results[0]
            uid = results[4]
            whosin = results[5]
            if whosin == None:
                whosin = ""
            whosout = results[8]
            if whosout == None:
                whosout = ""
            whosamaybe = results[9]
            if whosamaybe == None:
                whosamaybe = ""
            print(whosout)
        except Exception as e:
            print(e)
            outputs.append([data['channel'], "Something went wrong"])
            #quit()
        try:
            if realname in str(whosout):
                outputs.append([data['channel'], '{} was already marked as out'.format(realname)])
            else:
                whosout = whosout+realname+"\n"
                sql = "UPDATE games SET whosout = '%s' WHERE uid = '%s'" % (whosout, uid)
                outputs.append([data['channel'], '{} is out :slightly_frowning_face:'.format(realname)])
                cursor.execute(sql)
                db.commit()
        except Exception as e:
            print(e)        
        try:
            if realname in str(whosin):
                replacename = str(realname+"\n")
                whosin = whosin.replace(replacename, "")
                sql = "UPDATE games SET whosin = '%s' WHERE uid = '%s'" % (whosin, uid)
                cursor.execute(sql)
                db.commit()

        except Exception as e:
            print(e)
        try:
            if realname in str(whosamaybe):
                replacename = str(realname+"\n")
                whosamaybe = whosamaybe.replace(replacename, "")
                sql = "UPDATE games SET whosamaybe = '%s' WHERE uid = '%s'" % (whosamaybe, uid)
                cursor.execute(sql)
                db.commit()
        except Exception as e:
            print(e)
        db.close()
