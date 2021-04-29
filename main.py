import usb_hid
from rgbkeypad import RGBKeypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from random import randint

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
    (0,0): {"color" : (200,0,0), "name" : "start"},
    (1,0): {"color" : (0,0,200), "name" : "stop"},
    (2,0): {"color" : (0,0,0), "name" : "n/a"},
    (3,0): {"color" : (0,0,0), "name" : "n/a"},
    
    (0,1): {"color" : (0,0,0), "name" : "n/a"},
    (1,1): {"color" : (0,0,0), "name" : "n/a"},
    (2,1): {"color" : (0,0,0), "name" : "n/a"},
    (3,1): {"color" : (0,0,0), "name" : "n/a"},

    (0,2): {"color" : (0,200,0), "name" : "Camera"},
    (1,2): {"color" : (0,0,0), "name" : "n/a"},
    (2,2): {"color" : (0,0,0), "name" : "n/a"},
    (3,2): {"color" : (0,0,0), "name" : "n/a"},

    (0,3): {"color" : (245,120,10), "name" : "Screen + Camera Top Right"},
    (1,3): {"color" : (245,120,10), "name" : "Screen + Camera Top Right"},
    (2,3): {"color" : (0,0,0), "name" : "n/a"},
    (3,3): {"color" : (0,100,100), "name" : "Screen Only"}
}


INVALID_KEY_COLOR = (255, 0, 0)
DEFAULT_BRIGHTNESS = 0.05

keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)

def resetBrightness():
    for key in keypad.keys:
        key.brightness = DEFAULT_BRIGHTNESS
        
def dimmBrightness():
    for key in keypad.keys:
        key.brightness = 0 # off the led
    
for key in keypad.keys:
    if (key.x, key.y) in KEY_COLOR_MAP.keys():
        key.color = KEY_COLOR_MAP[(key.x, key.y)]["color"]
    key.brightness = DEFAULT_BRIGHTNESS


while True:
    for key in keypad.keys:
        if key.is_pressed():
            resetBrightness();
            key.brightness = 0.5
            
            if (key.x, key.y) in KEYBOARD_MAP.keys():
                kbd.send(*KEYBOARD_MAP[(key.x, key.y)]) 
            else:
                key.color = (255,255,255)
                dimmBrightness()
            
            while key.is_pressed():
                pass
