#! python3
# MGCPrestart.py logs into voice gateway and restarts MGCP service

import os, sys, re, getpass, time, paramiko
from netmiko import ConnectHandler

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\')

def restart():
	while True:
		try:
			# Gateway List
			print('\n### Voice Gateway List ###\n')
			print('Albany Gateway IP:	172.27.254.41')
			print('Albany VG-204 IP:	172.27.55.5')
			print('Aloclek Gateway IP:	172.17.254.117')
			print('Austin VG-202 IP:	172.27.48.7')
			print('Austin VG-204 IP:	172.27.48.6')
			print('Austin VG-310 IP:	172.27.45.5')
			print('Billerica Gateway IP:	172.17.254.190')
			print('Boise Gateway IP:	172.17.254.221')
			print('Austin BW6 IP:		172.17.254.217')
			print('Chaska VG-310 IP:	172.17.217.45')
			print('Fremont Gateway IP:	172.17.254.105')
			print('Fishkill VG-202 IP:	172.27.17.5')
			print('Lehi Gateway IP:	172.17.254.85')
			print('Malta VG-204 IP:	172.27.75.5')
			print('Manassas VG-202 IP:	172.27.16.5')
			print('Phoenix Gateway IP:	172.17.254.194')
			print('QRS Gateway IP:		172.27.254.137')
			print('\n')


			device = input('Enter IP of voice gateway: ')
			
			# Confirm that correct IP Address format is used
			# TODO: Use correct RFC format for IP addresses
			non_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']
			res = any(non in device for non in non_characters)	
			ipformat_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
			ipformat = ipformat_regex.search(device)
			

			if not device:
				print('\nIP Address needed')
				print()
				continue
			
			if ipformat == None:
				print('\nPlease us correct IP address format')
				print()
				continue
				
			if res == True:
				print('\nPlease us correct IP address format')
				print()
				continue
			
			# Username and password input --password is hidden using getpass module--
			print('\n\n### Restart MGCP Service on Voice Gateway ###\n')
			username = input('Enter in your username: ')
			password = getpass.getpass('Enter in your password: ')
	
			cisco = {
				'device_type': 'cisco_ios',
				'host': device,
				'username': username,
				'password': password,
				}
	
			net_connect = ConnectHandler(**cisco)

			net_connect.find_prompt()

			sh_ccm = net_connect.send_command("sh ccm-manager")

			print('\n\n{}\n\n\n\n'.format(sh_ccm))

			shut_mgcp = ['no mgcp']
			shut_mgcp_conf = net_connect.send_config_set(shut_mgcp)

			print('\nShutdown of MGCP on {} complete'.format(device))
			time.sleep(3)
	
			mgcp = ['mgcp']
			mgcp_conf = net_connect.send_config_set(mgcp)

			print('MGCP service on {} restarted successfully\n'.format(device))
		# Some Exception Handling
		# Failed Authentication
		except paramiko.AuthenticationException as error:
			print('\n!!! AUTHENTICATION FAILED !!!')
			print()
			continue
		except KeyboardInterrupt:
			sys.exit('\n\nGoodbye!\n')
restart()
