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
    human_move()
    if check_game_won(): break

sys.exit(0)
