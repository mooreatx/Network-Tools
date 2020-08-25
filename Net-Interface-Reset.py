#! python3
# Net-Interface-Reset -- Logs into device and shut/no shut interface ports
# listed in text file

import os, sys, re, getpass, time, paramiko
from netmiko import ConnectHandler

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\')



# Function  requests login into device and iterates through list of interfaces
# to run the shut/no shut command on
def intReset():

    # Import list of interfaces to poll
    filename = input('Enter text file name with interfaces: ' )
    file = open(filename, 'r')
    file_read = file.read()
    int_list = file_read.split(',')
    
    
    device = input('Enter IP of device: ')
    username = input('Enter in your username: ')
    password = getpass.getpass('Enter in your password: ')
            
    # Confirm that correct IP Address format is used
    # TODO: Use correct RFC format for IP addresses
    non_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']
    res = any(non in device for non in non_characters)    
    ipformat_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    ipformat = ipformat_regex.search(device)
            

    if not device:
        print('\nIP Address needed, exiting...')
        print()
        return
            
    if ipformat == None:
        print('\nPlease us correct IP address format, exiting...')
        print()
        return
                
    if res == True:
        print('\nPlease us correct IP address format, exiting...')
        print()
        return
    
    cisco = {
                'device_type': 'cisco_ios',
                'host': device,
                'username': username,
                'password': password,
                }
    
    net_connect = ConnectHandler(**cisco)
    net_connect.find_prompt() 
    
    for int in int_list:
        print('\n\n### Restarting Interface {} ###\n'.format(int))
        
        conf_int = ['int ' + int, 'shut', 'no shut']
        output = net_connect.send_config_set(conf_int)
        print(output)


    print('Interfaces service on {} restarted successfully\n'.format(device))
    
    return
    


intReset()
