import math
import time
import numpy as np
import cv2
import mediapipe as mp
import keyboard
import mouse
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pyautogui.FAILSAFE = False

sourcefile = open('Landmarks.txt', 'w')       #### Printing landmark locations to ext file ####

Flag = 1        #### Execution state ####
starttime = 0
endtime = 0
Main_switch = 0   ###turns code on or off

## FPS counter
last_frame_time, current_frame_time = 0, 0

i = 1       ## For indexing output ##

#### Lists store landmarks ####
xlmarks = []
ylmarks = []
zlmarks = []

for i in range(21):
  xlmarks.append(0)
  ylmarks.append(0)
  zlmarks.append(0)

config_cycle = 900
count = 0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    ##FPS counter
    current_frame_time = time.time()
    fps = 1/(current_frame_time - last_frame_time)
    last_frame_time = current_frame_time
    fps = str(int(fps))
    font = cv2.FONT_HERSHEY_COMPLEX

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    h, w, r = image.shape          #### taking in image size #####
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if(starttime < endtime):
      endtime = endtime - 1
    if(endtime == starttime):
      Flag = 1
    

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        for id, lms in enumerate(hand_landmarks.landmark):
          if(count <= config_cycle):
            count += 1
          
          else:
            xlmarks[id] = lms.x*w
            ylmarks[id] = lms.y*h
            zlmarks[id] = lms.z

            xmouse = np.interp(xlmarks, (0, w), (0, 1920))
            ymouse = np.interp(ylmarks, (0, h), (0, 1080))

            if(Flag == 1):
              ###### 1. controls for main switch ######
              if(589 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 80 and 0 < ylmarks[12] < 80 and Main_switch == 0):
                Main_switch = 1
                Flag = 0

                ## Pause time ##
                starttime = int(time.time())
                endtime = starttime + 60
              elif(589 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 80 and 0 < ylmarks[12] < 80 and Main_switch == 1):
                Main_switch = 0
                Flag = 0

                ## Pause time ##
                starttime = int(time.time())
                endtime = starttime + 60
              ##### Main switch end #####

              ##### 2. Edit mode [Press Tab] #####
              if((0 < xlmarks[16] < xlmarks[12] < xlmarks[8] < 90) and (0 < ylmarks[8] < 80) and (0 < ylmarks[12] < 80) and (0 < ylmarks[16] < 80) and Main_switch == 1):
                Flag = 0
                
                ## Pause time ##
                starttime = int(time.time())
                endtime = starttime + 40

                keyboard.press_and_release('Tab')
              ##### Edit mode end #####

              ##### 3. Drag ##### [WIP]
              if(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and Main_switch == 1):
                ######### No pause time in drag as we require a continuous input for that one #########
                mouse.drag(pyautogui.position().x, pyautogui.position().y, xmouse[8], ymouse[8])
                print(pyautogui.position())
              
              # ##### 4. Select stuff #####
              if(math.dist((xlmarks[8], ylmarks[8]), (xlmarks[12], ylmarks[12])) <= 10 and Main_switch == 1):
                Flag = 0
                
                ## Pause time ##
                starttime = int(time.time())
                endtime = starttime + 40

                pyautogui.click(button='left')
              
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      i += 1
    
    else:
      count = 0
            
    cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    cv2.rectangle(image, (0, 0), (90, 80), (255,0,0))
    if(Main_switch == 1):
      cv2.rectangle(image, (589, 0), (639, 80), (0,0,255))
    elif(Main_switch == 0):
      cv2.rectangle(image, (589, 0), (639, 80), (0,255,0))
    cv2.imshow('MediaPipe Hands', image)
    
    # # # # # # # # # # # # # # # endtime = time.time()     ## runtime counter ##
    # # # # # # # # # # # # # # # print(endtime-starttime)

    if cv2.waitKey(2) & 0xFF == 27:
      break

sourcefile.close()
cap.release()