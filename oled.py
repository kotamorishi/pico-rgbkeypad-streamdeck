import adafruit_ssd1306
import board
import busio
import terminalio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import adafruit_imageload
import time

# if you wish to use custom fonts...
from adafruit_bitmap_font import bitmap_font
font = bitmap_font.load_font("/font.bdf", displayio.Bitmap)


displayio.release_displays()

oled_reset = board.GP15 # what is this?

# Use for I2C
i2c = busio.I2C(board.GP7, board.GP6, frequency=400000)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C, reset=oled_reset)

# OLED Monitor size
WIDTH = 128
HEIGHT = 32
BORDER = 2

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

def init():
    # Make the display context
    splash = displayio.Group(max_size=10)
    display.show(splash)
    
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White
    
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
    )
    splash.append(inner_sprite)
    
    # Draw a label
    text = "OBS switcher"
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
        #font, text=text, color=0xFFFFFF, x=4, y=HEIGHT // 2 - 1
    )
    splash.append(text_area)

def sleep():
    splash = displayio.Group(max_size=10)
    display.show(splash)
    
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # off    
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

def setMmessage(text):
    splash = displayio.Group(max_size=1)
    display.show(splash)
    text_area = label.Label(
        terminalio.FONT,
        text=text,
        color=0xFFFFFF,
        x=4,
        y=HEIGHT // 2 - 1
        #font, text=text, color=0xFFFFFF, x=4, y=HEIGHT // 2 - 1
    )
    splash.append(text_area)

def setConfirmMmessage(text):
    splash = displayio.Group(max_size=1)
    display.show(splash)

    text_area2 = label.Label(
        terminalio.FONT,
        text="OK?",
        color=0xFFFFFF,
        x=4,
        y=16 // 2 - 1
        #font, text=text, color=0xFFFFFF, x=4, y=HEIGHT // 2 - 1
    )
    splash.append(text_area2)

    text_area = label.Label(
        terminalio.FONT,
        text="> " + text,
        color=0xFFFFFF,
        x=4,
        y=24
        #font, text=text, color=0xFFFFFF, x=4, y=HEIGHT // 2 - 1
    )
    splash.append(text_area)

    