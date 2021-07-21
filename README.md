# Blender gesture input

So, as the name suggests, this repo has a code which allows you to do some basic work in blender using hand gestures. It is of course limited as the gesture complexity would become too much.

First off, setting it all up. I'll include the whole abc, starting from installing the required libraries, so let's get to it.

***Note:** The code makes use of the Python language, which can be downloaded from [here](https://www.python.org/downloads/). The installation is quite easy and there is no complex setup required. Just remember to check the 'Add to path' option when installing.*

> 1. Installing libraries:

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

> 2. Running the code:

Open the folder containing the file named **final.py** and open the file using python.

[Open file](/Imgs for documentation/Open file.png)
