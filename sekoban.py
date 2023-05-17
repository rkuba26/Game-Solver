direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}
def initial():
    """
    Part of new_game: makes empty sets for each key
    """
    pieces = {"player": set(), "target": set(), \
              "wall": set(), "computer": set(), "open": set()}
    return pieces 

def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    data = initial()
    rows, cols = len(level_description),len(level_description[0])
    for row in range(rows):
        for col in range(cols):
            if not level_description[row][col]:
                continue
            for piece in level_description[row][col]:
                data[piece].add((row,col))
    data["x"] = (rows,cols)
    return data
    
def victory_check(game):
    """
    Checks that if there are computers and targets,
    that each computer is on a target
    If it isn't, the game isn't solved
    """
    compare = game["computer"] ^ game["target"]
    if not compare and game["computer"]: 
        return True
    return False

def change(coord,diff):
    """
    Find the coordinate adjacent to it
    """
    return (coord[0]+diff[0],coord[1]+diff[1])

def add_rem(sect,rem,add):
    """
    Changing the position of the player or computer
    """
    section = sect.copy()
    section.remove(rem)
    section.add(add)
    return section

def step_game(game, direction):
    """
    Two possible ways a player can move:
    1) The movement is to an empty space
    An empty space is defined as not having a computer or wall
    2) The movement pushes a computer into an empty space
    """
    wall_comp = lambda x: x in revised["wall"] or x in revised["computer"]
    computer = lambda x: x in revised["computer"]
    revised = game.copy()
    # Find the coordinate of the player
    (coord,) = revised["player"]
    add = direction_vector[direction]
    # New is the coordinate that the player wants to move to
    new = change(coord,add)
    # If New is empty space
    if not wall_comp(new) and not computer(new):
        revised["player"] = add_rem(game["player"],coord,new)
    elif computer(new):
        # Extra is the coordinate want to move computer to
        extra = change(new,add)
        # As long as extra is an empty space
        if not wall_comp(extra):
            revised["computer"] = add_rem(game["computer"],new,extra)
            revised["player"] = add_rem(game["player"],coord,new)
    return revised

def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    rows,cols = game["x"]
    representation = []
    for row in range(rows):
        curr_row = [[] for _ in range(cols)]
        representation.append(curr_row)
    for key in game: 
        if key in {"open", "x"}: 
            continue
        for row,col in game[key]: 
            representation[row][col].append(key)
    return representation

def neighbors(node,wall):
    neighbor = []
    info = {"player": {node[0]}, "computer": node[1], "wall": wall}
    for direction in direction_vector:
        neighbor.append(make_hash(step_game(info,direction),direction))
    return neighbor

def make_hash(game,direction = None):
    (player,) = game["player"]
    computers = game["computer"]
    return (player,computers,direction)

def seen_hash(made):
    return made[0] + (frozenset(made[1]),) + (made[2],)

def test(touching,coord,target):
    """
    The testing part of the terminate function
    """
    set1 = {(-1,0),(+1,0)}
    set2 = {(0,-1),(0,+1)}
    if len(touching) == 2 and not touching ^ set1 or not touching ^ set2:
        return True 
    elif len(touching) > 2 and coord not in target: 
        return True
    return False 

def terminate(neighbor,wall,target):
    """
    Looks thru all the coordinates adjacent to
    one of the computer sides
    If a computer is in a corner of a wall,
    This pathway will never solve the game, so
    it will return True (meaning it should terminate)
    """
    for coord in neighbor[1]: 
        adj = adjacent(coord)
        touching = {th for th in adj if th in wall}
        if test(touching,coord,target):
            return True
    return False 

def adjacent(coord):
    adjac = []
    add = list(direction_vector.values())
    for direction in add: 
        adjac.append(change(coord,direction))
    return adjac

def path(current):
    list1 = []
    for i in range(1, len(current)):
        list1.append(current[i][2])
    return list1

def solve_puzzle(game):
    """
    BFS
    Also checks if already solved at beginning
    """
    solved = lambda comp: not comp ^ target
    target = game["target"]
    wall = game["wall"]
    transform = make_hash(game)
    if solved(transform[1]):
        return []
    queue = [(transform,)]
    seen = {seen_hash(transform)}
    while queue: 
        look_at = queue.pop(0)
        for neighbor in neighbors(look_at[-1],wall):
            if seen_hash(neighbor) in seen:
                continue
            elif solved(neighbor[1]):
                return path(look_at + (neighbor,))
            seen.add(seen_hash(neighbor))
            if not terminate(neighbor,wall,target): 
                new_path = look_at + (neighbor,)
                queue.append(new_path)
    return None



