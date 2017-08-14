import socket
import threading
import os
import getpass

def Retrieve(name, sock):
	fileName = sock.recv(1024)
	print "[server] Searching for: " + fileName
	if os.path.isfile(fileName):
		print "[server] Found: " + fileName
		sock.send("Exists " + str(os.path.getsize(fileName)))
		
		#Wait for client response
		userReply = sock.recv(1024)
		if userReply[:1] == "Y":
			print "[server] Starting Transfer (" + str(os.path.getsize(fileName)) + ") Bytes"
			with open(fileName, 'rb') as f:
				sendBytes = f.read(1048576) #1MB buffer
				sock.send(sendBytes)
				while sendBytes != "":
					sendBytes = f.read(1048576)
					sock.send(sendBytes)
				ftp_done = sock.recv(1024)
				print "[server] " + ftp_done
	else:
		sock.send("Error")
	
	sock.close()
	
def Main():
	host = '127.0.0.1'
	port = 5000
	
	usr = getpass.getuser()
	
	os.chdir('/home/'+ usr +'/Desktop')
	
	s = socket.socket() #default to TCP
	s.bind((host, port))
	s.listen(5)
	
	print "[server] Server Started."
	
	while True:
		c, adr = s.accept()
		print "[server] Client [" + str(adr) + "] Connected."
		t = threading.Thread(target=Retrieve, args =("retrThread", c))
		t.start()
	
	s.close()
	
if __name__ == '__main__':
	Main()
