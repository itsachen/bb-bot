#!/usr/bin/python2.7

import sys, math, time, random
from autopy import *
from board import *
import screenpixel
import Quartz.CoreGraphics as CG
import color
from pudb import set_trace

SLEEP_TIME = 0.2
CELL_WIDTH = 40
# START_PIXEL_COLOR = 0x53393a # 46210a?
START_PIXEL_COLOR = 0x4f3b3b
START_PIXEL_COLOR_RIGHT = 0x352016
START_PIXEL_COLOR_LEFT = 0x53393a

SWAP_CLICK_DELAY = .2
NEXT_MOVE_DELAY = .1

# raw_input("Press Enter to start...")

# region = CG.CGRectMake(mouse.get_pos()[0], mouse.get_pos()[1], 100, 100)
# sp = screenpixel.ScreenPixel()
# sp.capture(region=region)
# result = sp.pixel(10,10)

# print "R: " + `result[0]` + " G: " + `result[1]` + " B: " + `result[2]`

# print "ALL YOUR BASE ARE BELONG TO US"
  
def make_move(((x,y),orient),board):
    print "A"
    mouse.move(board.topleft_x + 40*x,board.topleft_y + 40*y)
    time.sleep(.001)
    mouse.click()
    time.sleep(SWAP_CLICK_DELAY)
    if orient == 1: #Right
        print "B"
        mouse.move(board.topleft_x + 40*(x+1),board.topleft_y + 40*y)
        time.sleep(.001)
        mouse.click()
        time.sleep(NEXT_MOVE_DELAY)
    elif orient == -2:
        print "B"
        mouse.move(board.topleft_x + 40*x,board.topleft_y + 40*(y+1))
        time.sleep(.001)
        mouse.click()
        time.sleep(NEXT_MOVE_DELAY)

def main():

    board = Board()
    # board.scan_cell()

    for cycle in range(99): #Number of rounds
        maxdepth = 3 
        depth = 0

        board.scan_board()

        corrupted = board.corrupted_board()
        rescan_count = 0

        while corrupted and rescan_count <= 10:
            # Coin?
            print "Rescanning.."
            board.scan_board()
            corrupted = board.corrupted_board()
            rescan_count += 1

        firstmove = Move(0,[("#","#")],("#","#"),0,board.board_state)

        movequeue = []
        movequeue.append(firstmove)
        maxmove = firstmove
        queuecount = 0

        continue_generating = True

        # board.scan_cell()
        # set_trace()
        print "Calculating moves..."
        while movequeue:
            queuecount += 1
            if queuecount > 1500:
                break
            move = movequeue[0]
            movequeue = movequeue[1:]

            if move.depth > depth:
                depth = move.depth
            if depth >= maxdepth:
                continue_generating = False
            if move.points > maxmove.points:
                maxmove = move

            if continue_generating:
                movequeue += possible_moves(move)

        for m in maxmove.prev_moves[1:]:
            print m
            make_move(m,board)

        # print maxmove.prev_moves
        # print maxmove.points


# This is the standar boilerplate that calls the main() function
if __name__ == '__main__':
    main()

