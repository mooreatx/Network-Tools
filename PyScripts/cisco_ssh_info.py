from netmiko import ConnectHandler
cisco = {
	'device_type': 'cisco_ios',
	'host': '172.17.1.8',
	'username': 'admin',
	'password': '2017T3sla!',
	}
	
net_connect = ConnectHandler(**cisco)

net_connect.find_prompt()

output = net_connect.send_command("show ver")

print("SHOW VERSION")
print(output)

output_2 = net_connect.send_config_set("do show inv")

print("SHOW INVENTORY")
print(output_2)

