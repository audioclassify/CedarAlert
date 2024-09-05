import sqlite3
from pprint import pprint
import time
import json

import cedar_timestamp
from cedar_timestamp import ts_now
from cedar_timestamp import ts_jpg
from cedar_timestamp import ts_from_float

from cedar_vars import cedar_vars_json_obj
cj = cedar_vars_json_obj()

def sqlite_connect():
	conn = sqlite3.connect("cedar_sqlite.db")
	# print("sqlite_connect() conn.total_changes: %s" % conn.total_changes)
	
	return conn

def drop_create_log_table():
	
	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
	
	sql  = "DROP TABLE IF EXISTS log;"
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)	
	
	sql  = "CREATE TABLE IF NOT EXISTS log ("
	sql += "id INTEGER PRIMARY KEY AUTOINCREMENT, "
	sql += "fa TEXT NOT NULL, " # found, alert, or exception
	sql += "name TEXT NOT NULL, "
	sql += "conf TEXT NOT NULL, "
	sql += "weights TEXT NOT NULL, "
	sql += "source TEXT NOT NULL, "
	sql += "save_path TEXT NOT NULL, "
	sql += "ts TEXT NOT NULL, "
	sql += "email_ts TEXT NOT NULL DEFAULT 'email_none', "
	sql += "sms_ts TEXT NOT NULL DEFAULT 'sms_none', "
	sql += "exception TEXT NOT NULL DEFAULT 'exception_none'"
	sql += ");"
	
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	conn.commit()
		
	sql = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	sql  = "SELECT sql FROM sqlite_schema WHERE name='log';"
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	return results
	
def query(sql):
	
	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
	
	sql  = "SELECT sql FROM sqlite_schema WHERE name='log';"
	print(sql)
	
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	return results

def log_add(jstr):
	
	if cj['disable_sqlite3']:
		return

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	#print("log_add() jstr: %s" % jstr)
		
	j    = json.loads(jstr)
	print("log_add() j: %s" % j)
	
	fa = "found"; # default
	
	if '"found"' in jstr:
		fa = "found"
	elif '"alert"' in jstr:
		fa = "alert"
	elif '"success"' in jstr: # look for success first because exception always exists
		fa = "success"
	elif '"exception"' in jstr:
		fa = "exception"
	else:
		print("ERROR: fs not found")
	
	sql  = "INSERT INTO LOG "
	sql += "(fa, name, conf, weights, source, save_path, ts, email_ts, sms_ts, exception) "
	sql += "VALUES ("
	
	# fa
	
	sql += "'" + fa + "', "
	
	# name
	
	if fa == "found":
		sql += "'" + j['found'] + "', "
	elif fa == "alert":
		sql += "'" + j['alert'] + "', "
	elif "exception" in j:
		sql += "'" + j['exception'] + "', "
	elif "success" in j:
		sql += "'" + j['success'] + "', "
							
	sql += "'" + j['conf'] + "', "
	sql += "'" + j['weights'] + "', "
	sql += "'" + j['source'] + "', "
	sql += "'" + j['save_path'] + "', "
	sql += "'" + j['ts'] + "', "
	sql += "'" + j['email_ts'] + "', "
	sql += "'" + j['sms_ts'] + "', "
	sql += "'" + j['exception'] + "'"
	sql += ");"	
	
	print("log_add() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	conn.commit()

	# sql  = "SELECT count(*) FROM log;"

	# #print("log_add() sql: %s" % sql)
	# cursor.execute(sql)
	# results = cursor.fetchall()
	# pprint(results)

	# sql  = "SELECT * FROM log WHERE source = '" + j['source'] + "';"	

	# print("log_add() sql: %s" % sql)
	# cursor.execute(sql)
	# results = cursor.fetchall()
	# pprint(results)
	
	return results
			
def log_update_email_sms(jstr):

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	print("log_update_email_sms() jstr: %s" % jstr)
		
	j    = json.loads(jstr)
	print("log_update_email_sms() j: %s" % j)
	
	ts_day_ago = float(time.time()) - 24*60*60

	sql  = "UPDATE log SET "
	sql += "ts = '" + j['email_ts'] + "', "
	sql += "sms_ts = '" + j['sms_ts'] + "' "
	sql += "WHERE "
	sql += "fa = 'alert' AND "
	sql += "email_ts = 'email_not_sent' AND "
	sql += "sms_ts = 'sms_not_sent';"

	print("log_update_email_sms() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	conn.commit()
	
	return results

def log_found_hours(hours):

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	start 		= float(time.time()) - hours * 60 * 60
	ts_start 	= ts_from_float(start)
	
	sql  = "SELECT * FROM log WHERE "
	sql += "fa = 'found' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_found_hours() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	#pprint(results)
	#print("log_found_hours() sql: %s" % sql)

	sql  = "SELECT count(*) FROM log WHERE "
	sql += "fa = 'found' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_found_hours() sql: %s" % sql)
	cursor.execute(sql)
	count = cursor.fetchall()
	#pprint(count)
		
	return {"fa":"found", "count":count, "results":results}
	
def log_alert_hours(hours):
	
	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	start 		= float(time.time()) - hours * 60 * 60
	ts_start 	= ts_from_float(start)
	
	sql  = "SELECT * FROM log WHERE "
	sql += "fa = 'alert' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts DESC;"

	#print("log_alert_hours() hours: %s, sql: %s" % (hours, sql))
	cursor.execute(sql)
	results = cursor.fetchall()
	#pprint(results)
	#print("log_alert_hours() hours() type(results): %s" % type(results))
	#print("log_alert_hours() hours: %s, sql: %s" % (hours, sql))

	sql  = "SELECT count(*) FROM log WHERE "
	sql += "fa = 'alert' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts DESC;"

	#print("log_alert_hours() hours: %s, sql: %s" % (hours, sql))
	cursor.execute(sql)
	count = cursor.fetchall()
	#pprint(count)
		
	return {"fa":"alert", "count":count, "results":results}

def log_exception_hours(hours):

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	start 		= float(time.time()) - hours * 60 * 60
	ts_start 	= ts_from_float(start)
	
	sql  = "SELECT * FROM log WHERE "
	sql += "fa = 'exception' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_exception_hours() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	#pprint(results)
	#print("log_exception_hours() sql: %s" % sql)

	sql  = "SELECT count(*) FROM log WHERE "
	sql += "fa = 'exception' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_exception_hours() sql: %s" % sql)
	cursor.execute(sql)
	count = cursor.fetchall()
	#pprint(count)
	#print("log_exception_hours() sql: %s" % sql)
		
	return {"fa":"exception", "count":count, "results":results}

