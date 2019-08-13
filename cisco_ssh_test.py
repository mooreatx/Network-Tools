from netmiko import ConnectHandler
cisco = {
	'device_type': 'cisco_ios',
	'host': '172.17.61.131',
	'username': 'admin',
	'password': 't3lusis',
	}
	
net_connect = ConnectHandler(**cisco)

net_connect.find_prompt()

output = net_connect.send_command("show ver")

print("Testing CLI Output")
print(output)

config_commands = ['do sh log']
output_2 = net_connect.send_config_set(config_commands)

print("Testing CLI Config Commands")
print(output_2)