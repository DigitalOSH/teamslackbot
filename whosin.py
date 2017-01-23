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
    return dbinfo


def process_message(data):
     if data['text'].startswith("!whosin"):
        info = getdbconfig()
        db = pymysql.connect(info['host'], info['user'], info['passwd'], info['dbname'])
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM games WHERE datetime > '%d' ORDER BY datetime ASC" % (time.time())
            cursor.execute(sql)
            results = cursor.fetchall()
            results = results[0]
            #gametime = results[0]
            gametime = time.strftime('%B %d, %-I:%M', time.localtime(int(float(results[0]))))
            location = results[1]
            team1 = results[2]
            team2 = results[3]
            teams = "*"+team1+" vs. "+team2+"*"
            uid = results[4]
            whosin = results[5]
            whosamaybe = results[9]
            if whosamaybe == None:
                whosamaybe = "No Maybes"
            if whosin == None:
                whosin = "No one yet\n"
        except Exception as e:
            print(e)
            outputs.append([data['channel'], "Something went wrong"])
            #quit()
        try:
            payload = "*Players in for this game:*\n"+whosin +"\n*Maybes for this game:*\n"+whosamaybe
            payload = str(payload)
            print(payload)
            outputs.append([data['channel'], payload])
        except Exception as e:
            print(e)
        db.close()
        sys.exit
