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
	username = raw_input("username: ") #Your login, or use RSA keys
	password = raw_input("password: ") #Your password, or use RSA keys
	enable = raw_input("enable password: ") #Enable password
	guestpassword = raw_input("New Guest Wireless Password: ") #Monthly WirelessGuestAccess password

	# Opens files in read mode
	f1 = open("WirelessControllersList.txt","r") #A flat file with hostnames or IP addresses.
	f2 = open("ControllerLoginResults.txt", "w") #Results/Exception output.

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
		remote_conn.send("configure terminal\n")
		time.sleep(5)
		remote_conn.send("enable""\n") #Example, replace with new encrypted root pw
		time.sleep(5)
		remote_conn.send("\r\n") % (enable)
		time.sleep(5)
		remote_conn.send("wlan ssid-profile WBSN_SSID_Guest\n")
        time.sleep(5)
        remote_conn.send("wpa-passphrase %r\n") % (guestpassword)
        time.sleep(5)
        remote_conn.send("end\n")
		time.sleep(5)
		remote_conn.send("exit\n")
		remote_conn_pre.close()
		remote_conn_pre2.close()
	f1.close()
	f2.close()
