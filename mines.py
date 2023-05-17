def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


def all_coord(dim):
    """Returns a list of all coordinates"""
    if len(dim) == 1:
        return [(i,) for i in range(dim[0])]
    return [j + (i,) for j in all_coord(dim[:-1]) for i in range(dim[-1])]

def neighbors(c,dim):
    """
    Determines the neighbors of a coordinate, c, in
    an arbitrary dimensioned board
    Does so recursively
    """
    delt = [-1,0,1]
    valid = lambda a,spec_dim: 0 <= a < spec_dim
    one = lambda i: [(c[i]+b,) for b in delt if valid(c[i]+b,dim[i])]
    if len(c) == 1: 
        return one(0)
    return [i + j for i in neighbors(c[:-1],dim[:-1]) for j in one(-1)]

def check(g,coords,target):
    """
    Check board and hidden for each
    coordinate to determine if victory (change if so)
    """
    bo,hi = g['board'],g['hidden']
    if target == '.':
        g['state'] = 'defeat'
        return 1
    for coord in coords:
        if get(hi,coord) and get(bo,coord) != '.':
            return 1
    g['state'] = 'victory'
    return 0

# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.
    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows,num_cols),bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    return dig_nd(game,(row,col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    last_row, bo = game['dimensions'][0] - 1, render_2d_locations(game,xray)
    string = ''
    for ind,row in enumerate(bo):
        for char in row: 
            string += char
        if ind != last_row:
            string += '\n'
    return string


# N-D IMPLEMENTATION
def board(dim,insert):
    """Make a clean board"""
    if len(dim) == 1: 
        return [insert for _ in range(dim[0])]
    return [board(dim[1:],insert) for _ in range(dim[0])]

def get(bo,target,whole = True):
    """
    Get a specific element from board (either game board or
    hidden) if whole is True
    Else, gets the list that the elem is in (use this when
    you want to change that elem)
    """
    x = bo[:]
    for i in range(len(target) -1):
        x = x[target[i]]
    if whole:
        x = x[target[-1]]
    return x 

def shorten(game):
    """Make it easier to name"""
    return (game['dimensions'],game['state'],game['board'],
        game['hidden'],all_coord(game['dimensions']))

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary
    """
    game = board(dimensions,0)
    for bomb in bombs:
        get(game,bomb,False)[bomb[-1]] = '.'
        for neighbor in neighbors(bomb,dimensions):
            if get(game,neighbor) != '.':
                get(game,neighbor,False)[neighbor[-1]] += 1
    return {
        'board': game,
        'dimensions': dimensions,
        'hidden': board(dimensions,True),
        'state': 'ongoing'
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed
    """
    dim,state,bo,hid,coords = shorten(game)
    def recursive(game,coordinates):
        if state != 'ongoing' or not get(hid,coordinates):
            return 0 
        get(hid,coordinates,False)[coordinates[-1]],count = False,1
        current = get(bo,coordinates)
        if current == 0:
            count += sum(recursive(game,c) if get(bo,c) != '.' and get(hid,c)
                else 0 for c in neighbors(coordinates,dim))
        check(game,coords,current)
        return count
    return recursive(game,coordinates)


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)
    """
    element = lambda a,hid: '_' if hid and not xray else ' ' \
        if a == 0 else str(a) if isinstance(a,int) else a
    def deep_copy(b,h):
        return [element(i,j) if not isinstance(i,list) \
            else deep_copy(i,j) for i,j in zip(b,h)]
    return deep_copy(game['board'],game['hidden'])


