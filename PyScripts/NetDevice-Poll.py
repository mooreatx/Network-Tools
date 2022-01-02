#! python3
# NetDevice-Poll -- Checks to see if list network devices and save results to 
# file

import os, datetime

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\Templates\\')

# Import list of devices to poll
file = open('devicelist.txt', 'r')
content = file.read()
content_list = content.split(',')

# Function iterates through list and checks if device is live
# Write results to log file
def poller(devices):

	# Get current time
	currenttime = datetime.datetime.now()
	
	# Create log file to write results to
	logfile = open('devicelog.txt', 'a')
	
	device_count = 0
	
	for dev in devices:
		poll_response = os.system('ping {}'.format(dev))
		device_count += 1
		
		if poll_response == 0:
			print('\nResponsive\n')
			poll_result = ('\n{} is responsive at {}'.format(dev, currenttime))
			results = logfile.write(poll_result)
		else:
			print('\nUNRESPONSIVE!!!\n')
			poll_result = ('\n{} is UNRESPONSIVE!!! at {}'.format(dev, currenttime))
			results = logfile.write(poll_result)
	
	print('Number of devices found: {}'.format(device_count))
	logfile.close()
	
	return
	


poller(content_list)
