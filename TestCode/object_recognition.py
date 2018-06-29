import cv2
import numpy as np

# 円を検出する
def re_circle(gray_image):

    image = cv2.cvtColor(gray_image, cv2.COLOR_RGB2GRAY)
    # 円を検出する
    # 画像、グラディエント
    # 解像度、円同士の最小距離、
    # エッジ検出の閾値、中心検出の閾値
    # 最小半径、最大半径
    #circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20, param1=10, param2=20, minRadius=20, maxRadius=100)
    circles= cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,4,100,param1=150,param2=150,minRadius=38,maxRadius=80)

    # 小さい円の座標
    small_r = circles[0,:][0][2]

    small = []
    big = []

    if(circles[0,:][1][2] > small_r):
        small = circles[0,:][0]
        big = circles[0,:][1]

    else:
        small = circles[0,:][1]
        big = circles[0,:][0]

    return small, big


image = cv2.imread('C:/Users/nakamura sho/Documents/user/en2.png')
s, l = re_circle(image)

print(s)
print(l)
#cv2.imshow("capture", image)
#cv2.waitKey(0)

