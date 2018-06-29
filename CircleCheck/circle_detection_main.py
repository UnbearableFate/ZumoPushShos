import cv2
import numpy as np
import math
from CircleCheck import circle_detection

def circle_detection_main(camera):
    red_pos_1 = []
    red_pos_2 = []
    blue_pos_1 = []
    blue_pos_2 = []

    # 画像からベクトルを取得
    camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2 = circle_detection.circle_detection(camera)

    return camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2



# デバグ用
if __name__ == '__main__':
    red_pos_1 = []
    red_pos_2 = []
    blue_pos_1 = []
    blue_pos_2 = []

    # カメラを選ぶ
    cap = cv2.VideoCapture(0)

    while (1):
        # カメラから画像データを読み込む
        ret, camera = cap.read()

        # 読み込んたかどうか判断
        if ret == True:

            # 画像からベクトルを取得
            camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2 = circle_detection_main(camera)
            cv2.imshow('capture', camera)

        # 'q'を押したら、プログラム終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()
