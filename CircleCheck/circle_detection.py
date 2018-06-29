import cv2
import numpy as np

# 引数：画像、点 2 つ
def debug_line(img, tmp_cir):
    # デバグ用
    cv2.line(img, (tmp_cir[0, 0], tmp_cir[0, 1]), (tmp_cir[1, 0], tmp_cir[1, 1]), (255, 0, 0), 10)

def debug_circle(img, i):
    # draw the outer circle
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)


# 閾値を設定
# 引数：RGB の値
def red_threshold(blue, green, red):
    if(red > 120 and green < 70 and blue < 70):
        return 1
    else:
        return 0

def blue_threshold(blue, green, red):
    if(blue > 120 and green < 100 and red <70):
    #if(blue > 100):
        return 1
    else:
        return 0


# 画像の前処理
def image_preprocessing(img):
    # median filter（ノイズ除去）
    img = cv2.medianBlur(img, 5)

    # ヒストグラム平坦化
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.equalizeHist(hsv_image[2], hsv_image[2])
    img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return img

# 色認識してベクトルを返す
# 引数：カラー画像、Hough 変換の結果、検出したい色
# 戻り値：指定した色のベクトル
def color_recognition(img, circles, color):
    # 出力ベクトル
    vec = []
    pos_1 = []
    pos_2 = []

    # 認識のした円を入れるリスト
    tmp_cir = []
    # 円を探すカウンター
    j = -1

    # すべての円で探索
    for i in circles[0, :]:
        j = j + 1

        # 閾値で色検出
        if(color == "red"):
            if (red_threshold(img[i[1]][i[0]][0], img[i[1]][i[0]][1], img[i[1]][i[0]][2]) == 1):
                tmp_cir = np.append(tmp_cir, circles[0, j])
        elif(color == "blue"):
            if (blue_threshold(img[i[1]][i[0]][0], img[i[1]][i[0]][1], img[i[1]][i[0]][2]) == 1):
                tmp_cir = np.append(tmp_cir, circles[0, j])

         # 2 つ円が検出されたとき長さは 6
        if (len(tmp_cir) == 6):
            tmp_cir = np.reshape(tmp_cir, (len(tmp_cir) // 3, 3))
            # convert from float to int
            tmp_cir = np.int16(np.around(tmp_cir))

            # デバグ用
            debug_line(img, tmp_cir)
            """
            # 比較
            vec_x = tmp_cir[0, 0] - tmp_cir[1, 0]
            vec_y = tmp_cir[0, 1] - tmp_cir[1, 1]

            if(tmp_cir[0, 2] - tmp_cir[1, 2] > 0):
                pass
            else:
                vec_x = -vec_x
                vec_y = -vec_y
                     

            # ベクトル作成
            vec = np.append(vec, vec_x)
            vec = np.append(vec, vec_y)
            """

            if(tmp_cir[0, 2] - tmp_cir[1, 2] > 0):
                pos_1 = np.append(pos_1, tmp_cir[0, 0])
                pos_1 = np.append(pos_1, tmp_cir[0, 1])

                pos_2 = np.append(pos_2, tmp_cir[1, 0])
                pos_2 = np.append(pos_2, tmp_cir[1, 1])

            elif(tmp_cir[1, 2] - tmp_cir[0, 2] >= 0):
                pos_1 = np.append(pos_1, tmp_cir[1, 0])
                pos_1 = np.append(pos_1, tmp_cir[1, 1])

                pos_2 = np.append(pos_2, tmp_cir[0, 0])
                pos_2 = np.append(pos_2, tmp_cir[0, 1])

            # 2 つの円が検出されたら抜ける
            break

        # 同じ円が 2 つ検出できなかった場合
        if (len(tmp_cir) < 6):
            pos_1 = []
            pos_2 = []

    return pos_1, pos_2


# 画像から円を検出する
# 引数：画像
# 戻り値：画像、2 つのベクトル
def circle_detection(img):

    # 出力ベクトル
    red_pos_1 = []
    red_pos_2 = []
    blue_pos_1 = []
    blue_pos_2 = []

    # median filter（ノイズ除去）
    img = image_preprocessing(img)
    # グレースケール変換
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 丸検出
    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 4, 100,
                                   param1=160, param2=150, minRadius=38, maxRadius=80)

    # 円検出に成功したら
    if circles is not None:
        # 型変換
        circles = np.int16(np.around(circles))

        # 円が 1 つ以上検出されたとき
        if circles.shape[1] > 1:
            #print(circles.shape[1])
            # それぞれのベクトルを取得
            red_pos_1, red_pos_2 = color_recognition(img, circles, "red")
            blue_pos_1, blue_pos_2 = color_recognition(img, circles, "blue")

        # 円を描画
        for i in circles[0,:]:
            debug_circle(img, i)

    return img, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2


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
            camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2 = circle_detection(camera)
            print(red_pos_1, red_pos_2, blue_pos_1, blue_pos_2)
            cv2.imshow('capture', camera)

        # 'q'を押したら、プログラム終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()
