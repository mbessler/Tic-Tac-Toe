#!/usr/bin/env python
# 
# This is Manuel Bessler's version of an interactive Tic-Tac-Toe game for the Tic-Tac-Toe challenge at
#    http://github.com/cmheisel/Tic-Tac-Toe
# 
# This implementation resides at http://github.com/mbessler/Tic-Tac-Toe
#
# This program was developed with the help of the following documents:
#  * http://en.wikipedia.org/wiki/Tic-tac-toe
#  * http://www.students.stedwards.edu/ccella/freeprog.html
#
# In the game of Tic-Tac-Toe, nobody can actually ever win if two equally strong opponents play against each other and both get to start the same number of rounds. 
# However, as the challenge calls for 'to never lose', this is possible since this does allow for a draw.
# 
# The 1983 film 'WarGames' used this theme to teach a military computer controlling nuclear warheads that there can be no winner.
#

import sys

grid = ['_'] * 9

# sets of winning positions
winning_pos = (
# check diagonal \
    [0, 4, 8],
# check diagonal /
    [2, 4, 6],
# check 3 horizontals 
    [0,1,2], [3,4,5], [6,7,8],
# check 3 verticals
    [0,3,6], [1,4,7], [2,5,8],
)

centerpos = 4
corners = [0,2,6,8]
middles = [1,3,5,7]
adjacent_corners = { 0:[2,6], 2:[0,8], 6:[0,8], 8:[2,6] }
edge_between_corners = { (0,2): 1, (2,8): 5, (0,6):3, (6,8):7 }
opposite_corners = { 0: 8, 2:6, 6:2, 8:0 }


def init():
    grid= ['_'] * 3 * 3


def is_oob(n):
    if n > 8 or n < 0:
        return true
    else:
        return false

def east_pos(n): # 0-based. -1 == not possible
    if (n+1)%3 != 0:
        return n+1
    else:
        return -1

def west_pos(n):
    if n%3 != 0:
        return n-1
    else:
        return -1

def north_pos(n):
    if n-3 < 0:
        return -1
    else:
        return n-3

def south_pos(n):
    if n+3 >= 9:
        return -1
    else:
        return n+3

def se_pos(n):
    s = south_pos(n)
    if s == -1: 
        return s
    e = east_pos(s)
    return e

def ne_pos(n):
    n = north_pos(n)
    if n == -1: 
        return n
    e = east_pos(n)
    return e

def sw_pos(n):
    s = south_pos(n)
    if s == -1: 
        return s
    w = west_pos(s)
    return w

def nw_pos(n):
    n = north_pos(n)
    if n == -1: 
        return n
    w = west_pos(n)
    return w




def check_game_won():
    for triple in winning_pos:
        if grid[triple[0]] == grid[triple[1]] and grid[triple[1]] == grid[triple[2]] and grid[triple[0]] in ('X', 'O'):
            print "%s WON" % grid[triple[0]]
            return True
    return False
    
def check_draw(): # assumes check_game_won is false
    for i in range(9):
        if grid[i] != 'X' and grid[i] != 'O':
            return False
    print "Game is a draw, nobody wins"
    return True


def strat_start():  # if the board is empty, start with a corner
    for i in range(9):
        if grid[i] in ('X', 'O'):
            return False
    grid[0] = 'X'
    return True

def strat_win():
    # already two in a winning set?
    for triple in winning_pos:
        i_have = 0
        you_have = 0
        put_pos = -1
        for pos in triple:
            if grid[pos] == 'X':
                i_have += 1
            elif grid[pos] == 'O':
                you_have += 1
            else:
                put_pos = pos
        if you_have == 0 and i_have == 2:
            # I win
            for pos in triple:
                grid[pos] = 'X'
            print "1. WIN computer puts 'X' in %d" % put_pos
            return True
    return False

def strat_block():
    # if opponent has already two in a winning set, block him
    for triple in winning_pos:
        i_have = 0
        you_have = 0
        put_pos = -1
        for pos in triple:
            if grid[pos] == 'X':
                i_have += 1
            elif grid[pos] == 'O':
                you_have += 1
            else:
                put_pos = pos
        if you_have == 2 and i_have == 0:
            # I block you
            for pos in triple:
                if grid[pos] != 'O':
                    grid[pos] = 'X'
            print "2. BLOCK computer puts 'X' in %d" % put_pos
            return True
    return False

def strat_fork_center():
    two_out_of_three = { (0,2):[1,6,8], (0,6):[2,3,8], (2,8):[0,5,6], (6,8):[0,2,7] }
    for corner in adjacent_corners.keys(): # find one corner where we already placed an 'X'
        if grid[corner] == 'X':
            for other_corner in adjacent_corners[corner]: # find an adjacent corner thats still empty
                if grid[other_corner] not in ('X', 'O'):
                    key = (corner,other_corner) if (corner<other_corner) else (other_corner,corner) # adjust for lookup
                    # check if we can still get at least two of three from the fields in the list to make a fork
                    toot = two_out_of_three[ key ]
                    i_have_or_avail = 0
                    for fld in toot:
                        if grid[fld] != 'O':
                            i_have_or_avail += 1
                    if i_have_or_avail >= 2:
                        grid[other_corner] = 'X'
                        print "3. FORK CENTER computer puts 'X' in %d" % other_corner
                        return True
    return False

