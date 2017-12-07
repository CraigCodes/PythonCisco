import paramiko
import time
import os
import re
import sys
import csv
import getpass

def login(IP, Username, Password):
	#Create instance of SSHClient Object
	remote_conn_pre=paramiko.SSHClient()

	#Automatically add untrusted hosts 
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	#Initiate SSH Connection
	remote_conn_pre.connect(IP, username=Username, password=Password, look_for_keys=False, allow_agent=False)
	print ("SSH Connection Established to %s" %IP)

	#Use invoke_shell to establish an interactive session
	remote_conn=remote_conn_pre.invoke_shell()
	print ("Interactive SSH session established")
	return remote_conn


def runCommands(session):
	#sends TFTP transfer command
	session.send("\n")
	session.send("copy running-config tftp:\n")
	session.send("TFTP SERVER IP ADDRESS \n")
	session.send("\n")
	time.sleep(5)
	print("Completed transfer")


def closeSession(session):	
	session.close()  
	print("SSH Session Closed")  
	time.sleep(2)



if __name__ == '__main__':



	#Get username and password
	Username = input("Username: ")
	Password = getpass.getpass("Password: ")

	#opens CSV file with the swith IP's, Calls the function to run the backup of config.dat
	with open('YOUR CSV FILE PATH') as csvDataFile:
		reader=csv.reader(csvDataFile)
		for row in reader:
			ip=row[0]
			print('Working on device '+ip)
			session = login(ip, Username, Password)
			runCommands(session)
			closeSession(session)
			


		

	print("Completed Backup")

