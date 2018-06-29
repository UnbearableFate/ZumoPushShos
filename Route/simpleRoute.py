import socket
from Route import ZumoExtension

zumo = ZumoExtension.ZumoExtension()

zumo.gogoSimple([0, 0, 0, 1, 40, 40, 1, 0, 80, 100, 1, 0])
print("gogo")
s = socket.socket()
port = 8090
host = socket.gethostname()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))

s.listen()

conn, addr = s.accept()
print(conn.recv(128))

print("gogogogogogo")
res = zumo.action

while len(res) != 0:
    pp = res[:21]
    speedData = ""
    for a in pp:
        speedData += a[0]+a[1]+a[2]
    print(speedData)
    print("")
    send = conn.send(speedData.encode("ascii"))
    res = res[21:]

speedData = ""
for i in range(0, 256):
    speedData += "0"

while True:
    send = conn.send(speedData.encode("ascii"))

conn.close()
s.close()
