# Blender gesture input

So, as the name suggests, this repo has a code which allows you to do some basic work in Blender using hand gestures. It is of course limited as the gesture complexity would become too much.

First off, setting it all up. I'll include the whole abc, starting from installing the required libraries, so let's get to it.

***Note:** The code makes use of the Python language, which can be downloaded from [here](https://www.python.org/downloads/). The installation is quite easy and there is no complex setup required. Just remember to check the 'Add to path' option when installing.*

## 1. Installing libraries

This is a one time setup you'll require to ever use the code. Just open command prompt and put in a few simple lines.

```shell
pip install numpy
pip install opencv-python
pip install mediapipe
pip install keyboard
pip install mouse
pip install pyautogui
```

***Note:** In case you already have Python2 installed on your PC, you will need to change up the lines a bit. Instead of:*

```shell
pip install xyz
```

use:

```shell
pip3 install xyz
```

## 2. Running the code

Open the folder containing the file named **final.py** and open the file using python.

![Open file](../master/Imgs-for-documentation/Open-file.png)

**Errors:** There are 2 types of common errors that users of other programs like this one tend to come across.
> 1. Missing libraries:
Most common error, caused when you are missing a library which the code requires and you should run all the pip commands again. The error looks something like this:

![Missing libs](../master/Imgs-for-documentation/missing-lib-error.png)

> 2. Wrong camera index or camera inaccessible:
Second most common error, caused when either you camera index is wrong, or the python file is unable to access you camera due to technical issues. To fix this, first check your index. If you are using an inbuilt camera, then index `0` is what you most probably require, but do try changing it to `1` or `2`. For this, navigate to line 41 of the code which looks like this:
```py
cap = cv2.VideoCapture(0)
```
> and change the camera index. If this doesn't work, check to see if your camera drivers are properly installed and that your camera works properly. The best way to check is to open the windows camera app and seeing if it throws and error.
The error will looks something like this:

![Camera issue](../master/Imgs-for-documentation/Cam-index-error.png)

## 3. Using the code; gestures and notes:

> Please refer to this image to know the locations of the landmarks mentioned in the documentation below as these indices are a central part of using this code

![Landmarks](../master/Imgs-for-documentation/hand_landmarks.png)

**Some general points before getting started:**
* You will notice that certain landmarks carry a pink-ish color as compared to others which carry color red, this is to aid you, the user. For example, to enable the master switch you require the tip of the index and middle fingers, hence they are marked, while in object mode the mouse follows the base of the index finger, hence it is marked differently.
* The code can be exited by either pressing `esc` key on the keyboard after selecting the output image or by selecting the terminal running your code and pressing `ctrl+c` on it.
* You might at times notice some operation don't work for a really small duration after doing some specific operations, this is because I have added a small amount of wait time after certain operations so as to give users a bit of time to move their hands to a resting state after executing the operations.
* Please carefully note which hand is mentioned. Only the menu works with the left hand, rest all the operations require the usage of the right hand. You can of course reverse the left hand and fool the code into thinking that it is your right, but hey, that's your choice, you do you.
* **Important:** If you do the gesture to enter a particular state, say you want to start scaling in object or edit mode, then you first need to exit scaling state and return to idle state by either repeating the gesture if you are satisfied with the changes or doing the cancel changes gesture if you aren't, more on this can be found under individual gestures.

- I have set the code to detecting only one hand at a time as the hand detection algorithm is not 100% correct and picks up random objects as hands too. If you don't have any objects that come close to the color of skin in your background and want the code to detect both hands at once, navigate to line 46 and remove it.

```py
with mp_hands.Hands(
    min_detection_confidence=0.5,
    max_num_hands = 1,          ### Remove this line
    min_tracking_confidence=0.5) as hands:
```

- There is an FPS counter which is there just to get a general feel of the performance of the code, if you wish to disable it, get rid of line line 456. You can get rid of lines 23 & 24 and 54 - 60 as it might provide a very very minor performance boost.
**BE EXTREMELY CAREFUL TO NOT MESS UP THE INDENTATION OF ANY LINE AS IT CAN BREAK THE CODE.**

### a) Enabling the master switch

To make the code start accepting gestures, move the tip of your index and middle finger of your **right hand [Landmarks 8 & 12]** in the green box on the top right of the screen. When the box turns red, the code is now accepting inputs from you and all the gestures will be enabled. The on/off state of the code can be checked by the color of the box in the upper right. <br> <br>
Red: The code is running and selecting the red box will cause it to stop. <br>
Green: The code is currently NOT running. Move landmarks 8 and 12 in the green region to start the code. <br>

Illustration:

![Switch on](../master/Imgs-for-documentation/Switch-on.png)

> Note that enabling the master switch will set the code state to idle.

Illustration for idle state:

![Idle](../master/Imgs-for-documentation/Idle-state.png)

### b) Menu and mode selection

To bring up the menu, move the tip of index, middle and ring finger of the **left hand [Landmarks 8, 12 & 16]** to the blue box in the top left corner. To select one of the 3 options, move the same 3 landmarks over the respective box.

Illustration:

![Menu](../master/Imgs-for-documentation/Menu.png)

> To be able to use the menu, the code needs to be in idle state which can be checked via the yellow text on the top of the output window.

### c) Selecting objects

To select objects in object mode and vertices in edit mode, move your hand, the mouse pointer follows the base of the index finger of the **right hand [Landmark 5]**. Once you have reached the object or corner you wish to select, move the tip of the thumb to the base of the index finger, again of the **right hand [Landmarks 4 and 5]**.
The code here works by simply pressing the left click when you do this particular gesture while holding down `shift` key to allow selection of multiple objects. 

Illustration:

![Click](../master/Imgs-for-documentation/click-select.png)

> Selecting only works when the code is in idle state which can be checked via the yellow text on the top of the output window.

### d) Cancelling changes in object and edit modes

In case you are unhappy with the current change you are making and wish to revert to a state before you started the current operation, or selected the wrong gesture, you can reset the current operation by curling the ring and pinky fingers of the **right hand** such that the tip is below the bae for both **[Landmarks 13, 16 & 17, 20]**.

Illustration:

![Cancel](../master/Imgs-for-documentation/press-esc.png)

> Please note that the cancel gesture stimulates pressing `esc` key on the keyboard, hence doing this gesture when the output window is selected will lead to the code terminating.

### e) Zooming in scene navi mode and scaling in object and edit modes

To begin zooming in the scene navigation mode, or to start scaling an object in the object and edit modes, bring the tip of the right hand thumb close to the tip of the **right hand index finger [Landmarks 4 & 8]**.

Illustration:

![Pinch index](../master/Imgs-for-documentation/pinch-index.png)

* In case of zoom mode, the position of the base of the index finger defines the zooming state. The center division corresponds to no zoom and is idle state. Going to the immediate left zooms out, while going to the leftmost zooms out at a much faster rate. Going to the right zooms in.
* In case of scaling mode, the mouse pointer follows the base of the index finger and moving the hand will scale up or down based on the behavior of the mouse pointer.

> For scaling mode, if you are satisfied with the changes, do the initial gesture of bringing landmarks 4 and 8 close to stimulate a `right-click` on the mouse and accept the changes, else use the gesture in section `d)` to cancel the placement.

### f) Rotating in all modes

To begin rotating in any of the modes, bring the tip of the right hand thumb close to the tip of the **right hand middle finger [Landmarks 4 & 12]**.

Illustration:

![Pinch index](../master/Imgs-for-documentation/pinch-middle.png)

> The mouse pointer follows the base of the index finger and moving the hand will rotate the scene or the objects based on the chosen operation mode.
For object and edit modes, if you are satisfied with the changes, do the initial gesture of bringing landmarks 4 and 12 close to stimulate a `right-click` on the mouse and accept the changes, else use the gesture in section `d)` to cancel the placement.

### g) Panning in scene navigation and moving objects in object/edit mode

For these operations, bring the make a fist such that tips of all fingers are below their respective bases for the **right hand [Landmarks 5, 8 & 9, 12 & 13, 16 & 17, 20]**.

Illustration:

![Pinch index](../master/Imgs-for-documentation/fist-panning.png)

* In case of panning mode, the position of the base of the index finger defines the panning direction. The center division corresponds to no movement and is idle state. Going to the immediate left pans left, while going to the leftmost pans left at a much faster rate. Similarly right, up and down pan in said directions.
* In case of moving mode, the mouse pointer follows the base of the index finger and moving the hand will move the object along with it.

> For moving mode, if you are satisfied with the changes, do the initial gesture of making a fist to stimulate a `right-click` on the mouse and accept the changes, else use the gesture in section `d)` to cancel the placement.

I think that about covers up everything, if you face any issues, feel free to open an issue or send me a mail at prateekdhaka@hotmail.com, I will surely respond as soon as I see the issue/mail. I wrote this with 3 days of no sleep, so please feel free to point out any mistakes.

Lots of love to anyone who tries this out and gives feedback. Thanks, you rock.