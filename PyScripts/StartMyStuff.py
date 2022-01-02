#! python3
# Start my daily used Apps

import os, subprocess

os.chdir('C:\\Windows\\System32')

def programs():
	# Open Notepad++
	print('\nOpening Notepad++\n')
	subprocess.Popen('C:\\Program Files (x86)\\Notepad++\\notepad++.exe')

	# Open Chrome
	print('\nOpening Chrome\n')
	subprocess.Popen('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')
	
	# Open Powershell
	print('\nOpening Powershell\n')
	os.startfile(r'C:\Users\182195\Desktop\Python -PowerShell.lnk')
	
	# Open Outlook
	print('\nOpening Outlook\n')
	os.startfile(r'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Outlook 2016.lnk')
	
programs()