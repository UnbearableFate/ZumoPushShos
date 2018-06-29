import cv2
import numpy as np


#カメラを選ぶ
cap = cv2.VideoCapture(1)

while(1):
    #カメラから画像データを読み込む
    ret, camera = cap.read()

    #読み込んたかどうか判断
    if ret == True:
        #median filter、ノイズ除去
        camera = cv2.medianBlur(camera, 5)
        #RGB 2 GRAY
        cameraGray = cv2.cvtColor(camera, cv2.COLOR_RGB2GRAY)

        #丸検出
        circles = cv2.HoughCircles(cameraGray, cv2.HOUGH_GRADIENT,4,100,
                            param1=150,param2=150,minRadius=38,maxRadius=80)

        #丸検出したかどうかを判断
        if circles is not None:
            #画像に丸を描く
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(camera,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(camera,(i[0],i[1]),2,(0,0,255),3)
        cv2.imshow('capture',camera)

    #'q'を押したら、プログラム終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
