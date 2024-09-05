import sys
import io
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from smtplib import SMTP
import multiprocessing as mp
import cedar_detect_dual
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
import multiprocessing as mp
import json
import os
import traceback
import fileinput
import subprocess
from ftfy import fix_text
from pprint import pprint

#
# cedar
#

from cedar_vars import cedar_vars_json_obj
cj = cedar_vars_json_obj()
	
import cedar_timestamp
from cedar_timestamp import ts_now
from cedar_timestamp import ts_jpg
from cedar_timestamp import ts_from_time_string

import cedar_sqlite
from cedar_sqlite import log_update_email_sms
from cedar_sqlite import sqlite_delete_old_rows

cedar_alert_seconds = float(15*60)
cedar_alert_last 	= "cedar_alert_last.txt"

cedar_maint_cnt = int(0)

class ImageHandler(FileSystemEventHandler):
 
	@staticmethod
	def on_any_event(event):
		if event.is_directory:
			return None

		elif event.event_type == 'created':
		
			#
			# create output filenames (fn_) for use with file pointers (fp_) for .jpg only
			#

			img = event.src_path
			
			if img[-4:] == ".jpg":
				
				print("\n=== ImageHandler() jpg file created: % s ===\n" % event.src_path)
				
				#
				# perform maintenance every cj['cedar_maint_max'] images
				#

				global cedar_maint_cnt
				cedar_maint_cnt += 1  
				print("ImageHandler() cedar_maint_cnt: % s" % cedar_maint_cnt)
				
				if cedar_maint_cnt == cj['cedar_maint_max']:
					cedar_timestamp.log_limit()

				elif cedar_maint_cnt == cj['cedar_maint_max'] + cj['cedar_ftp_offset']:
					cedar_timestamp.ftp_limit()

				elif cedar_maint_cnt == cj['cedar_maint_max'] + cj['cedar_runs_offset']:
					cedar_timestamp.runs_limit()
					
				elif cedar_maint_cnt == cj['cedar_maint_max'] + cj['cedar_sqlite3_offset']:
					cedar_maint_cnt = int(0) # reset cedar_maint_cnt
					sqlite_delete_old_rows()
					
				image_data = ([cj['cedar_home'] + '/yolov9-s-converted.pt', img], 
							 [cj['cedar_home'] + '/yolov9-s-fire-converted.pt', img]
							 )
							 							 							 											
				image_pool_handler(image_data)		

			else:			
				#raise SystemExit("SystemExit: file type not .jpg")
				print("ImageHandler() file type not .jpg: %s" % img)

		else:
			pass
			# print("ImageHandler() event_type: %s, %s" % (event.event_type, event.src_path))				

def image_work(image_data):
	
	model = image_data[0]
	img   = image_data[1]
    
	print("\n--- image_work() start model: %s, image: %s ---\n" % (model, img))

	opt 			= cedar_detect_dual.parse_opt()
	opt.source 		= img
	opt.weights 	= model
	cedar_detect_dual.main(opt)
		
	print("\n--- image_work() end model: %s, image: %s ---\n" % (image_data[0], image_data[1]))

