import sqlite3
from sqlmap_api_test import AutoSqli


DATABASE = './database.db'
SqlMapServer = 'http://192.168.1.82:8775'
conn = sqlite3.connect(DATABASE)
task = AutoSqli(SqlMapServer)

while True:
	


