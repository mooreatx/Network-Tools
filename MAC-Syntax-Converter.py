#! python3
# MAC-Syntax-Converter.py - Converts MAC address to different formats

import sys


def macAddress():
	while True:
		try:
			print()
			print("What is your MAC address?")
			mac_addr = input("MAC Address> ")
			print()
	
			non_characters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']
			res = any(non in mac_addr for non in non_characters)
			
			if len(mac_addr) > 17:
				print("Please only use correct 12 character Hexidecimal Standards with no spaces")
				print()
				continue
				
			if len(mac_addr) < 12:
				print("Please only use correct 12 character Hexidecimal Standards with no spaces")
				print()
				continue

			if res == True:
				print("Please only use correct 12 character Hexidecimal Standards with no spaces")
				print()
				continue

			if ":" in mac_addr:
				mac_split = mac_addr.split(":")
				hex_0 = mac_split[0]
				hex_1 = mac_split[1]
				hex_2 = mac_split[2]
				hex_3 = mac_split[3]
				hex_4 = mac_split[4]
				hex_5 = mac_split[5]
				print("Cisco Format:")
				print("{}{}.{}{}.{}{}".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				print("\nEUI-48 Format")
				print("{}-{}-{}-{}-{}-{}\n".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				continue
			elif "-" in mac_addr:
				mac_split = mac_addr.split("-")
				hex_0 = mac_split[0]
				hex_1 = mac_split[1]
				hex_2 = mac_split[2]
				hex_3 = mac_split[3]
				hex_4 = mac_split[4]
				hex_5 = mac_split[5]
				print("Cisco Format:")
				print("{}{}.{}{}.{}{}".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				print("\nUNIX Format")
				print("{}:{}:{}:{}:{}:{}\n".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				continue
			elif "." in mac_addr:
				hex_0 = mac_addr[0] + mac_addr[1]
				hex_1 = mac_addr[2] + mac_addr[3]
				hex_2 = mac_addr[5] + mac_addr[6]
				hex_3 = mac_addr[7] + mac_addr[8]
				hex_4 = mac_addr[10] + mac_addr[11]
				hex_5 = mac_addr[12] + mac_addr[13]
				print("EUI-48 Format:")
				print("{}-{}-{}-{}-{}-{}".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				print("\nUNIX Format")
				print("{}:{}:{}:{}:{}:{}\n".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				continue
			else:
				hex_0 = mac_addr[0] + mac_addr[1]
				hex_1 = mac_addr[2] + mac_addr[3]
				hex_2 = mac_addr[4] + mac_addr[5]
				hex_3 = mac_addr[6] + mac_addr[7]
				hex_4 = mac_addr[8] + mac_addr[9]
				hex_5 = mac_addr[10] + mac_addr[11]
				print("Cisco Format:")
				print("{}{}.{}{}.{}{}".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				print("\nEUI-48 Format")
				print("{}-{}-{}-{}-{}-{}".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				print("\nUNIX Format")
				print("{}:{}:{}:{}:{}:{}\n".format(hex_0, hex_1, hex_2, hex_3, hex_4, hex_5))
				continue
		except KeyboardInterrupt:
			sys.exit('\n\nGood Bye.\n')

macAddress()