def strat_fork_corner():
    for corner in corners:
        if grid[corner] == 'X': # do I have a corner?
            for other_corner in adjacent_corners[corner]: # find an adjacent corner thats still empty 
                if grid[other_corner] not in ('X', 'O'):
                    key = (corner,other_corner) if (corner<other_corner) else (other_corner,corner) # adjust for lookup
                    in_between = edge_between_corners[ key ]
                    if grid[in_between] not in ('X', 'O'):
                        grid[in_between] = 'X'
                        print "3. FORK CORNER A computer puts 'X' in %d" % in_between
                        return True
    for corner in corners:  # similar to above, but check opposite corner and center for availability
        if grid[corner] == 'X': # do I have a corner?
            if grid[centerpos] not in ('X', 'O') and opposite_corners[corner] not in ('X', 'O'): # get opposite corner
                grid[opposite_corners[corner]] = 'X'
                print "3. FORK CORNER B computer puts 'X' in %d" % opposite_corners[corner]
                return True
    return False

def strat_fork():
    if grid[centerpos] == 'X': # do I own the center?
        if strat_fork_center():
            return True
    # otherwise, do I have one of the corners to build a fork
    return strat_fork_corner()

def strat_fork_block():  # block fork possibilities of the opponent
    block_data = [ [0,8], [2,6] ] # the sets of opposing corners
    for check in block_data:
        # this triggers if I have center and opponent has two opposing corners
        if grid[check[0]] == 'O' and grid[check[1]] == 'O' and grid[centerpos] == 'X':
            # then I try to find an available edge position, this will block the opponent's fork 
            for edge in middles:
                if grid[edge] not in ('X', 'O'):
                    grid[edge] = 'X'
                    print "4. BLOCK FORK computer puts 'X' in %d" % edge
                    return True
    return False

def strat_center():
    if grid[centerpos] not in ('X', 'O'):
        grid[centerpos] = 'X'
        print "4. CENTER computer puts 'X' in %d" % centerpos
        return True
    return False

def strat_opposite_corner():
    for pos in opposite_corners.keys(): # the four corners
        if grid[pos] == 'O' and grid[opposite_corners[pos]] not in ('O', 'X'):
            grid[opposite_corners[pos]] = 'X'
            print "5. OPPOSITE CORNER computer puts 'X' in %d" % opposite_corners[pos]
            return True
    return False

def strat_empty_corner():
    for pos in corners: # the four corners
        if grid[pos] not in ('X', 'O'):
            grid[pos] = 'X'
            print "6. EMPTY CORNER computer puts 'X' in %d" % pos
            return True
    return False

def strat_empty_side():
    for pos in middles: # the middles of each side
        if grid[pos] not in ('X', 'O'):
            grid[pos] = 'X'
            print "7. EMPTY SIDE computer puts 'X' in %d" % pos
            return True
    return False


def computer_move(): # plays 'X'
    if strat_start() or strat_win() or strat_block() or strat_fork() or strat_fork_block() or strat_center() or strat_opposite_corner() or strat_empty_corner() or strat_empty_side(): # use short-circuiting
        return
    else:
        print "ERROR, computer did not move !!!!!!!"
    return

def print_grid():
    print "   | ABC "
    print "---+-----"
    for i in range(3):
        print " %d |" % (i+1),
        print ''.join(grid[i*3:i*3+3])

def human_move():
    print_grid()
    while True:
        print "Your Move",
        pos = raw_input()
        if len(pos) != 2: 
            print "invalid input, please try again"
            continue
        if pos[0] not in ('A', 'B', 'C'):
            print "invalid input for first coordinate, must be A, B, or C"
            continue
        if pos[1] not in ('1','2', '3'):
            print "invalid input for second coordinate, must be 1, 2, or 3"
            continue
        x = ord(pos[0])-ord('A')
        y = ord(pos[1])-ord('1')
        n = y * 3 + x # tranlate to array index
        if grid[n] == 'X' or grid[n] == 'O':
            print "position %s already used" % pos
            continue
        grid[n] = 'O'
        break

def who_starts():
    while True:
        print "Who will start, the computer ('X') or you ('O')? [X/O] ?",
        inp = raw_input()
        if inp in ('X', 'O'):
            return inp

print "Welcome to Tic-Tac-Toe."
print "The computer plays as 'X', and you will play as 'O'"
print "To place your mark ('O'), select an empty field using x/y coordinates, \n\tfor example: A1 or C2 or B3"

init()
starter = who_starts()
if starter == 'O': # human starts
    human_move()
while True:
    computer_move()
    if check_game_won(): break
    if check_draw(): break
    human_move()
    if check_game_won(): break
    if check_draw(): break

print_grid()
sys.exit(0)
