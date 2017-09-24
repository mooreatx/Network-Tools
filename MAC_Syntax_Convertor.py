# Python Script that converts MAC Address formats to different standards
# Converts between Cisco, UNIX, and EUI-48 Format depending on input

print "\n"
print "What is your MAC address?"
mac_addr = raw_input("MAC Address> ")
print "\n"

if ":" in mac_addr:
    mac_split = mac_addr.split(":")
    hex_0 = mac_split[0]
    hex_1 = mac_split[1]
    hex_2 = mac_split[2]
    hex_3 = mac_split[3]
    hex_4 = mac_split[4]
    hex_5 = mac_split[5]
    print "Cisco Format:"
    print "%s%s.%s%s.%s%s\n" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
    print "EUI-48 Format"
    print "%s-%s-%s-%s-%s-%s" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
elif "-" in mac_addr:
    mac_split = mac_addr.split("-")
    hex_0 = mac_split[0]
    hex_1 = mac_split[1]
    hex_2 = mac_split[2]
    hex_3 = mac_split[3]
    hex_4 = mac_split[4]
    hex_5 = mac_split[5]
    print "Cisco Format:"
    print "%s%s.%s%s.%s%s\n" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
    print "UNIX Format"
    print "%s:%s:%s:%s:%s:%s" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
elif "." in mac_addr:
    hex_0 = mac_addr[0] + mac_addr[1]
    hex_1 = mac_addr[2] + mac_addr[3]
    hex_2 = mac_addr[5] + mac_addr[6]
    hex_3 = mac_addr[7] + mac_addr[8]
    hex_4 = mac_addr[10] + mac_addr[11]
    hex_5 = mac_addr[12] + mac_addr[13]
    print "EUI-48 Format:"
    print "%s-%s-%s-%s-%s-%s\n" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
    print "UNIX Format"
    print "%s:%s:%s:%s:%s:%s" % (hex_0, hex_1, hex_2, hex_3, hex_4, hex_5)
else:
    print "I didn't understand your input"
