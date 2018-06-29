import socket

s = socket.socket()
port = 8010
host = socket.gethostname()

print(host)

s.bind((host, port))

s.listen()

conn, addr = s.accept()

r = 100
l = 100

while True:
    client_data = conn.recv(1024)
    print('受信しました。')

    speedData = 'r' + str(r) + 'l' + str(l)
    print(speedData)
    send = conn.send(speedData.encode("ascii"))

