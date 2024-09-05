# using datetime module
import datetime;
import time
import os
import shutil
from pathlib import Path
import sys
from pprint import pprint
import sqlite3
import json

from cedar_vars import cedar_vars_json_obj
cj = cedar_vars_json_obj()

def ts_now(): # create string that can be used for filename on Linux, Windows, and Android
	
	ts_dt = datetime.datetime.now()
	#print("ts_now() ts_dt: %s, type(ts_dt)" % ts_dt, type(ts_dt))
	
	t1 = str(ts_dt).replace(" ", "_")
	#print("ts_now() t1: %s, type(t1)" % t1, type(t1))

	t2 = str(t1).replace(".", "-")
	#print("ts_now() t2: %s, type(t2)" % t2, type(t2))
		
	ts = str(t2).replace(":", "-")
	#print("ts_now() ts: %s, type(ts)" % ts, type(ts))
	
	return ts
	
def ts_from_time_string(v): # create string that can be used for filename on Linux, Windows, and Android
		
	ts_dt = datetime.datetime.fromtimestamp(float(v))
	
	t1 = str(ts_dt).replace(" ", "_")
	#print("ts_from_time_string() t1: %s, type(t1)" % t1, type(t1))

	t2 = str(t1).replace(".", "-")
	#print("ts_from_time_string() t2: %s, type(t2)" % t2, type(t2))
		
	ts = str(t2).replace(":", "-")
	
	print("ts_from_time_string(): %s" % ts)
	
	return ts
	
def ts_from_float_arg1(): # create string that can be used for filename on Linux, Windows, and Android
	
	if len(sys.argv) > 1:
		
		ts_dt = datetime.datetime.fromtimestamp(float(sys.argv[1]))
		
		t1 = str(ts_dt).replace(" ", "_")
		#print("ts_from_float_arg1 t1: %s, type(t1)" % t1, type(t1))

		t2 = str(t1).replace(".", "-")
		#print("ts_from_float_arg1 t2: %s, type(t2)" % t2, type(t2))
			
		ts = str(t2).replace(":", "-")
		
		print("ts_from_float_arg1: %s" % ts)
		
		return ts
		
	else:
		print("ts_from_float_arg1: ERROR - exactly one float required")

def ts_from_float(var_float): # create string that can be used for filename on Linux, Windows, and Android
	
	ts_dt = datetime.datetime.fromtimestamp(var_float)

	t1 = str(ts_dt).replace(" ", "_")
	#print("ts_from_float t1: %s, type(t1)" % t1, type(t1))

	t2 = str(t1).replace(".", "-")
	#print("ts_from_float t2: %s, type(t2)" % t2, type(t2))
		
	ts = str(t2).replace(":", "-")

	#print("ts_from_float: var_float: %f.6, %s" % (var_float, ts))

	return ts
		
def cedar_alert_last_dt():
	
		f = open("cedar_alert_last.txt","r")
		cedar_alert_last_str = f.read()
		f.close()
		
		cedar_alert_last = float(cedar_alert_last_str)
		
		print("cedar_alert_last_dt() cedar_alert_last float:  %s" % cedar_alert_last)
		
		ts_dt = datetime.datetime.fromtimestamp(cedar_alert_last)

		#
		# create string that can be used for filename on Linux, Windows, and Android
		#
		
		t1 = str(ts_dt).replace(" ", "_")
		#print("cedar_alert_last_dt() t1: %s, type(t1)" % t1, type(t1))

		t2 = str(t1).replace(".", "-")
		#print("cedar_alert_last_dt() t2: %s, type(t2)" % t2, type(t2))
			
		ts = str(t2).replace(":", "-")
		
		print("cedar_alert_last_dt() cedar_alert_last string: %s" % ts)
				
def ts2timefloat(ts):
	
	t = str(ts).replace("_", " ")
	#print("ts2timefloat() t: %s, type(t)" % t, type(t))
	
	usec = t[-6:]
	#print("ts2timefloat() usec: %s, type(usec)" % usec, type(usec))
	
	t1 = time.strptime(t,'%Y-%m-%d %H-%M-%S-%f')
	#print("ts2timefloat() t1: %s, type(t1): %s" % (t1, type(t1)))
	
	t2 = time.mktime(t1)
	#print("ts2timefloat() t2: %s, type(t2): %s" % (t2, type(t2)))
	
	time_float = t2 + float(usec)/1000000
	
	#print("ts2timefloat() time_float: %s, type(time_float): %s" % (time_float, type(time_float)))
	
	return time_float
	
