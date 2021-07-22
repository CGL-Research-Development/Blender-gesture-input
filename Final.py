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
    min_tracking_confidence=0.5) as hands:    ### idk what this part really does, so I'd appreciate someone filling in the gaps. much thank
  
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
    font = cv2.FONT_HERSHEY_COMPLEX
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
        

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:       ### The loops here basically return the positions of each landmark indexed by ID
        for id, lms in enumerate(hand_landmarks.landmark):
          xlmarks[id] = lms.x*w                                 ### Storing all the landmarks in list. The *h and *w are done to scale the obtained
          ylmarks[id] = lms.y*h                                 ### vals of landmarks to vid input
          zlmarks[id] = lms.z

          xmouse = np.interp(xlmarks, (0, w), (0, screenW))     ### Here we interpolate the x and y landmarks from video size to user screen size
          ymouse = np.interp(ylmarks, (0, h), (0, screenH))     ### which is used when we move the mouse around

          if(Flag == 1):
            #### This is where the flag comes in, for a set number of frames which are defined based on what I felt right for that particular gesture
            #### no gesture will be executed, this gives the user a bit of time to move their hands in a different gesture or to idle
            #### Meanwhile some gestures like dragging mouse or moving the pointer don't have a wait time since we need them to work continuously
            
            ##### 0. controls for main switch: Move index 8 and 12 of right hand specifically in the box in the top right corner
            if(589 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 80 and 0 < ylmarks[12] < 80 and Main_switch == 0):
              Main_switch = 1
              Flag = 0

              ## Pause time
              starttime = int(time.time())
              endtime = starttime + 60
            
            elif(589 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 80 and 0 < ylmarks[12] < 80 and Main_switch == 1):
              Main_switch = 0
              Flag = 0

              ## Pause time
              starttime = int(time.time())
              endtime = starttime + 60
            ######################################################################################

            ##### 1. Edit mode: Move index 8, 12 and 16 of left hand specifically to the box in the upper left corner
            if((0 < xlmarks[16] < xlmarks[12] < xlmarks[8] < 90) and (0 < ylmarks[8] < 80) and (0 < ylmarks[12] < 80) and (0 < ylmarks[16] < 80) and Main_switch == 1):
              Flag = 0
              
              ## Pause time ##
              starttime = int(time.time())
              endtime = starttime + 40

              keyboard.press_and_release('Tab')
            ######################################################################################

            ##### 2. Drag selection: Move indices 8 and 12 close to each other and then move your hand to drag the pointer
            if(math.dist((xlmarks[8], ylmarks[8]), (xlmarks[12], ylmarks[12])) <= 9 and Main_switch == 1):
              ######### No pause time in drag as we require a continuous input for that one #########
              mouse.drag(pyautogui.position().x, pyautogui.position().y, xmouse[9], ymouse[9])
            ######################################################################################

            ##### 3. Move mode: Move indices 4 and 8 close in a pinching motion, this stimulates pressing the 'g' key on the keyboard which drags objects in Blender
            if(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and Main_switch == 1):
              Flag = 0

              ## Pause time ##
              starttime = int(time.time())
              endtime = starttime + 40

              keyboard.press_and_release('g')
            ######################################################################################

            ##### 4. Rotate mode: Move indices 4 and 12 close, same as above, stimulates pressing 'r' which starts rotating the object
            if(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[12], ylmarks[12])) <= 20 and Main_switch == 1):
              Flag = 0

              ## Pause time ##
              starttime = int(time.time())
              endtime = starttime + 40

              keyboard.press_and_release('r')
            ######################################################################################
                          
            ##### Last-ish: Press esc: Move landmarks 4 and 20 close to stimulate pressing 'esc' key. We use this to cancel the current drag, rotation, scaling, etc. changes being done
            if(Main_switch == 1 and math.dist((xlmarks[4], ylmarks[4]), (xlmarks[20], ylmarks[20])) <= 20):
              keyboard.press_and_release('esc')
            ######################################################################################

            ##### Last: Move mouse around: This simply makes the mouse pointer follow the index 9 as soon as the master switch is set to activated
            if(Main_switch == 1):
              ######### No pause time in move as we require a continuous input for that one #########
              mouse.move(xmouse[9], ymouse[9])
              # # # # # # print(pyautogui.position())
            ######################################################################################
      
      cv2.rectangle(image, (0, 0), (75, 50), (255,0,0), cv2.FILLED)       ### Space which stimulates pressing 'tab'
    
      if(Main_switch == 1):                                               ### To show the main switch box, the if conditions are for changing color as the state changes
        cv2.rectangle(image, (589, 0), (639, 80), (0,0,255))
      elif(Main_switch == 0):
        cv2.rectangle(image, (589, 0), (639, 80), (0,255,0))

      mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)     ### Draws the amazing looking lines and red dots you see on your hands
      
    # else:                                                       ### To disable the main switch in case the algo doesn't detect any hands
    #   Main_switch = 0
            
    cv2.putText(image, fps, (20, 120), font, 3, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    
    cv2.imshow('Output', image)                                   ### A basic cv2 command which displays the output image
    if cv2.waitKey(2) & 0xFF == 27:
      break

cap.release()                                                     ### closes the cam