def log_success_hours(hours):

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	start 		= float(time.time()) - hours * 60 * 60
	ts_start 	= ts_from_float(start)
	
	sql  = "SELECT * FROM log WHERE "
	sql += "fa = 'success' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_success_hours() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	#pprint(results)
	#print("log_success_hours() sql: %s" % sql)

	sql  = "SELECT count(*) FROM log WHERE "
	sql += "fa = 'success' AND "
	sql += "ts > '" + ts_start + "' AND ";
	sql += "ts < '" + ts_now() + "' "
	sql += "ORDER BY ts;"

	#print("log_success_hours() sql: %s" % sql)
	cursor.execute(sql)
	count = cursor.fetchall()
	#pprint(count)
	#print("log_success_hours() sql: %s" % sql)
		
	return {"fa":"success", "count":count, "results":results}
			
def log_select_all():

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
		
	sql  = "SELECT * FROM log;"	

	print("log_select_all() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	return resuls
	
def sqlite_delete_old_rows():

	conn 	= sqlite_connect()
	cursor 	= conn.cursor()
	
	sql  = "DELETE FROM log "
	sql += "WHERE id IN "
	sql += "(SELECT id FROM log ";
	sql += "ORDER BY id DESC "
	sql += f"LIMIT -1 OFFSET {cj['cedar_sqlite3_rows_max']});"

	print("sqlite_delete_old_rows() sql: %s" % sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	pprint(results)
	
	conn.commit()

	return results
		
if __name__ == "__main__":
	
	drop_create_log_table() # for test or reset only
	
	# sqlite_delete_old_rows()

	# log_select_all()
	
	# pprint(log_found_hours(24))

	# pprint(log_success_hours(24))
	
	# pprint(log_alert_hours(24))
	
	# pprint(log_exception_hours(24))
	
