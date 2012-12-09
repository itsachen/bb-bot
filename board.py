from array import *

class Board:
  """Contains the state of the game board"""
  def __init__(self):
    """Initializes the board"""
    self.board_state = [[0,0,0,0,0,0,0,0] for x in range(8)]
    
  def scan_board(self):
    """Scans the board and updates the board_state"""
    
    