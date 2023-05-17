
import sys
import time

sys.setrecursionlimit(10_000)


bool_list = [True,False]

def new_formula(formula,curr_var,curr_bool):
    """
    Remove any lines that will always be true
    given the variables 
    """
    # Sort shortest to longest (one-chains, then ...)
    new = []
    for section in formula:
        insert, add = [],True
        for var,boo in section:
            if var != curr_var:
                insert.append((var,boo))
            elif not boo ^ curr_bool:
                add = False
                break
        if add:
            new.append(insert)
    return new

def recurse(formula,var,boolean):
    """
    Recursion: into the satisfying assignment 
    """
    new_form = new_formula(formula,var,boolean)
    dict1 = satisfying_assignment(new_form)
    if dict1 is not None:
        dict1[var] = boolean
        return dict1
    return None

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    """
    if len(formula) == 0:
        return {}
    formula.sort(key = len)
    if not formula[0]:
        return None
    curr_var = formula[0][0][0]
    for boo in bool_list:
        result = recurse(formula,curr_var,boo)
        if result is not None: return result
    return None

def cnf(l1):
    """
    Returns cnf literals that say:
    1) At least one of them have to be true
    2) Only one of them can be True
    """
    return [[((coord),True) for coord in l1]] + [[(l1[c1],False),(l1[c2],False)]
         for c1 in range(len(l1)) for c2 in range(c1+1,len(l1))]
    
def helper(dimension):
    """
    All the CNFs for cell constriction, row constriction,
    and column constriction (but not subgrid)
    """
    answer = []
    for r in range(dimension):
        for c in range(dimension):
            answer += cnf([(r,c,val) for val in range(1,dimension+1)])
        for val in range(1,dimension+1):
            answer += cnf([(r,c,val) for c in range(dimension)])
            answer += cnf([(c,r,val) for c in range(dimension)])
    return answer,dimension

def subgrid(dimension,square):
    """
    Subgrid CNFs, going through each subgrid
    """
    answer = []
    for val in range(1,dimension+1):
        for r in range(0,dimension,square):
            for c in range(0,dimension,square):
                answer += cnf([(s_r,s_c,val) for s_r in 
                    range(r,r+square) for s_c in range(c,c+square)])
    return answer

def already_there(sudoku_board,dimension):
    """
    Set requirements for the numbers already set
    """
    return [[((r,c,sudoku_board[r][c]),True)] for r in range(dimension)
        for c in range(dimension) if sudoku_board[r][c]]


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    answer,dimension = helper(len(sudoku_board))
    answer.extend(subgrid(dimension,int(dimension ** 0.5)))
    answer.extend(already_there(sudoku_board,dimension))
    return answer


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolveable board, return None
    instead.
    """
    if assignments is None: return assignments
    board = [[0]*n for _ in range(n)]
    for (r,c,val),boo in assignments.items():
        if boo:
            board[r][c] = val
    return board


def valid(board,row,col):
    ro = [val for val in board[row] if val != 0]
    co = [board[r][col] for r in range(len(board)) if board[r][col] != 0]
    square = int(len(board)**(0.5))
    sr, sc = (row//square)*square, (col//square)*square
    subg = [board[r][c] for r in range(sr,sr+square) for c in range(sc,sc+square) if board[r][c] != 0]
    cant = set(ro) | set(co) | set(subg)
    return [val for val in range(1,len(board)+1) if val not in cant]
      
def solver(sudoku_board):
    dimension = len(sudoku_board)
    for row in range(dimension):
        for col in range(dimension):
            if sudoku_board[row][col] != 0:
                continue
            for trial in valid(sudoku_board,row,col):
                sudoku_board[row][col] = trial
                result = solver(sudoku_board)
                if result is not None:
                    return result
            sudoku_board[row][col] = 0
            return None
    return sudoku_board   

if __name__ == '__main__':
    board = [
        [0,8,0,0,0,6,2,0,0],
        [5,0,0,8,7,0,3,0,0],
        [0,0,0,0,0,4,0,7,0],
        [0,4,0,2,1,0,0,3,0],
        [0,0,9,0,0,0,5,0,0],
        [0,0,0,0,0,7,0,0,0],
        [0,0,0,6,0,0,0,0,0],
        [0,2,0,3,8,0,0,1,0],
        [4,0,0,0,0,0,0,0,2]
    ]
    t0 = time.time()
    two_cnf = sudoku_board_to_sat_formula(board)
    solved = satisfying_assignment(two_cnf)
    new_board = assignments_to_sudoku_board(solved,len(board))
    print(*new_board,sep="\n")
    t1 = time.time()
    print("\n")
    print(*solver(board),sep="\n")
    t2 = time.time()
    print("\n")
    print(t1-t0)
    print(t2-t1)
