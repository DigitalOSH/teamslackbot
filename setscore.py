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
     if data['text'].startswith("!setscore"):
        score = data['text'].replace("!setscore","")
        score = score.replace(" ","")
        print(score)
        try:
            scores = score.split("-")
            ourscore = int(scores[0])
            theirscore = int(scores[1])
            ourscore += 1
            ourscore -= 1
            theirscore += 1
            theirscore -= 1
            ourscore = str(ourscore)
            theirscore = str(theirscore)
        except Exception as e:
            print(e)
            outputs.append([data['channel'], "Sorry, that didn't work. Correct usage: ! setscore <Our Score>-<Their Score>"])
        if score == "":
            outputs.append([data['channel'], "Sorry, that didn't work. Correct usage: ! setscore <Our Score>-<Their Score>"])
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
                #quit()
            try:
                sql = "UPDATE games SET ourscore = '%s' WHERE uid = '%s'" % (ourscore, uid)
                cursor.execute(sql)
                db.commit()
                sql = "UPDATE games SET theirscore = '%s' WHERE uid = '%s'" % (theirscore, uid)
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
            try:
                if info['team'] in team1:
                    us = team1
                else:
                    them = team1
                if info['team'] in team2:
                    us = team2
                else:
                    them = team2
                payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"*Final Score*\n"+us+" - "+ourscore+" | "+them+" - "+theirscore
                payload = str(payload)
                print(payload)
                outputs.append([data['channel'], payload])
            except Exception as e:
                print(e)
                outputs.append([data['channel'], "Something went wrong"])
            db.close()
            sys.exit
