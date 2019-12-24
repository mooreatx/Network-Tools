#! python3
# Crack document password with brute force using dictionary file

import PyPDF2, os

os.chdir('C:\\Users\\182195\\OneDrive - Tokyo Electron Limited\\Network Info\\PyScripts\\Automate_the_Boring_Stuff_onlinematerials\\bruteforce')

pdfReader = PyPDF2.PdfFileReader(open('encrypted.pdf', 'rb'))
dictFile = open('dictionary.txt', 'r')
dictContent = dictFile.readlines()

def listToStrings(s):
	str1 = ''
	return (str1.join(s))


s = dictContent
dictStrings = listToStrings(s).split('\n')

for phrase in dictStrings:
	print(phrase)
	pdfReader.decrypt(phrase)
	if pdfReader.decrypt(phrase) == 1:
		print('\nSuccess passphrase is {}\n'.format(phrase))
		break