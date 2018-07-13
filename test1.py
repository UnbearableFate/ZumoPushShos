from CircleCheck import circle_detection_main
from Route import ZumoExtension
import cv2
import numpy as np
import socket
import math

cap = cv2.VideoCapture(0)
ret, camera = cap.read()
while True :
    camera, red_pos_1, red_pos_2, blue_pos_1, blue_pos_2 = circle_detection_main.circle_detection_main(camera)
    print(red_pos_1)
