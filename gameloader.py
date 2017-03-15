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
     if data['text'].startswith("!loadgames"):
        try:
            source = data['text']
            source = source.split(" ")
            source = str(source[1])
            source = source.replace('webcal', 'http')
            source = source.replace('<','')
            source = source.replace('>','')
            info = getdbconfig()
            db = pymysql.connect(info['host'], info['user'], info['passwd'], info['dbname'])
            cursor = db.cursor()
            r=requests.get(source, verify=False)
            raw = str(r.content)
            #print(raw)
            if "BEGIN" in raw:
                raw = raw.replace("END:VEVENT", "")
                raw = raw.replace("DTSTART:", "")
                raw = raw.replace("UID:", "")
                raw = raw.replace("DTEND:", "")
                raw = raw.replace("SUMMARY:", "")
                raw = raw.replace("DESCRIPTION:", "")
                raw = raw.replace("LOCATION:", "")
                raw = raw.replace(" - Winter GAME", "")
                raw = raw.replace(" - Spring GAME", "")
                raw = raw.replace(" - Summer GAME", "")
                raw = raw.replace(" - Fall GAME", "")
                raw = raw.replace("\\\'","")
                raw = raw.replace("'","")
                raw = raw.replace("\\\,",",")
                raw = raw.replace("\\'","")
                raw = raw.split("BEGIN:VEVENT")
                for game in raw:
                    if info['team'] in game:
                        sql = "SELECT uid FROM games"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        #print(results)
                        game = game.split("\\r\\n")
                        time = game[1]
                        year = int(time[0:4])
                        month = int(time[4:6])
                        day = int(time[6:8])
                        hours = int(time[9:11])
                        mins = int(time[11:13])
                        dt = datetime.datetime(year, month, day, hours, mins)
                        dt = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
                        #dt = datetime.timestamp(dt)
                        print(dt)
                        uid = game[2]
                        uid = str(uid[0:7])
                        teams = game[4]
                        teams = teams.split(" @ ")
                        team1 = teams[0]
                        team2 = teams[1]
                        location = game[6]
                        if uid in str(results):
                            sql = "UPDATE games SET datetime = '%s', location = '%s', team1 = '%s', team2 = '%s' WHERE uid = '%s'" % (dt, location, team1, team2, uid)
                            outputs.append([data['channel'], "Updated a game"])
                            print('updated')
                            cursor.execute(sql)
                            db.commit()
                        if uid not in str(results):
                            print(datetime, location, team1, team2, uid)
                            sleep(1)
                            sql = "INSERT INTO games(datetime, location, team1, team2, uid) VALUES ('%s', '%s', '%s', '%s', '%s' )" % (dt, location, team1, team2, uid)
                            outputs.append([data['channel'], "Added new game"])
                            cursor.execute(sql)
                            db.commit()

        except Exception as e:
            print(e)
            outputs.append([data['channel'], "Something went wrong. Please make sure that's the right URL. Error: ", e])