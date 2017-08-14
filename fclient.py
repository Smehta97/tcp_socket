import socket

def Main():
	host = '127.0.0.1' #server IP
	port = 5000
	
	s = socket.socket() #default TCP socket
	s.connect((host, port))
	
	print "[client] Connection Established."
	fileName = raw_input("File Name: ")
	
	if fileName != 'q':
		s.send(fileName)
		
		#wait for file exist check [server]
		data = s.recv(1024)
		if data[:6] == "Exists":
			fileSize = long(data[6:])
			msg = raw_input("[client] File found, download " +\
											 str(fileSize) +" Bytes? ")
			
			if msg == "Y":
				s.send("Y")
				f = open("ftp_" + fileName, 'wb')
				data = s.recv(1024)
				totalRecv = len(data)
				f.write(data)
				while totalRecv < fileSize:
					data = s.recv(1024)
					totalRecv += len(data)
					f.write(data)
					print "{0:.2f}".format((totalRecv/float(fileSize))*100) + "% done."
				print "[client] Download Complete"
				s.send("Transfer Successful")
		
		else:
			print "File Does Not Exist."
	
	s.close()
	
if __name__ == '__main__':
	Main()
