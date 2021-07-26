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

Code_state = 2            ### Used to determine what the current state of the input is. Zoom/edit/pan etc.
Code_substate = 0         ### Used to determine a substate. Basically distinguishes b/w all the options persent in one state
### In this code for example, the default state when it runs allows the used to zoom, pan and rotate the scene, each with diff gestures
### We use substate to distinguish b/w said 3 operations allowed in this particular state

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
      cv2.rectangle(image, (569, 0), (639, 60), (0,0,255), cv2.FILLED)
    elif(Main_switch == 0):
      cv2.rectangle(image, (569, 0), (639, 60), (0,255,0), cv2.FILLED)

    #### As the user selects different options, the view on the output will change
    if(Code_state == 1):
      #### State 1 corresponds to scene control
      #### substate 1 is zoom, substate 2 is pan and substate 3 is rotate scene
      if(Code_substate == 0):
        ### Header
        cv2.putText(image, 'Idle', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      
      elif(Code_substate == 1):
        ### Header
        cv2.putText(image, 'Zooming', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
        ### Dividing lines
        cv2.line(image, (129, 0), (129, 479), (0,0,0), 2)                 ## 1
        cv2.line(image, (258, 0), (258, 479), (0,0,0), 2)                 ## 2
        cv2.line(image, (387, 0), (387, 479), (0,0,0), 2)                 ## 3
        cv2.line(image, (516, 0), (516, 479), (0,0,0), 2)                 ## 4
        ### Showing text
        cv2.putText(image, 'Zoom out', (30, 450), cv2.FONT_HERSHEY_DUPLEX, 0.47, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Zoom out [Fine]', (134, 450), cv2.FONT_HERSHEY_DUPLEX, 0.47, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Idle', (310, 450), cv2.FONT_HERSHEY_DUPLEX, 0.47, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Zoom in [Fine]', (397, 450), cv2.FONT_HERSHEY_DUPLEX, 0.47, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, 'Zoom in', (546, 450), cv2.FONT_HERSHEY_DUPLEX, 0.47, (0, 0, 255), 1, cv2.LINE_AA)
      
      elif(Code_substate == 2):
        ### Header
        cv2.putText(image, 'Panning', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
        ### Dividing screen
        cv2.rectangle(image, (209, 169), (429, 319), (255, 255, 255), 2)        ## Idle
        cv2.line(image, (69, 0), (69, 479), (255,255,255), 2)                   ## leftmost region
        cv2.line(image, (209, 0), (209, 479), (255,255,255), 2)                 ## left region
        cv2.line(image, (429, 0), (429, 479), (255,255,255), 2)                 ## right region
        cv2.line(image, (569, 0), (569, 479), (255,255,255), 2)                 ## rightmost region
        ### Showing text
        cv2.putText(image, 'Idle', (300, 250), cv2.FONT_HERSHEY_DUPLEX, 0.57, (20, 170, 0), 1, cv2.LINE_AA)
      
      elif(Code_substate == 3):
        ### Header
        cv2.putText(image, 'Rotating', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      #########################################
      
    elif(Code_state == 2 or Code_state == 3):
      #### State 2 corresponds to object mode
      #### substate 1 is move, substate 2 is scale and substate 3 is rotate
      if(Code_substate == 0):
        ### Header
        cv2.putText(image, 'Idle', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      
      elif(Code_substate == 1):
        ### Header
        cv2.putText(image, 'Scaling', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      
      elif(Code_substate == 2):
        ### Header
        cv2.putText(image, 'Moving', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      
      elif(Code_substate == 3):
        ### Header
        cv2.putText(image, 'Rotating', (280, 40), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 1, cv2.LINE_AA)
      #########################################
    ######################################################################################

    #### Mediapipe code
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:       ### The loops here basically return the positions of each landmark indexed by ID
        for id, lms in enumerate(hand_landmarks.landmark):
          xlmarks[id] = int(lms.x*w)                                 ### Storing all the landmarks in list. The *h and *w are done to scale the obtained
          ylmarks[id] = int(lms.y*h)                                 ### vals of landmarks to vid input
          zlmarks[id] = int(lms.z)

          xmouse = np.interp(xlmarks, (0, w), (0, screenW))     ### Here we interpolate the x and y landmarks from video size to user screen size
          ymouse = np.interp(ylmarks, (0, h), (0, screenH))     ### which is used when we move the mouse around

          if(Flag == 1):
            #### This is where the flag comes in, for a set number of frames which are defined based on what I felt right for that particular gesture
            #### no gesture will be executed, this gives the user a bit of time to move their hands in a different gesture or to idle
            #### Meanwhile some gestures like dragging mouse or moving the pointer don't have a wait time since we need them to work continuously
            
            ##### 0. controls for main switch: Move index 8 and 12 of right hand specifically in the box in the top right corner
            if(569 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 60 and 0 < ylmarks[12] < 60 and Main_switch == 0):
              Flag = 0
              ## Pause time
              starttime = int(time.time())
              endtime = starttime + 60
              
              Main_switch = 1
              Code_substate = 0
              continue
            
            elif(589 <= xlmarks[8] < xlmarks[12] <= 639 and 0 < ylmarks[8] < 80 and 0 < ylmarks[12] < 80 and Main_switch == 1):
              Flag = 0
              ## Pause time
              starttime = int(time.time())
              endtime = starttime + 60
              
              Main_switch = 0
            ######################################################################################

            ##### 1. Mode selection: Move index 8, 12 and 16 of left hand specifically to the box in the upper left corner
            if((0 < xlmarks[16] < xlmarks[12] < xlmarks[8] < 90) and (0 < ylmarks[8] < 80) and (0 < ylmarks[12] < 80) and (0 < ylmarks[16] < 80) and Main_switch == 1):
              Flag = 0
              
              ## Pause time ##
              starttime = int(time.time())
              endtime = starttime + 10

              Code_state = 0
              Code_substate = 0
            ######################################################################################

            ##### 2. Zoom/Pan/Rotate mode: Touch tip of thumb and index finger to start zooming, make a fist once to start panning, take thumb to tip of middle finger to start rotating
            if(Main_switch == 1 and Code_state == 1 and xlmarks[5] < xlmarks[9] < xlmarks[13]):
              ######### 2.i) zooming #########
              if(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and (Code_substate == 0 or Code_substate == 2 or Code_substate == 3)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 1
                continue
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and Code_substate == 1):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                continue
              ######### 2.ii) panning #########
              elif(ylmarks[8] > ylmarks[5] and ylmarks[12] > ylmarks[9] and ylmarks[16] > ylmarks[13] and ylmarks[20] > ylmarks[17] and (Code_substate == 0 or Code_substate == 1 or Code_substate == 3)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 2
                continue
              elif(ylmarks[8] > ylmarks[5] and ylmarks[12] > ylmarks[9] and ylmarks[16] > ylmarks[13] and ylmarks[20] > ylmarks[17] and Code_substate == 2):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                continue
              ######### 2.iii) rotating #########
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[12], ylmarks[12])) <= 20 and (Code_substate == 0 or Code_substate == 1 or Code_substate == 2)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 3
                continue
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[12], ylmarks[12])) <= 20 and Code_substate == 3):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                continue
              ######### 2.i) zooming #########
              if(Code_substate == 1):
                if(xlmarks[5] <= 129):
                  Flag = 0
                  starttime = int(time.time())
                  endtime = starttime + 4
                  mouse.wheel(-1)

                elif(xlmarks[5] <= 258):
                  Flag = 0
                  starttime = int(time.time())
                  endtime = starttime + 24
                  mouse.wheel(-1)

                elif(xlmarks[5] <= 387):
                  Flag = 0
                  starttime = int(time.time())
                  endtime = starttime

                elif(xlmarks[5] <= 516):
                  Flag = 0
                  starttime = int(time.time())
                  endtime = starttime + 24
                  mouse.wheel(1)

                elif(xlmarks[5] <= 639):
                  Flag = 0
                  starttime = int(time.time())
                  endtime = starttime + 4
                  mouse.wheel(1)
              ######### 2.ii) panning #########
              elif(Code_substate == 2):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 4

                if(xlmarks[5] <= 69):
                  pyautogui.keyDown('ctrl')
                  pyautogui.press('num4')
                  pyautogui.press('num4')
                  pyautogui.press('num4')
                  pyautogui.keyUp('ctrl')
                elif(xlmarks[5] <= 209):
                  pyautogui.keyDown('ctrl')
                  pyautogui.press('num4')
                  pyautogui.keyUp('ctrl')

                if(xlmarks[5] >= 569):
                  pyautogui.keyDown('ctrl')
                  pyautogui.press('num6')
                  pyautogui.press('num6')
                  pyautogui.press('num6')
                  pyautogui.keyUp('ctrl')
                elif(xlmarks[5] >= 429):
                  pyautogui.keyDown('ctrl')
                  pyautogui.press('num6')
                  pyautogui.keyUp('ctrl')

                if(209 < xlmarks[5] < 429):
                  if(ylmarks[5] < 169):
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('num8')
                    pyautogui.keyUp('ctrl')
                  elif(ylmarks[5] > 319):
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('num2')
                    pyautogui.keyUp('ctrl')
              ######### 2.iii) rotating #########
              elif(Code_substate == 3):
                ######### No pause time in rotate as we are moving mouse and don't want a lag #########
                mouse.hold('middle')
                mouse.move(xmouse[5], ymouse[5])
                mouse.release('middle')
            ######################################################################################


            ##### 2 & 3. Object mode and Edit mode respectively:
            ##### Touch tip of thumb and index finger to start Scaling, make a fist once to start moving, take thumb to tip of middle finger to start rotating
            ##### To click on an object, touch tip of thumb to ring finger, and to cancel placement (i.e., press 'esc' key. touch tip of thumb and pinky)
            elif(Main_switch == 1 and (Code_state == 2 or Code_state == 3) and xlmarks[5] < xlmarks[9] < xlmarks[13]):
              ######### 2,3.i) scaling #########
              if(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and (Code_substate == 0 or Code_substate == 2 or Code_substate == 3)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 1
                keyboard.press_and_release('s')
                continue
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[8], ylmarks[8])) <= 20 and Code_substate == 1):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                mouse.click('left')
                continue
              ######### 2,3.ii) moving #########
              elif(ylmarks[8] > ylmarks[5] and ylmarks[12] > ylmarks[9] and ylmarks[16] > ylmarks[13] and ylmarks[20] > ylmarks[17] and (Code_substate == 0 or Code_substate == 1 or Code_substate == 3)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 2
                keyboard.press_and_release('g')
                continue
              elif(ylmarks[8] > ylmarks[5] and ylmarks[12] > ylmarks[9] and ylmarks[16] > ylmarks[13] and ylmarks[20] > ylmarks[17] and Code_substate == 2):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                mouse.click('left')
                continue
              ######### 2,3.iii) rotating #########
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[12], ylmarks[12])) <= 20 and (Code_substate == 0 or Code_substate == 1 or Code_substate == 2)):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 3
                keyboard.press_and_release('r')
                keyboard.press_and_release('r')
                continue
              elif(math.dist((xlmarks[4], ylmarks[4]), (xlmarks[12], ylmarks[12])) <= 20 and Code_substate == 3):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 20
                
                Code_substate = 0
                mouse.click('left')
                continue
              #########################################
              mouse.move(xmouse[5], ymouse[5])
              ######### 2,3.0) mouse click holding down shift #########
              if(Code_substate == 0 and math.dist((xlmarks[4], ylmarks[4]), (xlmarks[16], ylmarks[16])) <= 20):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 10

                keyboard.press('shift')
                mouse.click('left')
                keyboard.release('shift')
              ######### 2,3.iv) press esc to cancel operation #########
              if((Code_substate == 1 or Code_substate == 2 or Code_substate == 3) and math.dist((xlmarks[4], ylmarks[4]), (xlmarks[20], ylmarks[20])) <= 20):
                Flag = 0
                starttime = int(time.time())
                endtime = starttime + 10

                keyboard.press_and_release('esc')
                cv2.putText(image, 'CANCELLED', (280, 270), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 1, cv2.LINE_AA)
            ######################################################################################


        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)     ### Draws the amazing looking lines and red dots you see on your hands
        cv2.circle(image, (xlmarks[5], ylmarks[5]), 10, (255, 0, 255), -1)              ### Draw a circle on landmark 5 to let users know it is being used for tracking

    cv2.putText(image, fps, (20, 120), cv2.FONT_HERSHEY_COMPLEX, 1.7, (10, 155, 0), 3, cv2.LINE_AA)    ## FPS counter
    
    cv2.imshow('Output', image)                                   ### A basic cv2 command which displays the output image
    if cv2.waitKey(2) & 0xFF == 27:
      break

cap.release()                                                     ### closes the cam