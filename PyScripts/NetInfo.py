#! python3
# NetInfo.py logs into network device and saves device info to text file

import os, sys, re, getpass
from netmiko import ConnectHandler

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\NetInfo')

def netinfo():
	while True:
		# Some Exception Handling
		try:
			device = input('Enter IP of network device: ')
			text_file = input('Enter name of text file: ')
			document = open(text_file, 'w')
			
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
			print('\n\n### Retrieve Version, Run-Config, Inventory, and License info for Network Device ###\n')
			username = input('Enter in your username: ')
			password = getpass.getpass('Enter in your password: ')
	
			cisco = {
				'device_type': 'cisco_ios',
				'host': device,
				'username': username,
				'password': password,
				}
	
			net_connect = ConnectHandler(**cisco)

			# Show Command variables and output
			net_connect.find_prompt()

			sh_ver = net_connect.send_command("sh ver")
			sh_run = net_connect.send_command("sh run")
			sh_inv = net_connect.send_command("sh inv")
			sh_lic = net_connect.send_command("sh lic")

			print('\n\n{}\n\n\n\n'.format(sh_ver))
			print('\n\n{}\n\n\n\n'.format(sh_run))
			print('\n\n{}\n\n\n\n'.format(sh_inv))
			print('\n\n{}\n\n\n\n'.format(sh_lic))

			# Save results to text file name
			document.write(sh_ver + '\n' + '-----------' * 12 + '\n' + sh_run + '\n' + '-----------' * 12 + '\n' + sh_inv + '\n' + '-----------' * 12 + '\n' + sh_lic + '\n' + '-----------' * 12 + '\n')
			document.close()
			print('\nResults saved for {}\n'.format(device))
		# Some Exception Handling - TODO: Add more multiple Execption handling alerts
		except KeyboardInterrupt:
			sys.exit('\n\nGoodbye!\n')
netinfo()