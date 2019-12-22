#! python3
# MGCPrestart.py logs into voice gateway and restarts MGCP service

import os, sys, getpass, time
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


			# TODO: Exception handling if wrong input is entered

			device = input('Enter IP of voice gateway: ')
	
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
		except KeyboardInterrupt:
			sys.exit('\n\nGoodbye!\n')
restart()