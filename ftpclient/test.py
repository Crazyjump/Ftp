import socket,json
s=socket.socket()
s.connect(("127.0.0.1",8090))

s.send(b"xxx")