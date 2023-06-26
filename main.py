import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc


class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def main():
    """
    Main function for the program
    """
    # Countdown to Repair
    x = 0
    fishCaught = 0

    # Max cast is 1.9 secs
    # Base time it will always cast at
    castingBaseTime = 1.0
    # Max random amount of time to add to the base
    castingRandom = .4

    # How long to slack the line
    lineSlackTime = 1.6

    # Adding randomness to the wait times for the animations
    animationSleepTime = .1 + (.1 * random.random())

    # Randomly will move right or left to keep from AFKing
    moveDirection = ["a", "d"]

    # Free cam key
    freeCamKey = "alt"

    # Finds all Windows with the title "New World"
    newWorldWindows = pyautogui.getWindowsWithTitle("New World")

    # Find the Window titled exactly "New World" (typically the actual game)
    for window in newWorldWindows:
        if window.title == "New World":
            newWorldWindow = window
            break

    # Select that Window
    newWorldWindow.activate()

    # Move your mouse to the center of the game window
    centerW = newWorldWindow.left + (newWorldWindow.width / 2)
    centerH = newWorldWindow.top + (newWorldWindow.height / 2)
    pyautogui.moveTo(centerW, centerH)

    # Clicky Clicky
    time.sleep(animationSleepTime)
    pyautogui.click()
    time.sleep(animationSleepTime)

    # Selecting the middle 3rd of the New World Window
    mssRegion = {"mon": 1, "top": newWorldWindow.top, "left": newWorldWindow.left,
                 "width": round(newWorldWindow.width), "height": newWorldWindow.height}

    # Starting screenshotting object
    sct = mss.mss()

    # This should resolve issues with the first cast being short
    time.sleep(animationSleepTime * 3)

    while True:
        # Screenshot
        sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
        # Calculating those times
        castingTime = castingBaseTime + (castingRandom * random.random())

        # Hold the "Free Look" Button
        print(Colors.LIGHT_GREEN + "Holding Free Look Button")
        pydirectinput.keyDown(freeCamKey)

        # Like it says, casting
        print(Colors.LIGHT_GREEN + "Casting Line")
        pyautogui.mouseDown()
        time.sleep(castingTime)
        pyautogui.mouseUp()

        # Looking for the fish icon, doing forced garbage collection
        while pyautogui.locate("imgs/fishIcon.png", sctImg, grayscale=True, confidence=.55) is None:
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

        # Hooking the fish
        print(Colors.LIGHT_GREEN + "Fish Hooked")
        pyautogui.click()
        time.sleep(animationSleepTime)

        # Keeps reeling into "HOLD Cast" text shows on screen
        while pyautogui.locate("imgs/holdCast.png", sctImg, grayscale=True, confidence=.55) is None:
            print(Colors.GREEN + "Reeling....")
            pyautogui.mouseDown()

            # If icon is in the orange area slack the line
            if pyautogui.locate("imgs/fishReelingOrange.png", sctImg, grayscale=True, confidence=.75) is not None:
                print(Colors.LIGHT_RED + "Slacking line...")
                pyautogui.mouseUp()
                time.sleep(lineSlackTime)

            # Uses a lot of memory if you don't force collection
            gc.collect()
            # Screenshot
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

            # Reel downtime
            time.sleep(animationSleepTime)

        pyautogui.mouseUp()
        time.sleep(animationSleepTime)
        fishCaught = fishCaught + 1
        print(Colors.LIGHT_BLUE + "Caught Fish: " + str(fishCaught))

        # 20% chance to move to avoid AFK timer
        if random.randint(1, 5) == 5:
            key = moveDirection[random.randint(0, 1)]
            pyautogui.keyDown(key)
            time.sleep(.1)
            pyautogui.keyUp(key)

        time.sleep(animationSleepTime)

        # Release the "Free Look" Button
        print(Colors.LIGHT_GREEN + "Released Free Look Button")
        pydirectinput.keyUp(freeCamKey)


        # Repairing
        x = x + 1
        print("Repair after " + str(50 - x) + " more catch(es).")
        if x == 50:
            print("Repairing...")
            time.sleep(3)
            pyautogui.keyDown("tab")
            time.sleep(.1)
            pyautogui.keyUp("tab")
            time.sleep(1)
            if pyautogui.locateOnScreen("imgs/repair_all.png", sctImg, grayscale=True, confidence=.75) is not None:
                pos_repair_all = pyautogui.locateOnScreen("imgs/repair_all.png", sctImg, grayscale=True, confidence=.75)
                time.sleep(1)
                pyautogui.moveTo(pos_repair_all)
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                if pyautogui.locateOnScreen("imgs/repair_yes.png", sctImg, grayscale=True, confidence=.55) is not None:
                    pos_yes = pyautogui.locateOnScreen("imgs/repair_yes.png", sctImg, grayscale=True, confidence=.75)
                    time.sleep(1)
                    pyautogui.moveTo(pos_yes)
                    time.sleep(1)
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.keyDown("tab")
                    time.sleep(.1)
                    pyautogui.keyUp("tab")
                    x = 0
                    print("Repair Complete")
                    time.sleep(3)
                    pyautogui.keyDown("f3")
                    time.sleep(.1)
                    pyautogui.keyUp("f3")
                    time.sleep(4)
            else:
                pyautogui.keyDown("f3")
                time.sleep(.1)
                pyautogui.keyUp("f3")
        # End Repairing


# Runs the main function
if __name__ == '__main__':
    main()
