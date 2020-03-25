#! python3
# IOSDNS-Config.py logs into list of devices and updates DNS servers

import os, sys, re, getpass, time, paramiko
from netmiko import ConnectHandler

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\')

def config():
	"""Function loops through list of devices and runs commands to remove old
	DNS servers and add correct DNS servers. Once finished config is saved."""
	
	# TODO: Pull in Device List from text file
	device_list = ["172.17.241.194", "172.17.254.110", "172.17.254.85", 
	"172.17.254.165", "172.17.254.157", "172.17.254.194",]
	
	username = input('Enter in your username: ')
	password = getpass.getpass('Enter in your password: ')
	
	for device in device_list:
		
		cisco = {
			'device_type': 'cisco_ios',
			'host': device,
			'username': username,
			'password': password,
			}

		net_connect = ConnectHandler(**cisco)

		net_connect.find_prompt()

		sh_host = net_connect.send_command("sh run | s hostname")
		print('\n\n\n\n\n####  Connected to {}  ####\n'.format(sh_host).upper())
		
		sh_dns = net_connect.send_command("sh run | s ip name")
		print('\nCurrent ip name-server config:\n{}\n'.format(sh_dns))

		ip_domain = ['ip domain lookup']
		ip_domain_conf = net_connect.send_config_set(ip_domain)
		print('\nAdding domain lookup config\n{}\n'.format(ip_domain))

		no_name_server = ['no ip name-server']
		no_name_server_conf = net_connect.send_config_set(no_name_server)
		print('\nRemoving old ip name-server config\n{}\n'.format(no_name_server))

		name_server = ['ip name-server 172.17.40.247 172.17.211.4 172.17.40.249']
		name_server_conf = net_connect.send_config_set(name_server)
		print('\nAdding correct name-server config:\n{}\n'.format(name_server))
		
		wr_mem = ['do wr']
		wr_mem_conf = net_connect.send_config_set(wr_mem)			
		print('\nSaving Config Changes...\n\n')
		
		print('####  DNS config on {} updated successfully  ####\n'.format(sh_host).upper())
	return
				
config()