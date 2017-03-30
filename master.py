#!usr/bin/python
#import modules
import os, subprocess, sys, inspect
from time import localtime, strftime

#define variables
def outputWrite(currentName, data):
	if not os.path.exists('../output'):
		os.makedirs('../output')
	outputFile = open('../output/' + currentName + '.txt', 'w')
	print (currentName + ' says: ' + strftime('[%X %x]: ' + data))
	outputFile.write(data)
	outputFile.close()
	logWrite(currentName, data)

def logWrite(outputWrite, data):
	if not os.path.exists('../logs'):
		os.makedirs('../logs')
	logFile = open('../logs/' + currentName + '.log', 'a')
	logFile.write(strftime('[%x %X]: Wrote to file ' + currentName + '.txt: ' + (data) + "\n"))
	logFile.close()	

def execAll():
	global currentName
	os.chdir(r'scripts')
	print "Executing all scripts in '/scripts'..."
	for i in os.listdir('.'):
		currentName = (i)[:-3]
		execScr(i)

def execScr(f):
	if f[-3:] == ".py":
		execfile(f)
	else:
		print "An error has occurred!"

#execute script		
def main():
	execAll()
	
try:
	if __name__ == "__main__":
		main()
except:
    print "Unexpected error:", sys.exc_info()[0]