def ts_jpg(source):
	
	# /home/cedar/ftp/inbox/PorchEast/AMC018M7DEQ8X7DS23/2024-08-13/06hour/jpg/06.56.37[M][0@0][0].jpg
	#  1    2     3   4     5         6                  7          8      9   10
	
	l = source.split("/")
	#print("ts_jpg() l: %s, type(l): %s" % (l, type(l)))
	
	t1 = l[7] + "_" + l[10][:8].replace(".","-") + "_" + l[5] + ".jpg"
	#print("ts_jpg() t1: %s, type(t1): %s" % (t1, type(t1)))
	
	return t1

def ts_txt(source):
	
	# /home/cedar/ftp/inbox/PorchEast/AMC018M7DEQ8X7DS23/2024-08-13/06hour/jpg/06.56.37[M][0@0][0].txt
	#  1    2     3   4     5         6                  7          8      9   10
	
	l = source.split("/")
	#print("ts_jpg() l: %s, type(l): %s" % (l, type(l)))
	
	t1 = l[7] + "_" + l[10][:8].replace(".","-") + "_" + l[5] + ".txt"
	#print("ts_jpg() t1: %s, type(t1): %s" % (t1, type(t1)))
	
	return t1
	
def log_limit():
	
	print("log_limit()")
	
	old 	= int(0) # old lines
	new 	= int(0) # new lines only
	ftmp	= "/tmp/cedar_tmp.txt"
	
	with open(cj['cedar_log'],"r") as f:
		for line in f:
			old += 1

	if os.path.exists(ftmp):
	  os.remove(ftmp)
	  
	shutil.copy(cj['cedar_log'], ftmp)
	
	os.truncate(cj['cedar_log'], 0)
	
	with open(cj['cedar_log'], "a") as fo:
	
		with open(ftmp,"r") as ft:
			
			for line in ft:

				if old - new >= cj['cedar_log_max']:
					fo.write(line)
					new += 1
	
	print("log_limit() cj['cedar_log_max']: %s" % cj['cedar_log_max'])
	print("log_limit() old: %s" % old)
	print("log_limit() new: %s" % new)

def ftp_limit():
	
	n = int(0)
	x = dict([])

	for path in Path(cj['cedar_ftp_path']).rglob('*.jpg'):
		
		# if n >= 5: # for test
			# break
		
		# if n == 0: for test
		if True:
			# print("ftp_limit() path: %s" % path)
			# print("ftp_limit() path.name): %s" % path.name)
			created = os.path.getctime(path)
			# print("ftp_limit() created: %s" % created)
			# print("ftp_limit() ts_from_time_string(created): %s" % ts_from_time_string(created))
			x.update({path: created})
		
		n += 1
		
	xr = {key: value for key, value in sorted(x.items(), key=lambda item: item[1], reverse=True)}
	# print("ftp_limit() len(xr): %s" % len(xr))
		
	print("ftp_limit() image files found: %s" % n)

	i = int(0)
	for key, value in xr.items():
		
		# print("ftp_limit() xr, ts_from_time_string(value): %s, key: %s" % (ts_from_time_string(value), key))
		
		if i >= cj['cedar_ftp_files_max']:
			
			# print("ftp_limit() xr Path.unlink(%s) created at time_string(value): %s" % (key, ts_from_time_string(value)))
			
			try:
				
				Path.unlink(key) # cameras occaissionally have FTP errors and files get deleted
	
			except Exception as e:

				print("ftp_limit() Exception, e: %s, type(e): %s ===" % (e, type(e)))
				print("ftp_limit() traceback.format_exc(): %s, type(traceback.print_exc()): %s ===" % (traceback.format_exc(), type(traceback.format_exc())))
				
				tb 		= traceback.format_exception(e)
				tb_cnt 	= int(0)
				tb_str 	= ""
				for item in tb:
					item = item.replace('"',"")
					item = item.replace("'","")
					item = item.replace("\n"," ")
					item = item.replace("\r"," ")
					item = item.replace("\t"," ")
					tb_str += " ### " + str(tb_cnt) + " @@@ " + fix_text(item) + " *** "
					tb_cnt += 1
				# print("ftp_limit() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))
				
				jstr  	= '{"exception": "ftp_limit() Exception", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), tb_str)
				
				# print("ftp_limit() Exception, jstr: %s ===\n" % jstr)
				
				log_file_write(jstr)

				cedar_sqlite.log_add(jstr)
				
			else:
				
				jstr  	= '{"success": "ftp_limit() success", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), f"unlink({key}")
				print("ftp_limit() success, jstr: %s" % jstr)
				
				if not cj['disable_log']:
					f_cedar = open(cj['cedar_log'],"a")
					f_cedar.write('\n' + jstr)
					f_cedar.close() 

				sqlite_log_add(jstr)

			finally:
				pass
								
		i += 1

