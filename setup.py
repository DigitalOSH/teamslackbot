import pymysql
import simplejson as json
import os
try:
	os.system('echo "{}" >> dbconfig.conf')
	host = input("MySQL host: ")
	username = input("MySQL username: ")
	password = input("MySQL password: ")
	dbname = input("What would you like to name your database?: ")
	db = pymysql.connect(host, username, password)
	cursor = db.cursor()
	sql = "CREATE DATABASE %s" % (dbname)
	cursor.execute(sql)
	sql = "USE %s" % (dbname)
	cursor.execute(sql)
	sql = "CREATE TABLE games (datetime varchar(30), location varchar(200), team1 varchar(50), team2 varchar(50), uid varchar(10), whosin varchar(9999), ourscore varchar(10), theirscore varchar(10), whosout varchar(999), whosamaybe varchar(999))"
	cursor.execute(sql)
	print("Database Setup Complete")
	slackteamURL = input("Slack team URL: https://")
	slacktoken = input("Slack token (starts with xoxb): ")
	teamname = input("What is your actual team's name? (as registered with your league: ")
	payload = {}
	payload['Host'] = host
	payload['User'] = username
	payload['Password'] = password
	payload['DB Name'] = dbname
	payload['Team'] = teamname
	payload['Slack Token'] = "https://"+slackteamURL+'/api/users.list?token='+slacktoken
	print(payload['Slack Token'])
	json.dumps(payload)
	with open('dbconfig.conf', 'w') as f: f.write(json.dumps(payload))
	db.rollback()
except Exception as e:
	print(e)
	db.rollback()