from array import *
from autopy import *
import screenpixel
import time
from color import *
from pudb import set_trace # DEBUG

class Orientation:
    RIGHT = 1
    DOWN = -2

ORIENTATIONS = [Orientation.RIGHT, Orientation.DOWN]

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
                self.board_state[y_i][x_i] = color_abbreviation(get_simple_color_name(captured_color))
                # time.sleep(.1)
                
        self.print_board()

    def scan_cell(self):
        """Scans the cell at (x_initial,y_initial)"""

        sp = screenpixel.ScreenPixel()
        sp.capture()
        captured_color = sp.pixel_avg(self.topleft_x,self.topleft_y,3)
        print "RGB:" + `captured_color` + "\nColor: " + `get_colour_name(captured_color)` +"\nSimple color:" + `get_simple_color_name(captured_color)`

    def print_board(self):
        """Prints the board""" # MAKE PRETTIER LATER
        for row in self.board_state:
            print row

class Move:
  """Represents a move"""
    # depth
    # prev_moves - list of swaps - [((x1,y1),(x2,y2)),...]
    # current_move - swap tuple - (x1,y1),ORIENTATION
    # points accumulated so far (prev + move points + state points)
    # state (post falling combos (run function to modify board until score is zero))

  def __init__(self,d,prev_moves,current_move,points,board):
    self.depth = d
    self.prev_moves = prev_moves
    self.current_move = current_move
    self.points = points
    self.board = board

# @# TODO BURST MODE - Label entire shifted columns with an extra # to avoid

def possible_moves(move):
    movelist = []

    for y in range(0, 8):
        for x in range (0, 8):
            for orient in ORIENTATIONS:
                newboard = deep_copy(move.board)
                (new_points,return_board) = swap((x,y),orient,newboard)
                if new_points != 0:
                    oldlist = deep_copy(move.prev_moves)
                    newmove = Move(move.depth+1,oldlist.append(move),((x,y),orient),move.points + new_points,return_board)
                    movelist.append(newmove)

    print `len(movelist)` + " moves"
    for m in movelist:
        print "Move:" + `m.current_move` + " Points: " + `m.points`

def swap(gem_position,orientation,board):
    """Swaps gem at x,y with right or bottom gem, depending on orientation
       and returns (amount of points gained,altered board)"""

    # print "Testing swap at " + `gem_position` + " with direction " + `orientation` #DEBUG
    (x,y) = gem_position
    swapped_board = deep_copy(board)

    if x == 5 and y == 3:
        set_trace()

    # (x,y) is at a null space
    if board[y][x] == "#":
        return (0,board)
       
    if orientation == Orientation.RIGHT:
        # Swap both gems and check for valid patterns at both locations
        if x == 7 or board[y][x+1] == "#":
            return (0,board)
        temp = board[y][x+1]
        swapped_board[y][x+1] = board[y][x]
        swapped_board[y][x] = temp
        (points_so_far,transition_board) = compute_swap(gem_position,swapped_board)
        (new_points,final_board) = compute_swap((x+1,y),transition_board)
        if points_so_far + new_points == 0:
            # Nothing was achieved
            # print "No swap" #DEBUG
            return (0,board)
        else:
            # print ">hit" #DEBUG
            return (points_so_far+new_points,final_board)
    elif orientation == Orientation.DOWN:
        if y == 7 or board[y+1][x] == "#":
            return (0,board)
        temp = board[y+1][x]
        swapped_board[y+1][x] = board[y][x]
        swapped_board[y][x] = temp
        (points_so_far,transition_board) = compute_swap(gem_position,swapped_board)
        (new_points,final_board) = compute_swap((x,y+1),transition_board)
        if points_so_far + new_points == 0:
            # Nothing was achieved
            # print "No swap" #DEBUG
            return (0,board)
        else:
            # print ">hit" #DEBUG
            return (points_so_far + new_points,final_board)