def runs_limit():
	
	n = int(0)
	x = dict([])

	for path in Path(cj['cedar_runs_path']).rglob('*.jpg'):
		
		# if n >= 5: # for test
			# break
		
		# if n == 0: for test
		if True:
			# print("ftp_limit() path: %s" % path)
			# print("ftp_limit() path.name): %s" % path.name)
			created = os.path.getctime(path)
			# print("ftp_limit() created: %s" % created)
			# print("ftp_limit() ts_from_time_string(created): %s" % ts_from_time_string(created))
			x.update({path: created})
		
		n += 1
		
	xr = {key: value for key, value in sorted(x.items(), key=lambda item: item[1], reverse=True)}
	# print("runs_limit() len(xr): %s" % len(xr))
		
	print("runs_limit() image files found: %s" % n)

	i = int(0)
	for key, value in xr.items():
		
		# print("runs_limit() xr, ts_from_time_string(value): %s, key: %s" % (ts_from_time_string(value), key))
		
		if i >= cj['cedar_runs_max']:
			
			# print("runs_limit()) xr Path.unlink(%s) created at time_string(value): %s" % (key, ts_from_time_string(value)))
			
			try:
				
				Path.unlink(key)
	
			except Exception as e:

				print("runs_limit() Exception, e: %s, type(e): %s ===" % (e, type(e)))
				print("runs_limit() traceback.format_exc(): %s, type(traceback.print_exc()): %s ===" % (traceback.format_exc(), type(traceback.format_exc())))
				
				tb 		= traceback.format_exception(e)
				tb_cnt 	= int(0)
				tb_str 	= ""
				for item in tb:
					item = item.replace('"',"")
					item = item.replace("'","")
					item = item.replace("\n"," ")
					item = item.replace("\r"," ")
					item = item.replace("\t"," ")
					tb_str += " ### " + str(tb_cnt) + " @@@ " + fix_text(item) + " *** "
					tb_cnt += 1
				# print("runs_limit() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))
				
				jstr  	= '{"exception": "runs_limit() Exception", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), tb_str)
				
				# print("runs_limit() Exception, jstr: %s ===\n" % jstr)
				
				log_file_write(jstr)

				cedar_sqlite.log_add(jstr)
				
			else:
				
				jstr  	= '{"success": "runs_limit() success", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), f"unlink({key}")
				print("runs_limit() success, jstr: %s" % jstr)
				
				if not cj['disable_log']:
					f_cedar = open(cj['cedar_log'],"a")
					f_cedar.write('\n' + jstr)
					f_cedar.close() 

				sqlite_log_add(jstr)

			finally:
				pass
								
		i += 1

def sqlite_connect():
	conn = sqlite3.connect("cedar_sqlite.db")
	# print("sqlite_connect() conn.total_changes: %s" % conn.total_changes)
	
	return conn
	
def sqlite_log_add(jstr):
	
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
	
	return results
	
if __name__ == "__main__":
	
	# ts = ts_now()
	# print("main ts: %s, type(ts)" % ts, type(ts))

	# #ts = "2024-08-11_11-42-47.123456"
	# time_float = ts2timefloat(ts)
	# print("main time_float: %s, type(time_float): %s" % (time_float, type(time_float)))
	
	# source = "/home/cedar/ftp/inbox/PorchEast/AMC018M7DEQ8X7DS23/2024-08-13/06hour/jpg/06.56.37[M][0@0][0].jpg"
	# fn = ts_jpg(source)
	# print("main fn: %s, type(fn): %s" % (fn, type(fn)))
	
	# fn 		= "cedar_log.txt"
	# limit 	= int(10000)

	# log_limit(fn, limit)
	
	# ftp_path = "/home/cedar/ftp/inbox"
	# ftp_limit(ftp_path)
	
	#ts_from_float()
	
	cedar_alert_last_dt()
