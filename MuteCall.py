import cv2
import pyautogui
import numpy as np
import keyboard

import configparser
import os
import sys
import shutil

from colorama import init, Fore, Back, Style
init()
# Get the directory of the .exe file (or .py file if running the script directly)
exe_dir = os.path.dirname(sys.executable)

# Check if we're running in a bundle
if getattr(sys, 'frozen', False):
    # If we are, use the directory of sys._MEIPASS as the base directory
    base_dir = sys._MEIPASS
else:
    # Otherwise, use the directory of this script file
    base_dir = exe_dir

# Define the files we want to extract
files_to_extract = ['Config.ini', 'Mute Call.png']

for filename in files_to_extract:
    bundled_path = os.path.join(base_dir, filename)
    external_path = os.path.join(exe_dir, filename)

    # If the file doesn't exist externally, copy it from the bundle
    if not os.path.exists(external_path):
        shutil.copy(bundled_path, external_path)

config = configparser.ConfigParser()
config.read('Config.ini')

Key = config.get('KEY', 'Key') # you can set this to anything incuding key + key (so like ctrl + q or something)

def find_and_click():
    # Load the template image (image of object you're looking for)
    template = cv2.imread('Mute Call.png', 0)

    w, h = template.shape[::-1]

    # Load the main image (screenshot of screen)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convert screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Get the location of the template in the screenshot
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Calculate the center point of the recognized image
    center_point = (top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2

    # Perform the click
    pyautogui.click(center_point)
    print("Clicked")

# Set up a hotkey that calls find_and_click() when 'ctrl + shift + a' is pressed
keyboard.add_hotkey(Key, find_and_click)

print("===================")
print(Fore.LIGHTGREEN_EX + "MADE BY: jaydaman53")
print("POGGIES")
print(Fore.RESET + "===================")

# Block the program, keeping it running in a loop to monitor for the hotkey press
keyboard.wait()
