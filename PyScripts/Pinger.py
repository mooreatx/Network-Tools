#! python3
# Ping Internal and External sites to determine if there's a current network issue

import os

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\')

def pinger():

	# External Websites to ping
	Google = 'google.com'
	Yahoo = 'yahoo.com'
	GoogleDNS = '8.8.8.8'
	
	# Internal Hosts to ping
	ausdc9500 = '172.17.1.1'
	alodc9500 = '172.17.3.129'
	auscmpub1 = 'auscmpub1'
	alocmsub1 = 'alocmsub1'
	intranet = 'home.us.tel.com'
	
	# DMZ Hosts to ping
	ausexpedge1 = 'ausexpedge1'
	
	Google_response = os.system('ping ' + Google)
	Yahoo_response = os.system('ping ' + Yahoo)
	GoogleDNS_response = os.system('ping ' + GoogleDNS)
	ausdc9500_response = os.system('ping ' + ausdc9500)
	alodc9500_response = os.system('ping ' + alodc9500)
	auscmpub1_response = os.system('ping ' + auscmpub1)
	alocmsub1_response = os.system('ping ' + alocmsub1)
	intranet_response = os.system('ping ' + intranet)
	ausexpedge1_response = os.system('ping ' + ausexpedge1)
	
	# Extenal Website Results
	print('\n\n\n\n    ### EXTERNAL WEBSITE RESULTS ###')
	if Google_response == 0:
		print('   1. Google is reachable')
	else:
		print('   1. Google is UNREACHABLE')
	if Yahoo_response == 0:
		print('   2. Yahoo is reachable')
	else:
		print('   2. Yahoo is UNREACHABLE!')
	if GoogleDNS_response == 0:
		print('   3. Google DNS is reachable')
	else:
		print('   3. Google DNS is UNREACHABLE')
	
	
	# Internal Host Results
	print('\n\n    ### INTERNAL HOST RESULTS ###')
	if ausdc9500_response == 0:
		print('   1. aus-dc-9500 is reachable')
	else:
		print('   1. aus-dc-9500 is UNREACHABLE!')
	if alodc9500_response == 0:
		print('   2. alo-dc-9500 is reachable')
	else:
		print('   2. alo-dc-9500 is UNREACHABLE!')
	if auscmpub1_response == 0:
		print('   3. Austin CUCM is reachable')
	else:
		print('   3. Austin CUCM is UNREACHABLE!')
	if alocmsub1_response == 0:
		print('   4. Aloclek CUCM is reachable')
	else:
		print('   4. Aloclek CUCM is UNREACHABLE!')
	if intranet_response == 0:
		print('   5. Intranet is reachable')
	else:
		print('   5. Intranet is UNREACHABLE!')


	# DMZ Host Results
	print('\n\n    ### DMZ HOST RESULTS ###')
	if ausexpedge1_response == 0:
		print('   1. Austin Expressway-E is reachable')
		print('\n\n')
	else:
		print('   1. Austin Expressway-E is UNREACHABLE!')
		print('\n\n')
	
pinger()