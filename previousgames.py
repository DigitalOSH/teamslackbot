<<<<<<< HEAD
import requests
import pymysql
import datetime
import time
import os
import linecache
import sys
import simplejson as json
crontable = []
outputs = []


def printexception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


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
            allgamestring = str(allgames)
            if teamname.lower() not in allgamestring.lower():
                outputs.append([data['channel'], 'No matching games found'])
            for results in allgames:
                print(results)
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
                else:
                    ourscore = str(ourscore)
                theirscore = results[7]
                if theirscore == None:
                    theirscore = ""
                else:
                    theirscore = str(theirscore)
                if info['team'] in team1:
                    us = team1
                else:
                    them = team1
                if info['team'] in team2:
                    us = team2
                else:
                    them = team2
                mvp = str(results[10])
                if teamname.lower() in teams.lower() or teamname == None:
                    if ourscore != "":
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"*Final Score*\n"+us+" - "+ourscore+" | "+them+" - "+theirscore+"\n*MVP*\n"+mvp+"\n-----------"
                    else:
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"\n-----------"
                    payload = str(payload)
                    outputs.append([data['channel'], payload])
        except Exception as e:
            printexception()
            outputs.append([data['channel'], 'Sorry, that didn\'t work'])
        db.close()
        sys.exit
=======
import requests
import pymysql
import datetime
import time
import os
import linecache
import sys
import simplejson as json
crontable = []
outputs = []


def printexception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


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
            allgamestring = str(allgames)
            if teamname.lower() not in allgamestring.lower():
                outputs.append([data['channel'], 'No matching games found'])
            for results in allgames:
                print(results)
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
                else:
                    ourscore = str(ourscore)
                theirscore = results[7]
                if theirscore == None:
                    theirscore = ""
                else:
                    theirscore = str(theirscore)
                if info['team'] in team1:
                    us = team1
                else:
                    them = team1
                if info['team'] in team2:
                    us = team2
                else:
                    them = team2
                mvp = str(results[10])
                if teamname.lower() in teams.lower() or teamname == None:
                    if ourscore != "":
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"*Final Score*\n"+us+" - "+ourscore+" | "+them+" - "+theirscore+"\n*MVP*\n"+mvp+"\n-----------"
                    else:
                        payload = teams+"\nDate: "+gametime+"\nLocation: "+location+"\n*Players in for this game:*\n"+whosin+"\n-----------"
                    payload = str(payload)
                    outputs.append([data['channel'], payload])
        except Exception as e:
            printexception()
            outputs.append([data['channel'], 'Sorry, that didn\'t work'])
        db.close()
        sys.exit
>>>>>>> 9a682d4a9cb0e715a6e90ae1d20d4019654de422
