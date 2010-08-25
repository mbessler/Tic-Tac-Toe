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

import sys

grid=' ' * 9

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

corners = [0,2,6,8]
middles = [1,3,5,7]
adjacent_corners = { 0:[2,6], 2:[0,8], 6:[0,8], 8:[2,6] }
edge_between_corners = { (0,2): 1, (2,8): 5, (0,6):3, (6,8):7 }
opposite_corners = { 0: 8, 2:6, 6:2, 8:0 }


def init():
    grid= '_' * 3 * 3


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


def computer_move(): # plays 'X'
    pass

def human_move():
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

init()
while True:
    computer_move()
    if check_game_won(): break
    if check_draw(): break
    human_move()
    if check_game_won(): break
    if check_draw(): break

sys.exit(0)
