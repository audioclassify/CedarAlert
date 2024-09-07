import json
import pprint

def cedar_vars_json_obj():

	#
	# 1. This file should be in a secure folder on a secure computer.
	#
	# 2. No JSON values may be "UPDATEME".
	#
	# 3. No JSON values may be empty ("").
	#
	# 4. No CedarAlert processes will run with an "UPDATEME" or empty JSON value.
	#
	# 5. If you have disabled email or sms you must still enter values other than "UPDATEME" (e.g. "disabled').
	#
		
	cj 								= json.loads("{}")
	
	cj['cedar_user'] 				= "cedar"
	cj['cedar_home'] 				= "/home/cedar/CedarAlert"
	
	cj['cedar_ftp_path']			= "/home/cedar/ftp"
	cj['cedar_runs_path']			= "/home/cedar/CedarAlert/runs"
	
	cj['cedar_log']					= cj['cedar_home'] + "/cedar_log.txt"
	cj['cedar_log_no_detections'] 	= True
	cj['disable_log']				= False

	cj['disable_sqlite3']			= False
			
	cj['cedar_alert_folder']		= cj['cedar_home'] + "/cedar_alert_folder"
	cj['cedar_alert_seconds']		= float(15*60)
	cj['cedar_alert_last']			= cj['cedar_home'] + "/cedar_alert_last.txt"
	
	#
	# maintenance
	#
	
	cj['cedar_maint_max']			= int(10000)   # run maintenance every 10,000 images
	cj['cedar_log_max']				= int(1000000) # each log line is about 300 characters, so max is about 300 MB

	cj['cedar_ftp_files_max']		= int(100000)  # each .jpg is about 1 MB, so 100,000 images is about 100 GB
	cj['cedar_ftp_offset']			= int(1000)    # perform maintenance for log, ftp, runs, and sqlite3 and different times

	cj['cedar_runs_max']			= int(10000)   # each .jpg is about 1 MB, so 10,000 images is about 10 GB
	cj['cedar_runs_offset']			= int(2000)    # perform maintenance for log, ftp, runs, and sqlite3 and different times

	cj['cedar_sqlite3_rows_max']	= int(1000000) # each row is about 500 bytes, so 100,000 rows is about 500 MB
	cj['cedar_sqlite3_offset']		= int(3000)    # perform maintenance for log, ftp, runs, and sqlite3 and different times
	
	#
	# email server
	#
	
	cj['cedar_email_disable']		= False;
	cj['cedar_email_server']		= "UPDATEME"
	cj['cedar_email_port']			= "UPDATEME" # unquoted port number
	cj['cedar_email_tls']			= True # True is TLS, False is SSL
	cj['cedar_email_login']			= "UPDATEME"
	cj['cedar_email_password']		= "UPDATEME"
	cj['cedar_email_from']			= "UPDATEME"
	cj['cedar_email_to']			= "UPDATEME"
	cj['cedar_email_timeout']		= 10.0
	cj['cedar_email_attempts_sleep']= int(1)
	cj['cedar_email_attempts_max']	= int(3)
	cj['cedar_email_debug_level']	= int(0)

	#
	# sms server
	#
		
	cj['cedar_sms_disable']			= False;
	cj['cedar_sms_server']			= "UPDATEME"
	cj['cedar_sms_port']			= "UPDATEME" # unquoted port number
	cj['cedar_sms_tls']				= True # True is TLS, False is SSL
	cj['cedar_sms_login']			= "UPDATEME"
	cj['cedar_sms_password']		= "UPDATEME"
	cj['cedar_sms_from']			= "UPDATEME"
	cj['cedar_sms_to']				= "UPDATEME" # Verizon is "YourCellNumber@vtest.com"
	cj['cedar_sms_timeout']			= 10.0
	cj['cedar_sms_attempts_sleep']  = int(1)
	cj['cedar_sms_attempts_max']	= int(3)
	cj['cedar_sms_debug_level']		= int(0)

	#
	# for test only
	#
	
	# cj['test1']						= ""
	# cj['test2']						= "UPDATEME"

	# cj['cedar_maint_max']			= int(4)
	# cj['cedar_log_max']				= int(10)
	# cj['cedar_ftp_files_max']		= int(20000)
	# cj['cedar_ftp_offset']			= int(1)
	# cj['cedar_sqlite3_rows_max']	= int(20)
	# cj['cedar_sqlite3_offset']		= int(2)
	
	#
	# verify no CHANGEME or empty values
	#
	
	kill_now = False
	
	# print("cedar_vars_json_obj(): before check, kill_now: %s" % kill_now)
	
	for k, v in cj.items():
		
		#print("cedar_vars_json_obj(): k: %s, v: %s" % (k, v))
		
		if v == "" or v == "UPDATEME":
			kill_now = True
			print("cedar_vars_json_obj(): ERROR k: %s, v: %s" % (k, v))
		else:
			pass
			# print("cedar_vars_json_obj(): OK    k: %s, v: %s" % (k, v))
	
	print("cedar_vars_json_obj(): after check, kill_now: %s" % kill_now)
	
	if kill_now:
		
		print('cedar_vars_json_obj(): CONFIGURATION ERROR - all CedarAlert processes will be terminated due to VALUE of "UPDATEME" or empty')
		
		import subprocess
		
		cmd1 ="sudo systemctl stop CedarAlert"
		print("cedar_vars_json_obj(): cmd1: %s" % cmd1)
		p1   = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out1 = p1.communicate()[0]
		print("cedar_vars_json_obj(): out1:\n%s" % out1.decode('UTF-8'))

		cmd2 ="sudo systemctl status CedarAlert"
		print("cedar_vars_json_obj(): cmd2: %s" % cmd2)
		p2   = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out2 = p2.communicate()[0]
		print("cedar_vars_json_obj(): out2:\n%s" % out2.decode('UTF-8'))
		
		cmd3 ="sudo pkill -9 CedarAlert"
		print("cedar_vars_json_obj(): cmd3: %s" % cmd3)
		p3   = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out3 = p3.communicate()[0]
		print("cedar_vars_json_obj(): out3:\n%s" % out3.decode('UTF-8'))
				
		cmd4 ="sudo ps aux | grep -i CedarAlert"
		print("cedar_vars_json_obj(): cmd4:\n%s" % cmd4)
		p4   = subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out4 = p4.communicate()[0]
		print("cedar_vars_json_obj(): out4: %s" % out4.decode('UTF-8'))
		
		print('cedar_vars_json_obj(): CONFIGURATION ERROR - all CedarAlert processes will be terminated due to VALUE of "UPDATEME" or empty')
		
		return
		
	return cj

def cedar_vars_json_str():
	jstr = json.dumps(cedar_vars_json_obj())
	return jstr

if __name__ == "__main__":
	
	cedar_vars_json_obj()
	
	# pprint.pp(cedar_vars_json_obj())
	
	# pprint.pp(cedar_vars_json_str())
	
	# print(cedar_vars_json_str())
	

