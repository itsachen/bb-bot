#!/usr/bin/python2.7

import sys, math, time, random
from autopy import *
from board import Board
import screenpixel
import Quartz.CoreGraphics as CG
import color

SLEEP_TIME = 0.2
CELL_WIDTH = 40
# START_PIXEL_COLOR = 0x53393a # 46210a?
START_PIXEL_COLOR = 0x4f3b3b
START_PIXEL_COLOR_RIGHT = 0x352016
START_PIXEL_COLOR_LEFT = 0x53393a

# raw_input("Press Enter to start...")

# region = CG.CGRectMake(mouse.get_pos()[0], mouse.get_pos()[1], 100, 100)
# sp = screenpixel.ScreenPixel()
# sp.capture(region=region)
# result = sp.pixel(10,10)

# print "R: " + `result[0]` + " G: " + `result[1]` + " B: " + `result[2]`

# print "ALL YOUR BASE ARE BELONG TO US"

def calibrate_vertically(x, y):
  region = CG.CGRectMake(0,0, 900, 900)
  sp = screenpixel.ScreenPixel()
  sp.capture(region=region)
  final = (0,0)
  for i in range (0, 20):
    for j in range (-10, 10):
        p1 = sp.pixel(x + j, y - i)
        mouse.move(x + j, y - i)
        # print hex(color.rgb_to_hex(p1[0],p1[1],p1[2]))
        if (hex(color.rgb_to_hex(p1[0],p1[1],p1[2])) == hex(START_PIXEL_COLOR)):
            print "Match!"
            p2 = sp.pixel(x + j + 1, y - i)
            if (hex(color.rgb_to_hex(p2[0],p2[1],p2[2])) == hex(START_PIXEL_COLOR_RIGHT)):
                final = (x + j + 1, y - i - 1)
  mouse.move(final[0],final[1])
  

def main():
    # board = initialize_board()
    while True:
        alert.alert("Place mouse on top left corner and press ENTER")
        (x_initial, y_initial) = mouse.get_pos()
        print "X:" + `x_initial` + " Y:" + `y_initial`

        sp = screenpixel.ScreenPixel()
        sp.capture()
        captured_color = sp.pixel_avg(x_initial,y_initial)
        print captured_color
        print color.get_simple_color_name(captured_color)

    # calibrate_vertically(x_initial,y_initial)
    # (x, y) = calibrate_vertically(xTmp, yTmp)
    # if ( (x, y) == (0, 0)):
    #     print ("Couldn't find initial pixel for calibrate")
    #     return
    # else:
    #     print ("Found starting pixel at (%d, %d)" % (x, y))

    # for i in range (1, 10000):
    #     scan_board(board, x, y)
    #     make_move(board, x, y)
    #     time.sleep(SLEEP_TIME)

# This is the standar boilerplate that calls the main() function
if __name__ == '__main__':
    main()