def compute_swap(gem_position,board):
    """Searches (x,y) for any valid patterns and
       returns (amount of points gained,altered board)"""
    (x,y) = gem_position

    root_color = board[y][x]
    # print "==============================="
    # print_board_list(board)
    # print "==============================="
    # print "  > Root color of " + `root_color` + " at " + `(x,y)` #DEBUG

    points = 0
    changed_board = deep_copy(board)

    leftmost_position = gem_position
    rightmost_position = gem_position
    topmost_position = gem_position
    bottommost_position = gem_position

    # Check horizontal
    for x_right in range(x+1,8):
        if board[y][x_right] != root_color:
            break
        else:
            # print "    > Hit at " + `(x_right,y)` #DEBUG
            rightmost_position = (x_right,y)
    for x_left in range(x-1,-1,-1):
        if board[y][x_left] != root_color:
            break
        else:
            # print "    > Hit at " + `(x_left,y)` #DEBUG
            leftmost_position = (x_left,y)

    # Check vertical
    for y_top in range(y-1,-1,-1):
        if board[y_top][x] != root_color:
            break
        else:
            # print "    > Hit at " + `(x,y_top)` #DEBUG
            topmost_position = (x,y_top)
    for y_bottom in range(y+1,8):
        if board[y_bottom][x] != root_color:
            break
        else:
            # print "    > Hit at " + `(x,y_bottom)` #DEBUG
            bottommost_position = (x,y_bottom)

    # Pattern size calculations for point calculation and state changing
    pattern_width = rightmost_position[0] - leftmost_position[0] + 1
    pattern_height = bottommost_position[1] - topmost_position[1] + 1

    # BOTH?
    if (pattern_width >= 3) and (pattern_height >= 3):
        # COMPUTE CROSS SCORES AND SHIT
        points += 1000 # @# TODO: DOUBLE CHECK SCORES
        # MOVE CELLS
        # Move strategy similar to a combination of horizontal then vertical, 
        # except horizontal is without the root (to avoid double shifting)
        for y_shift in range(y-1,-1,-1): # Horizontal pattern shifting
            for x_shift in range(leftmost_position[0],x):
                changed_board[y_shift+1][x_shift] = board[y_shift][x_shift]
            for x_shift in range(x+1,rightmost_position[0]+1):
                changed_board[y_shift+1][x_shift] = board[y_shift][x_shift]
        for y_shift in range(y-pattern_height,-1,-1): # Vertical pattern shifting
            changed_board[y_shift+pattern_height][x] = board[y_shift][x]

        # FILL EMPTY SPACES
        for x_fill in range(leftmost_position[0],x): # Horizontal left
            changed_board[0][x_fill] = "#"
        for x_fill in range(x+1,rightmost_position[0]+1): # Horizontal right
            changed_board[0][x_fill] = "#"
        for y_fill in range(0,pattern_height): # Vertical
            changed_board[y_fill][x] = "#"

    # 3 or more horizontal?
    elif pattern_width >= 3:
        # ASSIGN POINTS
        if pattern_width == 3:
            points += 250
        elif pattern_width == 4: #FLAME
            points += 500
        elif pattern_width == 5: #HYPER
            points += 750 # @# TODO: DOUBLE CHECK SCORES, ADD SPECIAL GEMS
        # MOVE CELLS
        for y_shift in range(y-1,-1,-1):
            for x_shift in range(leftmost_position[0],rightmost_position[0]+1):
                changed_board[y_shift+1][x_shift] = board[y_shift][x_shift]
        # FILL EMPTY SPACES WITH #'s
        for x_fill in range(leftmost_position[0],rightmost_position[0]+1):
            changed_board[0][x_fill] = "#"

    # 3 or more veritcal
    elif pattern_height >= 3:
        # ASSIGN POINTS
        if pattern_height == 3:
            points += 250
        elif pattern_height == 4: #FLAME
            points += 500
        elif pattern_height == 5: #HYPER
            points += 750 # @# DOUBLE CHECK SCORES
        # Move cells
        for y_shift in range(y- pattern_height,-1,-1):
            changed_board[y_shift+pattern_height][x] = board[y_shift][x]
        # FILL EMPTY SPACES WITH #'s
        for y_fill in range(0,pattern_height):
            changed_board[y_fill][x] = "#"

    return (points,changed_board)

# ORIENTATION MACROS
def above((x,y)):
    return ((x,y-1))

def below((x,y)):
    return ((x,y+1))

def left((x,y)):
    return ((x-1,y))

def right((x,y)):
    return ((x+1,y))

def print_board_list(board):
    for row in board:
            print row

def deep_copy(matrix):
    return [row[:] for row in matrix]