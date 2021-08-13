# Set ture for No-OLED monitor.
DISABLE_OLED = False
if(DISABLE_OLED == False):
    try:
        import oled
        oled.init()
    except:
        print("OLED not available to use.")
        DISABLE_OLED = True
import time
startTime = time.monotonic_ns()

import usb_hid
from rgbkeypad import RGBKeypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from random import randint
import math


# set name for "n/a" is not assigned. trigger for the party night mode ;-)
# name : display name
KEYBOARD_MAP = {
    (0,0): {"color" : (200,  0,  0), "name" : "START Streaming"     , "confirm" : "yes", "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ONE)   }, 
    (1,0): {"color" : (  0,  0,200), "name" : "STOP Streaming"      , "confirm" : "yes", "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_TWO)   },
    (2,0): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_THREE) },
    (3,0): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FOUR)  },
    
    (0,1): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FIVE)  },
    (1,1): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SIX)   },
    (2,1): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SEVEN) },
    (3,1): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_EIGHT) },

    (0,2): {"color" : (  0,200,  0), "name" : "Camera"              , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_NINE)  },
    (1,2): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ZERO)  },
    (2,2): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_ONE)   },
    (3,2): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_TWO)   },

    (0,3): {"color" : (245,120, 10), "name" : "Screen + Camera Top" , "confirm" : "yes", "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_THREE) },
    (1,3): {"color" : (245,120, 10), "name" : "Screen + Camera Down", "confirm" : "no" , "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_FOUR)  },
    (2,3): {"color" : (  0,  0,  0), "name" : "n/a"                 , "confirm" : "no" , "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_FIVE)  },
    (3,3): {"color" : (  0,100,100), "name" : "Screen Only"         , "confirm" : "no" , "keycode" : (Keycode.LEFT_ALT,     Keycode.KEYPAD_SIX)   }
}


INVALID_KEY_COLOR = (255, 0, 0)
DEFAULT_BRIGHTNESS = 0.05

keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)

def resetBrightness():
    for key in keypad.keys:
        if (key.x, key.y) in KEYBOARD_MAP.keys():
            key.color = KEYBOARD_MAP[(key.x, key.y)]["color"]
        key.brightness = DEFAULT_BRIGHTNESS
        
def dimmBrightness():
    #for key in keypad.keys:
    #    key.brightness = 0 # off the led
    if(DISABLE_OLED == False):
        oled.setMmessage(" ")
    partyNight()

def showMessage(text):
    global startTime
    if(DISABLE_OLED == False):
        oled.setMmessage(text)
        startTime = time.monotonic_ns()

def showConfirmMessage(text):
    global startTime
    startTime = time.monotonic_ns()
    if(DISABLE_OLED == False):
        oled.setConfirmMmessage(text)
    
def partyNight():
    targetColors = []     # color array
    minRVal = randint(1,200)
    minGVal = randint(1,200)
    minBVal = randint(1,200)
    for key in keypad.keys:
        key.color = (randint(minRVal,255), randint(minGVal,255), randint(minBVal,255))
        key.brightness = DEFAULT_BRIGHTNESS
        targetColors.append(key.color)
    
    while True:
        if(randint(0, 50) == 39):
            minRVal = randint(1,200)
            minGVal = randint(1,200)
            minBVal = randint(1,200)

        # change each
        changeKeys = []
        for i in range(randint(1,5)):
            # this could be duplicated - 2x or more speedy change.
            changeKeys.append(randint(0,15))

        while True:
            for i in changeKeys:
                for key in keypad.keys:
                    if key.is_pressed():
                        # any key to exit party mode
                        return

                if(gradationLED(keypad.keys[i], targetColors[i])):
                    targetColors[i] = (randint(minRVal,255), randint(minGVal,255), randint(minBVal,255))
                    break
            else:
                continue
            break
            
def gradationLED(key, tobe):
    if(
        (key.color[0] == tobe[0]) and
        (key.color[1] == tobe[1]) and
        (key.color[2] == tobe[2])):
        return True
    
    key.color = (
        gradationAmount(key.color[0], tobe[0]), # R
        gradationAmount(key.color[1], tobe[1]), # G
        gradationAmount(key.color[2], tobe[2])) # B
    return False

def gradationAmount(current, tobe):
    if(current == tobe):
        return current
    elif(current > tobe):
        diff = current - tobe
        return current - math.ceil(diff / 10.0)
    else:
        diff = tobe - current
        return current + math.ceil(diff / 10.0)

    
def confirm(confirmKey, currentKey):

    showConfirmMessage(KEYBOARD_MAP[confirmKey]["name"])
    
    # wait for 0.2 sec to avoid mis-click
    time.sleep(0.2)

    global startTime
    keyBrightnessAdjustment = 0.03
    while True:
        currentKey.brightness = currentKey.brightness + keyBrightnessAdjustment
        if(currentKey.brightness > 0.7):
            keyBrightnessAdjustment = -0.03
        if(currentKey.brightness < 0.2):
            keyBrightnessAdjustment = 0.03

        ms_duration = round((time.monotonic_ns() - startTime) / 1e6, 1)
            
        if(ms_duration > 10000): # 10 sec
            # not confirmed within 10 seconds
            showMessage("Cancelled")
            currentKey.brightness = DEFAULT_BRIGHTNESS
            return

        for key in keypad.keys:
            if key.is_pressed():
                #3resetBrightness();
                
                if((key.x, key.y)  == confirmKey):
                    showMessage(KEYBOARD_MAP[confirmKey]["name"])
                    key.brightness = 0.35
                    kbd.send(*KEYBOARD_MAP[(key.x, key.y)]["keycode"])
                else:
                    # cancel with any other keys
                    showMessage("Cancelled")
                    currentKey.brightness = DEFAULT_BRIGHTNESS
                    
                while key.is_pressed():
                    pass
                return

def main():
    while True:

        if(DISABLE_OLED == False):
            ms_duration = round((time.monotonic_ns() - startTime) / 1e6, 1)
            if(ms_duration > 30000): # 30 sec
                oled.sleep()
            

        for key in keypad.keys:
            if key.is_pressed():
                resetBrightness();
                key.brightness = 0.35
                
                if (key.x, key.y) in KEYBOARD_MAP.keys():
                    if(KEYBOARD_MAP[(key.x, key.y)]["confirm"] == "yes"):
                        confirm((key.x, key.y), key)
                        break
                    else:
                        if(KEYBOARD_MAP[(key.x, key.y)]["name"] == "n/a"):
                            dimmBrightness()
                            resetBrightness()
                            break

                        kbd.send(*KEYBOARD_MAP[(key.x, key.y)]["keycode"])
                        showMessage(KEYBOARD_MAP[(key.x, key.y)]["name"])
                        

                
                while key.is_pressed():
                    pass
while True:
    try:
        resetBrightness()
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt :)")
        break
    except:
        # ignore any other errors.
        print("An exception occurred")
