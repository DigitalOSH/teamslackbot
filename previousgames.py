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
        dbinfo['team'] = dbconf['Team']
    return dbinfo

def process_message(data):
     if data['text'].startswith("!previous"):
        teamname = data['text'].replace("!previous","")
        teamname = teamname.replace(" ","")
        print(teamname)
        info = getdbconfig()
        db = pymysql.connect(info['host'], info['user'], info['passwd'], info['dbname'])
        cursor = db.cursor()
        try:
            sql = "SELECT * FROM games WHERE datetime < '%d' ORDER BY datetime ASC" % (time.time())
            cursor.execute(sql)
            allgames = cursor.fetchall()
            for results in allgames:
                gametime = time.strftime('%B %d, %-I:%M', time.localtime(int(float(results[0]))))
                location = results[1]
                team1 = results[2]
                team2 = results[3]
                teams = "*"+team1+" vs. "+team2+"*"
                uid = results[4]
                whosin = results[5]
                if whosin == None:
                    whosin = "No one yet\n"
                ourscore = results[6]
                if ourscore == None:
                    ourscore = ""
                theirscore = results[7]
                if theirscore == None:
                    theirscore = ""
                if info['team'] in team1:
                    us = team1
                else:
                    them = team1
                if info['team'] in team2:
                    us = team2
                else:
                    them = team2
                if teamname.lower() in teams.lower() or teamname == None:
                    if ourscore != "":
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\nUID: "+uid+"\n*Players in for this game:*\n"+whosin+"*Final Score*\n"+us+" - "+ourscore+" | "+them+" - "+theirscore+"\n-----------"
                    else:
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\nUID: "+uid+"\n*Players in for this game:*\n"+whosin+"-----------"
                    payload = str(payload)
                    print(payload)
                    outputs.append([data['channel'], payload])
        except Exception as e:
            print(e)
        db.close()
        sys.exit
