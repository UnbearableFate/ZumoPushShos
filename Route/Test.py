import socket
from Route import ZumoExtension

zumo = ZumoExtension.ZumoExtension()

res= zumo.superGOGO([0,0, 0,1, 60,40 ,1,0 , 80 ,100,1,0],[])
print("gogo")
s = socket.socket()
port = 8090
host = socket.gethostname()

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind((host, port))

s.listen()

conn, addr = s.accept()
print(conn.recv(128))

print("gogogogogogo")

while len(res) != 0 :
    pp = res[:32]
    speedData = ""
    for a in pp :
        speedData += a[3]+ a[4]
    print(speedData)
    print("")
    send = conn.send(speedData.encode("ascii"))
    res = res[32:]


speedData = ""
for i in range(0,256) :
    speedData += "0"

while True :
    send = conn.send(speedData.encode("ascii"))

conn.close()
s.close()
