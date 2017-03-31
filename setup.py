#!/usr/bin/python
import os, json

def compileOutput():
    global output
    output = {}
    if 'FTPaddr' in globals():
        output['FTP_address'] = FTPaddr
        output['FTP_password'] = FTPpass
    if 'steamID' in globals():
        output['steam32id'] = steamID
    if output != {}:
        file = open("config.ini", 'w')
        file.write(json.dumps(output))
        file.close()
    else:
        if os.path.isfile('config.ini'):
            os.remove("config.ini")
            print "\nConfig.ini deleted"
        else:
            print "\nConfig.ini not existing and not created."
    
def promptFTP():
    while True:
        resp = raw_input ("Update FTP address? Y/N ").lower()
        if resp.lower() == 'n':
            print "Skipping!"
            break
        elif resp != 'y' and resp != 'n': print 'Input not accepted, try again'
        elif resp == 'y': pass
        global FTPaddr, FTPpass
        FTPaddr = raw_input('Enter FTP address: ')
        FTPpass = raw_input('Enter FTP password: ')
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
        if resp2.isdigit():
            global steamID
            steamID = resp2
            break
        else: print "Input is not all digits. Try again"

if __name__ == "__main__":
    promptFTP()
    promptID()
    compileOutput()
