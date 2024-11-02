# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
import keypad
import time

km = keypad.KeyMatrix(
    row_pins=(board.GP2, board.GP3, board.GP4, board.GP5),
    column_pins=(board.GP6, board.GP7, board.GP8, board.GP9),
)

layer_0 = {
    0: "1",
    1: "2",
    2: "*",
    3: "3",
    4: "4",
    5: "5",
    6: "/",
    7: "6",
    8: "7",
    9: "8",
    10: "L_u",
    11: "9",
    12: "C",
    13: "0",
    14: "L_d",
    15: "=",
}


layer_1 = {
    0: "+",
    1: "<-",
    2: "(",
    3: "3",
    4: "-",
    5: "5",
    6: ")",
    7: "6",
    8: "7",
    9: "8",
    10: "L_u",
    11: "9",
    12: "C",
    13: "0",
    14: "L_d",
    15: "=",
}

layers = [layer_0, layer_1]
# Support both 8.x.x and 9.x.x. Change when 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(clock=board.GP14, MOSI=board.GP15)
tft_cs = board.GP22
tft_dc = board.GP27

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP26)

display = ST7735R(display_bus, width=160, height=128, rotation=270, bgr=True)

splash = displayio.Group()
display.root_group = splash

# index_layer_txt = 0
layer_txt = ['layer 0', 'layer 1', 'layer 2', 'layer 3', 'layer 4', 'layer 5', 'layer 6', 'layer 7', 'layer 8', 'layer 9']

splash2 = displayio.Group()
display.root_group = splash2
text_area2 = label.Label(terminalio.FONT, text=layer_txt[0], color=0xFFFFFF, x=115, y=120)
splash2.append(text_area2)

color_bitmap = displayio.Bitmap(160, 80, 1)
color_palette = displayio.Palette(1)
# write some text in each font color, rgb, cmyk
color_palette[0] = 0x00FF00  # green
s = ''
index_layer = 0

def result_formating(s: str):

    s_display = ''
    for i in range(6):
        if len(s) > 24:
            s_display += s[:24] + '\n'
            s = s[24:]
    s_display += s[:24] + '\n'
    return s_display

def logic_layers(key_name):
    global index_layer

    if key_name == 'L_u' and index_layer != len(layers)-1:
        index_layer += 1
    elif key_name == 'L_d' and index_layer !=0:
        index_layer -= 1

def calc(key_name):
                global s, splash, display

                if key_name == 'C':
                    s = ''
                elif key_name == '<-':
                    s = s[:len(s)-1]
                    
                    splash = displayio.Group()
                    display.root_group = splash
                else:
                    if key_name == 'L_d' or key_name == 'L_u':
                        pass
                    elif key_name == 'sqrt':
                        s += 'sqrt'
                    else:
                        s += key_name
                
                if key_name == '=':

                    if 'sqrt' in s:

                        from math import sqrt
                        num = s[s.find('sqrt(')+5:s.find(')')] 
                        s = str(sqrt(float(num))) 
                    s_format = s.replace('\n','')
                    r = str(eval(s_format[:len(s_format)-1]))
                    s = result_formating(s_format+r)

                if len(s) == 24:
                        s += '\n'
                elif len(s) == 24*2:
                    s += '\n'
                elif len(s) == 24*3:
                    s+= '\n'
                elif len(s) == 24* 4:
                    s += '\n'
                elif len(s) == 24 * 5:
                    s += '\n'
                elif len(s) == 24 * 6:
                    s += '\n'


while True:
    event = km.events.get()
    if event:
        if event.pressed:
            
            # Получаем номер нажатой клавиши
            key_number = event.key_number
            # Получаем название клавиши
            key_name = layers[index_layer].get(key_number, "Неизвестная клавиша")
            # print(f"Нажата: {key_name}")
            
            logic_layers(key_name)

            calc(key_name)


        # update display
        splash = displayio.Group()
        display.root_group = splash
        
        text = s

        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=10)

        splash.append(text_area)
         
        text_area2 = label.Label(terminalio.FONT, text=layer_txt[index_layer], color=0xFFFFFF, x=115, y=120)
        splash.append(text_area2)
