import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from pynput.mouse import Button,Controller

###############################################
wCam,hCam = 1920,1080
###############################################
mouse = Controller()


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.5)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img, (x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)
        mouse.position = (x2,y2)

        if length < 50:
            cv2.circle(img, (cx, cy), 5, (0,255,0), cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)

    cv2.imshow('Img',img)
    cv2.waitKey(1)
