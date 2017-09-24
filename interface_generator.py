#Template for spitting interface range of commands
target = raw_input("Type your initial interface command except for the switch port (ie set interface ge-0/0/ ) :  ")
end_target = raw_input("Type the last portion of your interface command: ")

for i in range (0, 48):
    print "%s%d %s" % (target, i, end_target)
