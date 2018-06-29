from CircleCheck import circle_detection_main
from Route import ZumoExtension
import cv2
import numpy as np
import socket
import math


# 親ディレクトリにあるコードをインポートできる
import sys
sys.path.append('../')

zumo = ZumoExtension.ZumoExtension()

print("gogo")
s = socket.socket()
port = 8090
host = socket.gethostname()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))

s.listen()

conn, addr = s.accept()
print(conn.recv(128))

# デバグ用
if __name__ == '__main__':
    red_pos_1 = []
    red_pos_2 = []
    blue_pos_1 = []
    blue_pos_2 = []

    # カメラを選ぶ
    cap = cv2.VideoCapture(0)
    print("#11")
    while (1):
        # カメラから画像データを読み込む
        ret, camera = cap.read()

        # 読み込んたかどうか判断
        if ret == True:

            # 画像からベクトルを取得
            # 赤い円、青い円の順、大きい円が先
            print("#2")
            camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2 = circle_detection_main.circle_detection_main(camera)
            cv2.imshow('capture', camera)
            if len(red_pos_1) == 0 :
                continue
            rr = math.sqrt(pow(red_pos_1[0] - red_pos_2[0],2) + pow(red_pos_1[1]-red_pos_2[1],2))
            C = 5 / rr;
            red_pos_1[0] = C * red_pos_1[0]
            red_pos_1[1] = C * red_pos_1[1]

            red_pos_2[1] = C * red_pos_2[1]
            red_pos_2[1] = C * red_pos_2[1]

            blue_pos_1[0] = C * blue_pos_1[0]
            blue_pos_1[1] = C * blue_pos_1[1]

            blue_pos_2[0] = C * blue_pos_2[0]
            blue_pos_2[1] = C * blue_pos_2[1]
            print(red_pos_1, red_pos_2, blue_pos_1, blue_pos_2)
            startX = (red_pos_1[0] + red_pos_2[0]) / 2
            startY = (red_pos_1[1] + red_pos_2[1]) / 2
            starRotX = red_pos_2[0] - red_pos_1[0]
            starRotY = red_pos_2[1] - red_pos_1[1]
            goalX = (blue_pos_1[0] + blue_pos_2[0]) / 2
            goalY = (blue_pos_1[1] + blue_pos_2[1]) / 2
            goalRotX = blue_pos_2[0] - blue_pos_1[0]
            goalRotY = blue_pos_2[1] - blue_pos_1[1]
            zumo.gogoSimple([startX,startY,starRotX,starRotY,goalX,goalY,goalRotX,goalRotY,100,100,0,1])
            print("#1")
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

        # 'q'を押したら、プログラム終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

conn.close()
s.close()

