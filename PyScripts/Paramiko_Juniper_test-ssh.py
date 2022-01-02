import paramiko
import time

def disable_paging(remote_conn):
	"'Disable paging on a Juniper Switch'"
	
	remote_conn.send("set cli screen-length 0\n")
	time.sleep(1)
	
	# Clear the buffer on the screen
	output = remote_conn.recv(1000)
	
	return output
	

if __name__ == '__main__':


	#VARIABLES THAT NEED CHANGED
	hostname = raw_input('Enter device hostname:  ')
	username = raw_input('Enter username:  ')
	password = raw_input('Enter password:  ')
	
	#Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()
	
	#Automatically add untrusted hosts
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	#initiate SSH connection
	remote_conn_pre.connect(hostname, username=username, password=password, look_for_keys=False, allow_agent=False)
	print "SSH connection established to %s" % hostname
	
	#Use invoke_shell to establish an 'interactive session'
	remote_conn=remote_conn_pre.invoke_shell()
	print "Interactive SSH session established"
	
	#Strip the initial router prompt
	output = remote_conn.recv(1000)
	
	#See what we have
	print output
	
	#Turn off paging
	disable_paging(remote_conn)
	
	#Now let's try to send the router a command
	remote_conn.send("\n")
	remote_conn.send("show interface terse\n")
	
	#Wait for the command to complete
	time.sleep(2)
	
	output = remote_conn.recv(5000)
	print output