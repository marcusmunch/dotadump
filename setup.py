#!/usr/bin/python
import os, json

def addGlobals():
    global output, oldConfig, FTPaddr, FTPpass, steamID
    output = {}

def loadOldConfig():
    if os.path.exists("config.ini"):
        global oldConfig
        file = open("config.ini").read()
        oldConfig = json.loads(file)
    else:
        file = open("config.ini", "w")
        file.write("{}")

def compileOutput():
    if 'FTPaddr' in globals():
        output['FTPaddr'] = FTPaddr
        output['FTPaddr'] = FTPpass
        print 'FTP logon credentials updated'
    if 'steamID' in globals():
        output['steamID'] = steamID
        print 'Steam32-ID updated'
    if output != {}:
        file = open("config.ini", 'w')
        file.write(json.dumps(output))
        file.close()
    
def promptFTP():
    while True:
        resp = raw_input ("Update FTP address? Y/N ").lower()
        if resp.lower() == 'n':
            print "Skipping!"
            FTPaddr = oldConfig['FTPaddr']
            FTPpass = oldConfig['FTPpass']
            break
        elif resp != 'y' and resp != 'n': print 'Input not accepted, try again'
        elif resp == 'y': pass
        input = raw_input('Enter FTP address: ')
        if input != '': FTPaddr = input
        else: FTPaddr = oldConfig['FTPaddr']
        input = raw_input('Enter FTP password: ')
        if input != '': FTPpass = input
        else: FTPpass = oldConfig['FTPaddr']
        break

def promptID():
    while True:
        resp = raw_input('Update Steam32 ID? Y/N ').lower()
        if resp == "n":
            print "Skipping!"
            break
        elif resp == "y": pass
        else: print "Input not accepted, try again"
        resp2 = raw_input ("Enter Steam32 ID: ")
        if resp2 == '':
            steamID = oldConfig['steamID']
        elif resp2.isdigit():
            steamID = resp2
            break
        else: print "Input is not all digits. Try again"

if __name__ == "__main__":
    addGlobals()
    loadOldConfig()
    promptFTP()
    promptID()
    compileOutput()
