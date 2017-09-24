import paramiko
import time

def patch_crypto_be_discovery():

    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]	

if __name__ == '__main__':
	username = "[script ssh login username]" #Replace with your login, or use RSA keys
	password = "[script ssh login password]" #Replace with your password, or use RSA keys
	username2 = "root"
	password2 = "roottest1" #Example, replace with new root pw
	
	# Opens files in read mode
	f1 = open("RootLoginList.txt","r") #A flat file with hostnames or IP addresses.
	f2 = open("RootLoginResults.txt", "w") #Results/Exception output.
	
	patch_crypto_be_discovery()

	# Creates list based on f1
	devices = f1.readlines()


	for device in devices:
		device = device.rstrip()
		remote_conn_pre = paramiko.SSHClient()
		remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			remote_conn_pre.connect(device, username=username, password=password, look_for_keys=False, allow_agent=False, timeout=5)
		except Exception:
			print (device, "First Login Failed", file=f2)
			print ("", file=f2)
			continue
		remote_conn = remote_conn_pre.invoke_shell()	
		remote_conn.send("\n")
		remote_conn.send("configure\n")
		time.sleep(5)
		remote_conn.send("set system root-authentication encrypted-password ""$1$HNspum6a$9MIf.Xm56oKUuaVwx8VcD/""\n") #Example, replace with new encrypted root pw
		time.sleep(5)
		remote_conn.send("delete system services ssh root-login deny\n")
		time.sleep(5)
		remote_conn.send("commit confirmed 5\n")	
		time.sleep(30)
		output = remote_conn.recv(8000)
		print (device, output, file=f2)
		print ("", file=f2)
		remote_conn_pre2 = paramiko.SSHClient()
		remote_conn_pre2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			remote_conn_pre2.connect(device, username=username2, password=password2, look_for_keys=False, allow_agent=False, timeout=5)
		except Exception:
			remote_conn.send("set system root-authentication encrypted-password ""[old encrypted password hash]""\n") #original encrypted root pw
			time.sleep(10)
			remote_conn.send("set system services ssh root-login deny\n")
			time.sleep(10)
			remote_conn.send("commit \n")			
			time.sleep(30)
			output = remote_conn.recv(8000)
			print (device, output, file=f2)
			print ("", file=f2)
			print (device, "Second Login Failed", file=f2)
			print ("", file=f2)
			continue
		remote_conn2 = remote_conn_pre2.invoke_shell()
		remote_conn.send("commit\n")
		time.sleep(30)
		remote_conn2.send("\n")
		remote_conn2.send("cli\n")
		time.sleep(2)
		remote_conn2.send("configure\n")
		time.sleep(5)
		remote_conn2.send("set system services ssh root-login deny\n")
		time.sleep(5)
		remote_conn.send("commit \n")
		time.sleep(30)
		output = remote_conn2.recv(8000)
		print (device, output, file=f2)
		print ("", file=f2)
		remote_conn.send("exit\n")
		remote_conn_pre.close()
		remote_conn_pre2.close()
	f1.close()
	f2.close()