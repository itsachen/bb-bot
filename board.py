from array import *
from autopy import *
import screenpixel
import time
import color

class Board:
    """Contains the state of the game board"""
    
    def __init__(self):
        """Initializes the board"""
        alert.alert("Place mouse on top left gem and press ENTER")
        (x_initial, y_initial) = mouse.get_pos()
        self.board_state = [[0,0,0,0,0,0,0,0] for x in range(8)]
        self.topleft_x = x_initial
        self.topleft_y = y_initial
    
    def scan_board(self):
        """Scans the board and updates the board_state"""

        sp = screenpixel.ScreenPixel()
        sp.capture()

        for y_i in range(0,8):
            for x_i in range(0,8):
                # mouse.move(self.topleft_x + 40*x_i,self.topleft_y + 40*y_i)
                captured_color = sp.pixel_avg(self.topleft_x + 40*x_i,self.topleft_y + 40*y_i,3) # Might need to increase the bitmap
                # print captured_color
                # print color.get_simple_color_name(captured_color)
                self.board_state[y_i][x_i] = color.color_abbreviation(color.get_simple_color_name(captured_color))
                # time.sleep(.1)
                
        self.print_board()

    def scan_cell(self):
        """Scans the cell at (x_initial,y_initial)"""

        sp = screenpixel.ScreenPixel()
        sp.capture()
        captured_color = sp.pixel_avg(self.topleft_x,self.topleft_y,3)
        print "RGB:" + `captured_color` + "\nColor:" + `color.get_simple_color_name(captured_color)`

    def print_board(self):
        """Prints the board""" # MAKE PRETTIER LATER
        for row in self.board_state:
            print row