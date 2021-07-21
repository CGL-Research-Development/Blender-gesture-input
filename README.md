# Blender gesture input

So, as the name suggests, this repo has a code which allows you to do some basic work in blender using hand gestures. It is of course limited as the gesture complexity would become too much.

First off, setting it all up. I'll include the whole abc, starting from installing the required libraries, so let's get to it.

***Note:** The code makes use of the Python language, which can be downloaded from [here](https://www.python.org/downloads/). The installation is quite easy and there is no complex setup required. Just remember to check the 'Add to path' option when installing.*

```
1. Installing libraries:
```

This is a one time setup you'll require to ever use the code. Just open command prompt or terminal depending on the OS you use, and put in a few simple lines.

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
python3 -m pip install xyz
```

```
2. Running the code:
```

Open the folder containing the file named **final.py** and open the file using python.

![Open file](../master/Imgs-for-documentation/Open-file.png)

```
Gesture list:
```

> Please refer to this image to know the locations of the landmarks mentioned in the documentation below

![Landmarks](../master/Imgs-for-documentation/hand_landmarks.png)

> 1. Enabling the master switch to start accepting inputs:

To make the code start accepting gestures, move the tip of your index and middle finger of your right hand [Landmarks 8 and 12] in the green box on the top right of the screen. When the box turns red, the code is now accepting inputs from you and all the gestures will be enabled. The on/off state of the code can be checked by the color of the box in the upper right. <br>
Red: The code is running and selecting the red box will cause it to stop. <br>
Green: The code is currently NOT running. Move landmarks 8 and 12 in the green region to start the code.

The screen will look something like this:
![Base state](../master/Imgs-for-documentation/Master-switch.png)

***Points to note:***
1. The master switch will only work with the right hand and using the left hand will not enable it. I have plans to enable a switch for left handed people, which is currently absent.
2. As soon as the code stops detecting a hand on the screen, it will automatically set the Master switch to off.