def image_pool_handler(image_data):
	
	try:

		p = mp.Pool(1)
		p.map(image_work, image_data)
		
	except Exception as e:

		print("=== image_pool_handler() e: %s, type(e): %s ===" % (e, type(e)))
		print("=== image_pool_handler() traceback.format_exc(): %s, type(traceback.print_exc()): %s ===" % (traceback.format_exc(), type(traceback.format_exc())))
		
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
		print("\n=== image_pool_handler() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))
		
		jstr  	= '{"exception": "image_pool_handler() Exception", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), tb_str)
		
		print("\n=== image_pool_handler() Exception, jstr: %s ===\n" % jstr)
		
		log_file_write(jstr)      

		cedar_sqlite.log_add(jstr)
		
	else:
		pass

	finally:
		pass

def update_alert_last():
	alert_last_float = time.time()
	alert_last_str	= str(alert_last_float)
	print("update_alert_last(): write(%s)" % alert_last_str)
	f_alert_last 	= open(cedar_alert_last,"w")
	f_alert_last.write(alert_last_str)
	f_alert_last.close()
	
	print("update_alert_last() return")
	return
	
class AlertEmailHandler(FileSystemEventHandler):

	@staticmethod
	#def on_modified(event):
	def on_created(event):
		
		print("\n=== AlertEmailHandler() on_created(event) event.src_path: %s ===\n" % event.src_path)
		
		f = open(event.src_path, 'r')
		jstr = f.readline()
		f.close()
		
		os.remove(event.src_path)

		#print('AlertEmailHandler(): jstr: %s' % jstr)
		#j = json.loads(jstr, strict=False)
		j = json.loads(jstr)
		print('AlertEmailHandler(): j: %s' % j)

		#
		# process_sms
		#
		
		process_sms_go = True
		process_sms_ok = True
		sleep_time  = 0.1
		
		start_time = time.time()
		print('AlertEmailHandler(): process_sms start_time: %.6f' % start_time)
		
		while process_sms_go:
			
			if process_sms_ok:
				process_sms_ok = False
				process_sms = mp.Process(target=alert_sms_process, args=(jstr,))
				process_sms.start()
			
			process_sms.join()

			if not process_sms.is_alive():
				et = time.time() - start_time
				print('AlertEmailHandler(): 1 if not process_sms.is_alive(), et: %.6f seconds' % et)
				process_sms_go = False
				break			
										
			et = time.time() - start_time
			print('AlertEmailHandler(): process_sms.is_alive(): %s, time.time(): %.6f seconds' % (process_sms.is_alive(), et))
			
			time.sleep(sleep_time)
			et = time.time() - start_time
			print('AlertEmailHandler(): process_sms elapsed: %.6f seconds' % et)

			if not process_sms.is_alive():
				et = time.time() - start_time
				print('AlertEmailHandler(): 2 if not process_sms.is_alive(), et: %.6f seconds' % et)
				process_sms_go = False
				break						
			
			too_long = (cj['cedar_sms_timeout'] * float(cj['cedar_sms_attempts_max']) * float(cj['cedar_sms_attempts_sleep'])) + float(cj['cedar_sms_attempts_max'])
			
			if time.time() - start_time >= too_long :
					
				et = time.time() - start_time
				print('AlertEmailHandler(): process_sm time.time() - start_time > cedar_email_timeout elapsed: %.6f seconds' % et)
			
				if process_sms.is_alive():
					process_sms.terminate()
					process_sms.join()
					et = time.time() - start_time
					print('AlertEmailHandler(): process_sms terminated after %.6f seconds' % et)
					process_sms_go = False
					break
				else:
					et = time.time() - start_time
					print('AlertEmailHandler(): process_sms is not alive after %.6f seconds' % et)
					process_sms_go = False							
			
		elapsed = time.time() - start_time
		print('AlertEmailHandler(): process_sms after while loop: %.6f seconds' % elapsed)
					
		#
		# process_email
		#
		
		process_email_go = True
		process_email_ok = True
		sleep_time  = 0.1
		
		start_time = time.time()
		print('AlertEmailHandler(): process_email start_time: %.6f, dt: %s' % (start_time, ts_from_time_string(start_time)))

		while process_email_go:
			
			if process_email_ok:
				process_email_ok = False
				process_email = mp.Process(target=alert_email_process, args=(jstr,))
				process_email.start()
			
			process_email.join()

			if not process_email.is_alive():
				et = time.time() - start_time
				print('AlertEmailHandler(): 1 if not process_email.is_alive(), et: %.6f seconds' % et)
				process_email_go = False
				break			
										
			et = time.time() - start_time
			print('AlertEmailHandler(): 2 process_email.is_alive() et: %s' % et)
			
			time.sleep(sleep_time)
			et = time.time() - start_time
			print('AlertEmailHandler(): 3 process_email.is_alive() et: %s' % et)

			if not process_email.is_alive():
				et = time.time() - start_time
				print('AlertEmailHandler(): 2 if not process_email.is_alive(), et: %.6f seconds' % et)
				process_email_go = False
				process_email.terminate()
				process_email.join()
				break						
			
			too_long = (cj['cedar_email_timeout'] * float(cj['cedar_email_attempts_max']) * float(cj['cedar_email_attempts_sleep'])) + float(cj['cedar_email_attempts_max'])
			
			if time.time() - start_time >= too_long:
					
				et = time.time() - start_time
				print('AlertEmailHandler(): 4 process_email time.time() - start_time > cedar_email_timeout elapsed: %.6f seconds' % et)
			
				if process_email.is_alive():
					process_email.terminate()
					process_email.join()
					et = time.time() - start_time
					print('AlertEmailHandler(): 5 process_email terminated after %.6f seconds' % et)
					process_email_go = False
					break
				else:
					et = time.time() - start_time
					print('AlertEmailHandler(): 6 process_email is not alive after %.6f seconds' % et)
					process_email_go = False							
			
		elapsed = time.time() - start_time
		print('AlertEmailHandler(): 7 process_email after while loop: %.6f seconds' % elapsed)


def replace_in_file(file_path, search_text, new_text):
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            new_line = line.replace(search_text, new_text)
            print(new_line, end='')
            
def alert_email_pool_handler(email_data):

	try:

		p = mp.Pool(1) # use one core for mail
		p.map(alert_email_process, email_data)
		
	except Exception as e:

		print("=== alert_email_pool_handler() e: %s, type(e): %s ===" % (e, type(e)))
		print("=== alert_email_pool_handler() traceback.format_exc(): %s, type(traceback.print_exc()): %s ===" % (traceback.format_exc(), type(traceback.format_exc())))
		
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
		print("\n=== alert_email_pool_handler() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))
		
		jstr  	= '{"exception": "alert_email_pool_handler() Exception", "conf":"n/a", "weights":"n/a", "source":"n/a", "save_path":"n/a", "ts":"%s", "email_ts":"n/a", "sms_ts":"n/a", "exception": "%s"}' % (ts_now(), tb_str)
		
		print("\n=== alert_email_pool_handler() Exception, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
	else:
		pass

	finally:
		pass	

def alert_email_process(email_data, attempts=int(0)):
	
	if cj['cedar_email_disable']:
		return
	
	# print("\n--- alert_email_process() email_data: %s, type(email_data): %s ---" % (email_data, type(email_data)))
	
	j = json.loads(email_data)
	# print("alert_email_process() j: %s, type(j): %s" % (j, type(j)))
	
	subject 			= "CedarAlert: " + j['alert'] + ", conf: " + j['conf']
	# print("alert_email_process() subject: %s" % subject)
	
	body 				= "weights: " + j['weights'] + "\r\n\r\nsource: " + j['source'] + "\r\n\r\nsave_path: " + j['save_path']
	body               += "\r\n\r\nAlert sent at: " + ts_now()
	# print("alert_email_process() body: %s" % body)

	# Create a multipart message and set headers
	msg 			= MIMEMultipart()
	msg["From"] 	= cj['cedar_email_from']
	msg["To"] 		= cj['cedar_email_to']
	msg["Subject"] 	= subject

	# Add body to email
	msg.attach(MIMEText(body, "plain"))

	#
	# attachment start
	#
	
	attachment_ok = True

	if(attachment_ok):

		with open(j['source'], "rb") as attachment:
			# Add file as application/octet-stream
			# Email client can usually download this automatically as attachment
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())
			
		# Encode file in ASCII characters to send by email    
		encoders.encode_base64(part)
		
		#
		# filename without path
		#
		
		filename_without_path 		= ts_jpg(j['source'])
		print("alert_email_process() attachment filename_without_path: %s" % filename_without_path)
		
		# Add header as key/value pair to attachment part
		part.add_header(
			"Content-Disposition",
			f"attachment; filename= {filename_without_path}",
		)
		
		# Add attachment to msg and convert msg to string
		msg.attach(part)

	#
	# attachment end
	#

	text = msg.as_string()
	# print("alert_email_process() email text: %s, type(text): %s" % (text, type(text)))
	
	# Log in to server using secure context and send email
	context = ssl.create_default_context()

	# print("alert_email_process() before 'with smtplib.SMTP_SSL'")
	
	if attempts >= cj['cedar_email_attempts_max']:
		
		tb_str = f"alert_email_process() attempts: {attempts}"
		jstr  = '{"exception": "' + tb_str + '", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), ts_now(), j['sms_ts'], tb_str)
		# print("\n=== alert_email_process() Exception, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
		return	
	
	try:
		
		if cj['cedar_email_tls']:

			with smtplib.SMTP(cj['cedar_email_server'], cj['cedar_email_port'], timeout=cj['cedar_email_timeout']) as server:
				
				server.set_debuglevel(cj['cedar_email_debug_level'])
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(cj['cedar_email_login'], cj['cedar_email_password'])
				server.sendmail(cj['cedar_email_from'], cj['cedar_email_to'], text)		
			
		else: # ssl
	
			with smtplib.SMTP_SSL(cj['cedar_email_server'], cj['cedar_email_port'], context=context, timeout=cj['cedar_email_timeout']) as server:
				
				server.set_debuglevel(cj['cedar_email_debug_level'])
				server.login(cj['cedar_email_login'], cj['cedar_email_password'])
				server.sendmail(cj['cedar_email_from'], cj['cedar_email_to'], text)
			
	except Exception as e:
		
		print("\n=== alert_email_process() Exception, e: %s, type(e): %s ===\n" % (e, type(e)))
		print("\n=== alert_email_process() Exception, traceback.format_exception(e): %s, type(traceback.format_exception(e)): %s ===\n" % (traceback.format_exception(e), type(traceback.format_exception(e))))
		
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
		print("\n=== alert_email_process() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))

		jstr  = '{"exception": "alert_email_process() Exception", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), ts_now(), j['sms_ts'], tb_str)
		
		print("\n=== alert_email_process() Exception, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
		time.sleep(cj['cedar_email_attempts_sleep'])
		
		alert_email_process(email_data, attempts+1)
		
	else:
		
		jstr  = '{"success": "alert_email_process()", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), ts_now(), j['sms_ts'], "Success alert_email_process()")
		# print("\n=== alert_email_process() Success, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)		
	
	finally:
		
		print("alert_email_process() finally after 'with smtplib.SMTP_SSL'")
	
	return


def alert_sms_process(email_data, attempts=int(0)):

	if cj['cedar_sms_disable']	:
		return
		
	# print("\n--- alert_sms_process() email_data: %s, type(email_data): %s ---" % (email_data, type(email_data)))
	
	j = json.loads(email_data)
	# print("alert_sms_process() j: %s, type(j): %s" % (j, type(j)))
	
	subject 			= "alert_sms_process(): " + j['alert'] + ", conf: " + j['conf'] + "\n\n" + ts_jpg(j['source'])
	# for test only with cedar_ftp_path_test
	# subject 			= "alert_sms_process(): " + j['alert'] + ", conf: " + j['conf'] + "\n\n" + ts_now() + ".jpg"
	# print("alert_sms_process() subject: %s" % subject)
	
	msg = MIMEText('plain')
 
	# setup the parameters of the message 
	msg['From'] 	= cj['cedar_sms_from']
	msg['To'] 		= cj['cedar_sms_to']
	msg['Subject'] 	= subject
	msg['Body'] 	= "Alert sent at: " + ts_now()
	
	text = msg.as_string()
	# print("alert_sms_process() sms text: %s, type(text): %s" % (text, type(text)))
	
	context = ssl.create_default_context()

	if attempts >= cj['cedar_sms_attempts_max']:
		
		tb_str = f"alert_sms_process() attempts: {attempts}"
		jstr  = '{"exception": "' + tb_str + '", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), ts_now(), j['sms_ts'], tb_str)
		# print("\n=== alert_email_process() Exception, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
		return	
			
	try:
	 
		if cj['cedar_sms_tls']:

			with smtplib.SMTP(cj['cedar_sms_server'], cj['cedar_sms_port'], cj['cedar_sms_timeout']) as server:
				
				server.set_debuglevel(cj['cedar_sms_debug_level'])
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(cj['cedar_sms_login'], cj['cedar_sms_password'])
				server.sendmail(cj['cedar_sms_from'], cj['cedar_sms_to'], text)		
			
		else: # ssl
	
			with smtplib.SMTP_SSL(cj['cedar_sms_server'], cj['cedar_sms_port'], context=context, timeout=cj['cedar_sms_timeout']) as server:
				
				server.set_debuglevel(cj['cedar_sms_debug_level'])
				server.login(cj['cedar_sms_login'], cj['cedar_sms_password'])
				server.sendmail(cj['cedar_sms_from'], cj['cedar_sms_to'], text)
				
	except Exception as e:
		
		print("\n=== alert_sms_process() Exception, e: %s, type(e): %s ===\n" % (e, type(e)))
		print("\n=== alert_sms_process() Exception, traceback.format_exception(e): %s, type(traceback.format_exception(e)): %s ===\n" % (traceback.format_exception(e), type(traceback.format_exception(e))))
		
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
		print("\n=== alert_sms_process() Exception, tb_str: %s, type(tb_str): %s ===\n" % (tb_str, type(tb_str)))

		jstr  = '{"exception": "alert_sms_process() Exception", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), j['email_ts'], ts_now(), tb_str)
		# print("\n=== alert_sms_process() Exception, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
		time.sleep(cj['cedar_sms_attempts_sleep'])
		
		alert_sms_process(email_data, attempts+1)

	else:
		
		jstr  = '{"success": "alert_sms_process()", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), ts_now(), j['sms_ts'], "Success alert_sms_process()")
		# print("\n=== alert_sms_process() Success, jstr: %s ===\n" % jstr)       

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)		
				
	finally:
		
		print("alert_sms_process() finally after 'with smtplib.SMTP_SSL'")
	
	return
	
def log_file_write(jstr):
	
	if cj['disable_log']:
		return

	f_cedar = open(cj['cedar_log'],"a")
	f_cedar.write('\n' + jstr)
	f_cedar.close()
	
if __name__ == "__main__":
	
	print('=== __main__ START at %s' % ts_now())
	print('=== __main__ cedar_ftp_path: %s' % cj['cedar_ftp_path'])
	print('=== __main__ cedar_log: %s ===' % cj['cedar_log'])
	print('=== __main__ cedar_email_timeout: %s' % cj['cedar_email_timeout'])
	print('=== __main__ cedar_alert_folder: %s' % cj['cedar_alert_folder'])
	
	keep_alive = True
		
	try:

		#
		# new images
		#

		print(f"=== __main__ start watching image directory {cj['cedar_ftp_path']!r}")
		
		image_event_handler = ImageHandler()
		image_observer 		= Observer()
		image_observer.schedule(image_event_handler, cj['cedar_ftp_path'], recursive=True)
		image_observer.start()
		
		#
		# find alerts from cedar_log
		#
		
		print(f"=== __main__ start watching cedar_alert_folder {cj['cedar_alert_folder']!r}")
			
		alert_handler = AlertEmailHandler()
		alert_observer = Observer()
		alert_observer.schedule(alert_handler, cj['cedar_alert_folder'], recursive=False)
		alert_observer.start()
			
	except Exception as e:

		print("=== ERROR __main__  image_observer or alert_handler e: %s, type(e): %s" % (e, type(e)))
		print("=== ERROR __main__  image_observer or alert_handler: %s, type(traceback.print_exc()): %s" % (traceback.format_exc(), type(traceback.format_exc())))
		
		tb = f"%s, %s" %(e, traceback.format_exc())
		tb = tb.replace('"',"")
		tb = tb.replace("'","")
		print("=== ERROR __main__  image_observer or alert_handler: %s, type(tb): %s" % (tb, type(tb)))
		
		jstr  = '{"exception": "Exception alert_email_process()", "conf":"%s", "weights":"%s", "source":"%s", "save_path":"%s", "ts":"%s", "email_ts":"%s", "sms_ts":"%s", "exception": "%s"}' % (j['conf'], j['weights'], j['source'], j['save_path'], ts_now(), j['email_ts'], j['sms_ts'], tb)
		print("=== ERROR __main__  image_observer or alert_handler jstr: %s" % jstr)    

		f_cedar = open(cj['cedar_log'],"a")
		f_cedar.write('\n' + jstr)
		f_cedar.close()

		cedar_sqlite.log_add(jstr)
		
		image_observer.stop()
		image_observer.join()		

		alert_observer.stop()
		alert_observer.join()
		
		#
		# sudo systemctl restart CedarAlert.service
		#
		
		print("=== Exception  __main__  if not keep_alive, sudo systemctl restart CedarAlert.service")
		subprocess.run(["sudo", "systemctl",  "restart", "CedarAlert.service"])

		keep_alive = False
		
	finally:
		
		while keep_alive:
			time.sleep(1)
		
