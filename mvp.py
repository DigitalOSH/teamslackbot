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
    if data['text'].startswith("!mvp"):
        mvp = data['text'].replace("!mvp ","")
        mvp = data['text'].replace("!mvp","")
        print(mvp)
        if mvp == "":
            outputs.append([data['channel'], "Sorry, that didn't work. Correct usage: ! mvp <MVP name>"])
        else:
            try:
                info = getdbconfig()
                db = pymysql.connect(info['host'], info['user'], info['passwd'], info['dbname'])
                cursor = db.cursor()
                sql = "SELECT * FROM games WHERE datetime < '%d' ORDER BY datetime DESC" % (time.time())
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
                if whosin == None:
                    whosin = "No one yet\n"
            except Exception as e:
                print(e)
                outputs.append([data['channel'], "Something went wrong"])
            try:
                sql = "UPDATE games SET mvp = '%s' WHERE uid = '%s'" % (mvp, uid)
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
            try:
                payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"*MVP*\n"+mvp
                payload = str(payload)
                print(payload)
                outputs.append([data['channel'], payload])
            except Exception as e:
                print(e)
                outputs.append([data['channel'], "Something went wrong"])
            db.close()
            sys.exit