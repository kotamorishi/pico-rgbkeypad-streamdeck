# Pico RGB Keypad Stream Deck with OLED monitor
![lib directory contents](/images/oled_mod.jpg)

# 3D print
Case are not nessesary, however it makes nicer :)
You can feel free to download stl files and print it.
[https://www.thingiverse.com/thing:4883873](https://www.thingiverse.com/thing:4883873)

# Pico RGB Keypad Stream Deck
This repository is all based on the incredible work by [Martin O'Hanlon](https://github.com/martinohanlon/pico-rgbkeypad) for controlling the [Pico RGB Keypad](https://shop.pimoroni.com/products/pico-rgb-keypad-base) for the [Raspberry Pi Pico](https://www.raspberrypi.org/documentation/pico/getting-started/)

The instructions and software in this repository will guide you through setting up your Pico RGB Keypad to be used as a stream deck device for [OBS Studio](https://obsproject.com).

![Pimoroni RGB Keypad](https://cdn.shopify.com/s/files/1/0174/1800/products/pico-addons-2_1024x1024.jpg?v=1611177905)

# Getting Started
If you've not setup your Raspberry Pi Pico I recommend following the [getting started guide](https://learn.pimoroni.com/tutorial/hel/getting-started-with-pico) over on [https://learn.pirimon.com](https://learn.pimoroni.com) to get familiar with the process.

The guide will talk you through installing the [Pimoroni MicroPython Firmware](https://github.com/pimoroni/pimoroni-pico/releases) (time of writing `pimoroni-pico-micropython.uf2 .uf2` version 0.0.8 Alpha) and how to write Python code and get it deployed onto your Pico with [Thonny](https://thonny.org/) a lite Python IDE for beginners.

## CircuitPython Firmware
The above links described the process of installing the MicroPython Firmware however for our example we're going to install the [CircuitPython Firmware](https://circuitpython.org/board/raspberry_pi_pico/) which will replace the currently installed Pimoroni MicroPython Firmware.

1) Download the [latest firmware](https://circuitpython.org/board/raspberry_pi_pico/), at the time of writing this file is `adafruit-circuitpython-raspberry_pi_pico-en_US-6.2.0-beta.2.uf2`
1) Boot your Raspberry Pico into bootloader mode by holding down the "BOOTSEL" button whilst plugging in the USB cable.
1) The Pico will boot and display in file explorer on your PC/Laptop.
1) Copy the downloaded `adafruit-circuitpython-raspberry_pi_pico-en_US-6.2.0-beta.2.uf2` file across to the explorer window.  After a few seconds your Pico will reboot and you'll be running CircuitPython.

## Adafruit CircuitPython
With the CircuitPython Firmware installed we are going to install Adafruit CircuitPython package.  This package includes various modules for interacting with the Pico device and add-on boards, particularly the Pico RGB Keypad. 

The Adafruit CircuitPython package is required to get our example up and running so head on over to the Adafruit CircuitPython GitHub page and checkout their latest [releases](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases).  We're looking to download the `py` bundle which, at the time of writing is labelled `adafruit-circuitpython-bundle-py-20210225.zip`

> Please note the date stamp used in the filename may differ depending on when you are reading this article.  It ~will~ should be fine to download the latest bundle so long as you download the `py` bundle.

## Martin O'Hanlon's Pico RGB Keypad
Download the powerful [Pico RGB Keypad](https://github.com/martinohanlon/pico-rgbkeypad/blob/main/rgbkeypad/rgbkeypad.py) module by Martin O'Hanlon.  

## Installation
Now we are going to combine the required files from the Adafruit CircuitPython bundle and Martin O'Hanlon Pico RGB Keypad module.

Create a directory on your local machine called "OBS Interface".  This will store the files we will copy to our Pico device.

Inside the "OBS Interface" directory create another directory called "lib".

Open the Adafruit CircuitPython archive bundle `adafruit-circuitpython-bundle-py-20210225.zip` and extract the directory "adafruit_hid" into the "lib" directory so we end up with `OBS Interface\lib\adafruit_hid\`

Now copy Martin O'Hanlon `rgbkeypad.py` module into the "lib" directory so we end up with `OBS Interface\lib\rgbkeypad.py`

Our "lib" directory structure should look like this:

![lib directory contents](/images/lib_contents.png)

From this repository save the `main.py` file into the "OBS Interface" root directory so we end up with `OBS Interface\main.py`

Our "OBS Interface" root directory structure should look like this:

![OBS Interface directory contents](/images/root_contents.png)

Now to get these files copied over to the Pico.

Now Copy the `lib` directory and `main.py` file to the Pico so we have the following structure:

![Pico directory contents](/images/pico_contents.png)

If you wish you can use Thonny to push your code in `main.py` to the Pico 🙂

## Keyboard Mapping
The keyboard mapping used to control OBS Studio is is found within the `main.py` file.  When the button on the Pico RGB Keypad are pressed the corresponding key combination is sent to your PC/Laptop:

| Pico Button  	| Key Combination   	|
|---	        |---	                |
| 0   	        | Left Ctrl + KeyPad 1  |
| 1  	        | Left Ctrl + KeyPad 2  |
| 2  	        | Left Ctrl + KeyPad 3  |
| 3  	        | Left Ctrl + KeyPad 4  |
| 4  	        | Left Ctrl + KeyPad 5  |
| 5  	        | Left Ctrl + KeyPad 6  |
| 6  	        | Left Ctrl + KeyPad 7  |
| 7  	        | Left Ctrl + KeyPad 8  |
| 8  	        | Left Ctrl + KeyPad 9  |
| 9  	        | Left Ctrl + KeyPad 0  |
| A  	        | Left Alt + KeyPad 1   |
| B  	        | Left Alt + KeyPad 2   |
| C  	        | Left Alt + KeyPad 3   |
| D  	        | Left Alt + KeyPad 4   |
| E  	        | Left Alt + KeyPad 5   |
| F  	        | Left Alt + KeyPad 6   |

If you wish to use different keycodes then checkout the [Adafruit CircuitPython HID](https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keycode.py) module.

Please feel free to use Thonny and amend the key combinations as you see fit, just remember to run/upload your script to the Pico via Thonny. 

In order to get these key combination working in OBS Studio you need to map the key combinations to the "Hotkeys" function in OBS Studio. For example, the bottom right corner button "F" on the Pico RGB Keypad is mapped to the `Left Alt + KeyPad 6` combination.  In OBS Studio open "Settings" -> "Hotkeys" and map your desired function as `Left Alt + KeyPad 6`.  It should appear like this:

![OBS Hotkey Mapping](/images/obs_hotkey.png)

Feel free to clone this repo and modify `main.py` to your own needs. I've included my 'lib' directory as reference along with the CircuitPython firmware but I recommend you download them from the official sources mentioned in this guide.

Don't forget to checkout [Martin O'Hanlon](https://github.com/martinohanlon/pico-rgbkeypad) module to ready about the various API functions for interacting with the Pico RGB Keypad!
