import cv2
import numpy as np

# カメラを選ぶ
cap = cv2.VideoCapture(0)

# def DrawCircle()

while (1):
    # カメラから画像データを読み込む
    ret, camera = cap.read()

    # 読み込んたかどうか判断
    if ret == True:
        # median filter、ノイズ除去
        camera = cv2.medianBlur(camera, 5)
        # RGB 2 GRAY
        cameraGray = cv2.cvtColor(camera, cv2.COLOR_RGB2GRAY)

        # 丸検出
        circles = cv2.HoughCircles(cameraGray, cv2.HOUGH_GRADIENT, 4, 100,
                                   param1=160, param2=150, minRadius=38, maxRadius=80)

        # 丸検出したかどうかを判断
        red_circles = []
        blue_circles = []
        j = -1

        # 出力ベクトル
        red_vec = []
        blue_vec = []

        # 円検出に成功したら
        if circles is not None:
            # 画像に丸を描く
            circles = np.int16(np.around(circles))

            # 円が3つ以上検出されたとき
            if circles.shape[1] > 1:
                #print(circles.shape[1])

                for i in circles[0, :]:
                    j = j + 1

                    if camera[i[1]][i[0]][2] > 100:# and camera[i[1]][i[0]][1] < 150:
                        red_circles = np.append(red_circles, circles[0, j])

                    if camera[i[1]][i[0]][0] > 200 and camera[i[0]][i[0]][2] < 150:
                        blue_circles = np.append(blue_circles, circles[0, j])

                # 2つ円が検出されたとき長さは6
                if (len(red_circles) == 6):
                    red_circles = np.reshape(red_circles, (len(red_circles) // 3, 3))
                    # convert from float to int
                    red_circles = np.int16(np.around(red_circles))
                    cv2.line(camera, (red_circles[0, 0], red_circles[0, 1]), (red_circles[1, 0], red_circles[1, 1]), (255, 0, 0), 10)

                    # 比較
                    if(red_circles[0, 2] - red_circles[1, 2] > 0):
                        red_vec_x = red_circles[0, 0] - red_circles[1, 0]
                        red_vec_y = red_circles[0, 1] - red_circles[1, 1]
                        print (red_circles[0, 0],red_circles[1, 0],red_vec_x)
                        print (red_circles[0, 1],red_circles[1, 1],red_vec_y)

                    else:
                        red_vec_x = red_circles[1, 0] - red_circles[0, 0]
                        red_vec_y = red_circles[1, 1] - red_circles[0, 1]

                    # レッドベクトル作成
                    red_vec = np.append(red_vec, red_vec_x)
                    red_vec = np.append(red_vec, red_vec_y)
                    print("red")
                    print(red_vec)


                if (len(blue_circles) == 6):
                    blue_circles = np.reshape(blue_circles, (len(blue_circles) // 3, 3))
                    # convert from float to int
                    blue_circles = np.int16(np.around(blue_circles))
                    cv2.line(camera, (blue_circles[0, 0], blue_circles[0, 1]), (blue_circles[1, 0], blue_circles[1, 1]), (255, 0, 0), 10)
                    # 比較
                    if(blue_circles[0, 2] - blue_circles[1, 2] > 0):
                        blue_vec_x = blue_circles[0, 0] - blue_circles[1, 0]
                        blue_vec_y = blue_circles[0, 1] - blue_circles[1, 1]

                    else:
                        blue_vec_x = blue_circles[1, 0] - blue_circles[0, 0]
                        blue_vec_y = blue_circles[1, 1] - blue_circles[0, 1]

                    # ブルーベクトル作成
                    blue_vec = np.append(blue_vec, blue_vec_x)
                    blue_vec = np.append(blue_vec, blue_vec_y)
                    print("blue")
                    print(blue_vec)

            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(camera, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(camera, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow('capture', camera)

    # 'q'を押したら、プログラム終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
