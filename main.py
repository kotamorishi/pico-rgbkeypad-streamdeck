DISABLE_OLED = False
if(DISABLE_OLED == False):
    import oled
    oled.init()
import time
startTime = time.monotonic_ns()

import usb_hid
from rgbkeypad import RGBKeypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from random import randint
import math

KEYBOARD_MAP = {
    (0,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ONE,),   # 0
    (1,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_TWO,),   # 1
    (2,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_THREE,), # 2
    #(3,0): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FOUR,),  # 3
    
    (0,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_FIVE,),  # 4
    (1,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SIX,),   # 5
    (2,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_SEVEN,), # 6
    (3,1): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_EIGHT,), # 7
    
    (0,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_NINE,),  # 8
    (1,2): (Keycode.LEFT_CONTROL, Keycode.KEYPAD_ZERO,),  # 9
    (2,2): (Keycode.LEFT_ALT, Keycode.KEYPAD_ONE,),       # A
    (3,2): (Keycode.LEFT_ALT, Keycode.KEYPAD_TWO,),       # B
    
    (0,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_THREE,),     # C
    (1,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FOUR,),      # D
    (2,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_FIVE,),      # E
    (3,3): (Keycode.LEFT_ALT, Keycode.KEYPAD_SIX,)        # F
}

KEY_COLOR_MAP = {
    (0,0): {"color" : (200,0,0), "name" : "START Streaming", "confirm" : "yes"},
    (1,0): {"color" : (0,0,200), "name" : "STOP Streaming", "confirm" : "yes"},
    (2,0): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (3,0): {"color" : (0,10,0), "name" : "n/a", "confirm" : "no"},
    
    (0,1): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (1,1): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (2,1): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (3,1): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},

    (0,2): {"color" : (0,200,0), "name" : "Camera", "confirm" : "no"},
    (1,2): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (2,2): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (3,2): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},

    (0,3): {"color" : (245,120,10), "name" : "Screen + Camera Top", "confirm" : "yes"},
    (1,3): {"color" : (245,120,10), "name" : "Screen + Camera Down", "confirm" : "no"},
    (2,3): {"color" : (0,0,0), "name" : "n/a", "confirm" : "no"},
    (3,3): {"color" : (0,100,100), "name" : "Screen Only", "confirm" : "no"}
}


INVALID_KEY_COLOR = (255, 0, 0)
DEFAULT_BRIGHTNESS = 0.05

keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)

def resetBrightness():
    for key in keypad.keys:
        if (key.x, key.y) in KEY_COLOR_MAP.keys():
            key.color = KEY_COLOR_MAP[(key.x, key.y)]["color"]
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
    if(DISABLE_OLED == False):
        oled.setConfirmMmessage(text)
        startTime = time.monotonic_ns()
    
def partyNight():
    targetColors = []     # color array
    for key in keypad.keys:
        key.color = (randint(0,255), randint(0,255), randint(0,255))
        key.brightness = DEFAULT_BRIGHTNESS
        targetColors.append(key.color)
    
    while True:
        # change each
        i = randint(0,15)
        for key in keypad.keys:
            if key.is_pressed():
                # any key to exit par2ty mode
                return
        while True:
            if(
                (keypad.keys[i].color[0] == targetColors[i][0]) and
                (keypad.keys[i].color[1] == targetColors[i][1]) and
                (keypad.keys[i].color[2] == targetColors[i][2])):
                targetColors[i] = (randint(0,255), randint(0,255), randint(0,255))
                break
            else:
                keypad.keys[i].color = (
                    gradationAmount(keypad.keys[i].color[0], targetColors[i][0]), # R
                    gradationAmount(keypad.keys[i].color[1], targetColors[i][1]), # G
                    gradationAmount(keypad.keys[i].color[2], targetColors[i][2])) # B


def gradationAmount(current, tobe):
    if(current == tobe):
        return current
    elif(current > tobe):
        diff = current - tobe
        return current - math.ceil(diff / 15.0)
    else:
        diff = tobe - current
        return current + math.ceil(diff / 15.0)

    
def confirm(confirmKey, currentKey):

    showConfirmMessage(KEY_COLOR_MAP[confirmKey]["name"])
    
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
                    showMessage(KEY_COLOR_MAP[confirmKey]["name"])
                    key.brightness = 0.35
                    kbd.send(*KEYBOARD_MAP[(key.x, key.y)])
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
                    if(KEY_COLOR_MAP[(key.x, key.y)]["confirm"] == "yes"):
                        confirm((key.x, key.y), key)
                        break
                    else:
                        kbd.send(*KEYBOARD_MAP[(key.x, key.y)])
                        showMessage(KEY_COLOR_MAP[(key.x, key.y)]["name"])

                else:
                    key.color = (255,255,255)
                    dimmBrightness()
                    resetBrightness()
                    break
                
                while key.is_pressed():
                    pass

resetBrightness()
main()
