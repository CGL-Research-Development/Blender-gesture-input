'''This is just a playground for me to test out stuff from keeb, mouse and pygui libs.
I'll just leave it here in case someone interested wants to play around as well without disturbing the main code
This is the same code as final.py, just without the main if conditions'''

import math
import time
import numpy as np
import cv2
import mediapipe as mp
import keyboard
import mouse
import pyautogui

### Mediapipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pyautogui.FAILSAFE = False                ### Setting the failsafe which terminates code as soon as mouse pointer reaches a screen corner to false

screenW, screenH = pyautogui.size()       ### Gets screen size, useful later when use use numpy interp

### Execution state: We use this to give the small break whenever we execute commands which don't need to give output continuously like
### pressing 'g' for example to move objects. We set the flag to 0 as soon as the code is executed and set it to 1 after a certain amount of time has passeed
Flag = 1
starttime, endtime = 0, 0     ### Used for counter before flag is set to 1 again

### FPS counter
last_frame_time, current_frame_time = 0, 0

Main_switch = 0   ### Turns code on or off: Works using the area in the upper right corner

Code_state = 1    ### Used to determine what the current state of the input is. Zoom/edit/pan etc.

### Lists store landmarks
xlmarks = []
ylmarks = []
zlmarks = []

for i in range(21):
  xlmarks.append(0)
  ylmarks.append(0)
  zlmarks.append(0)

cap = cv2.VideoCapture(0)     ### This tell the code what the index of the camera to be used is. If the code doesn't read your camera input, try changing the index


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:    ### idk how to summarize confidence, so I'd appreciate someone filling in the gaps. much thank  
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")   ### If there is a successful frame captured, the code will continue, else it provids an error message
      continue

    #### FPS counter
    current_frame_time = time.time()
    fps = 1/(current_frame_time - last_frame_time)
    last_frame_time = current_frame_time
    fps = str(int(fps))
    font = cv2.FONT_HERSHEY_SIMPLEX
    #### So to make this work, I basically take the current time when this frame is being read
    #### and subtract it from the time when the previous frame was read and take inverse of the whole thing

    #### Flipping the image since we get a mirror image from camera
    #### and converting it to RGB since cv2 gives BGR but mediapipe works on RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    h, w, r = image.shape          ### Taking in image size. r value is practically useless to us
    
    #### To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    #### Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #### This snippet resets the flag state to 1 after a set amount of time has passed
    if(starttime < endtime):
      endtime = endtime - 1
    if(endtime == starttime):
      Flag = 1
    
    cv2.rectangle(image, (0, 0), (90, 60), (255,0,0), cv2.FILLED)       ### Space which stimulates pressing 'tab'
      
    if(Main_switch == 1):                                               ### To show the main switch box, the if conditions are for changing color as the state changes
      cv2.rectangle(image, (569, 0), (639, 60), (0,0,255))
    elif(Main_switch == 0):
      cv2.rectangle(image, (569, 0), (639, 60), (0,255,0))

    if(Code_state == 1):
      cv2.line(image, (129, 0), (129, 479), (0,0,0), 2)                 ## 1
      cv2.line(image, (258, 0), (258, 479), (0,0,0), 2)                 ## 2
      cv2.line(image, (387, 0), (387, 479), (0,0,0), 2)                 ## 3
      cv2.line(image, (516, 0), (516, 479), (0,0,0), 2)                 ## 4


    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:       ### The loops here basically return the positions of each landmark indexed by ID
        for id, lms in enumerate(hand_landmarks.landmark):
          xlmarks[id] = lms.x*w                                 ### Storing all the landmarks in list. The *h and *w are done to scale the obtained
          ylmarks[id] = lms.y*h                                 ### vals of landmarks to vid input
          zlmarks[id] = lms.z

          xmouse = np.interp(xlmarks, (0, w), (0, screenW))     ### Here we interpolate the x and y landmarks from video size to user screen size
          ymouse = np.interp(ylmarks, (0, h), (0, screenH))     ### which is used when we move the mouse around

          if(Flag == 1):
            if(xlmarks[9] <= 129):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 4
                
                mouse.wheel(-1)            
            elif(xlmarks[9] <= 258):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 24
                
                mouse.wheel(-1)            
            elif(xlmarks[9] <= 387):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime            
            elif(xlmarks[9] <= 516):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 24
                
                mouse.wheel(1)            
            elif(xlmarks[9] <= 639):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 4
                
                mouse.wheel(1)

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)     ### Draws the amazing looking lines and red dots you see on your hands
                
    cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    
    cv2.imshow('Output', image)                                   ### A basic cv2 command which displays the output image
    if cv2.waitKey(2) & 0xFF == 27:
      break

cap.release()                                                     ### closes the cam