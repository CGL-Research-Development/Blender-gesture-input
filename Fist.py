import cv2
import time
from math import sqrt
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
on=False
on2=False

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
while True:
    success, img = cap.read()
    cv2.rectangle(img,(0,0),(75,75),(127,160,43),cv2.FILLED)
    cv2.rectangle(img,(85,0),(160,75),(127,160,43),cv2.FILLED)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        

        # print(fingers)
        # if(fingers[1]==1):
        #     if(lmList[8][0]<75 and lmList[8][0]>0 and lmList[8][1]<75 and lmList[8][1]>0):
        #         if(on2==False):
        #             on2=True
        #             print("TAB MODE ON")
            
        #     elif(lmList[8][0]<160 and lmList[8][0]>85 and lmList[8][1]<75 and lmList[8][1]>0):
        #         if(on2==True):
        #             on2=False
        #             print("TAB MODE OFF")
        
                    
              
        if (lmList[tipIds[1]][2] < lmList[tipIds[0]][2]) and (lmList[tipIds[1]][2] < lmList[tipIds[3]][2]) and (lmList[tipIds[1]][2] < lmList[tipIds[4]][2])  and (lmList[tipIds[2]][2] < lmList[tipIds[0]][2]) and lmList[tipIds[2]][2] < lmList[tipIds[3]][2] and lmList[tipIds[2]][2] < lmList[tipIds[4]][2]:
                x1 = lmList[tipIds[1]][1]
                y1 = lmList[tipIds[1]][2]
                x2 = lmList[tipIds[2]][1]
                y2 = lmList[tipIds[2]][2]
                
                #print(dist((x1,y1),(x2,y2)))
                if(dist((x1,y1),(x2,y2))<25): 
                    print("Select")      
        totalFingers = fingers.count(1)
        if(totalFingers==0):
            if(on==False):
                on=True
                print("ObjectSelected")
        elif(totalFingers==5):
            if(on==True):
                on=False
                print("ObjectReleased")
            if (lmList[tipIds[1]][2] < lmList[tipIds[0]][2]) and (lmList[tipIds[1]][2] < lmList[tipIds[3]][2]) and (lmList[tipIds[1]][2] < lmList[tipIds[4]][2])  and (lmList[tipIds[2]][2] < lmList[tipIds[0]][2]) and lmList[tipIds[2]][2] < lmList[tipIds[3]][2] and lmList[tipIds[2]][2] < lmList[tipIds[4]][2]:
                x1 = lmList[tipIds[1]][1]
                y1 = lmList[tipIds[1]][2]
                x2 = lmList[tipIds[2]][1]
                y2 = lmList[tipIds[2]][2]
                
                #print(dist((x1,y1),(x2,y2)))
                if(dist((x1,y1),(x2,y2))<25): 
                    print("Select")
                
        
            
        # print(totalFingers)

        # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #             10, (255, 0, 0), 25)

    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime

    # cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
    #             3, (255, 0, 0), 3)
    img = cv2.flip(img,1)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if(key==27):
        break

cap.release()
cv2.destroyAllWindows()