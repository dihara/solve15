import mem

#here PUZZLE_SIZE is the number of columns or rows in the puzzle (i.e. for 15 puzzle PUZZLE_SIZE = 16)
PUZZLE_SIZE = 4
BLANK_SQUARE = "*"

#This linked list is to know which MOVES I made to reach each state (in the frontier or the visited nodes list)
class Puzzle_node:
    def __init__(self,state):
        self.state = state
        self.move = ""
        self.previous = None

    def getState(self):
        return self.state

    def getPrevious(self):
        return self.previous
        
    def getMove(self):
        return self.move

    def setState(self,newstate):
        self.state = newstate

    def setPrevious(self,newprevious):
        self.previous = newprevious
        
    def setMove(self, newmove):
        self.move = newmove

#function that parses the input and returns the first puzzle node
def parse_to_puzzle(s):
    w, h = PUZZLE_SIZE, PUZZLE_SIZE;
    i = 0
    matrix = [[0 for x in range(w)] for y in range(h)] 

    elements = s.split(' ')
    if len(elements) != (PUZZLE_SIZE ** 2):
        raise ValueError("you must input", PUZZLE_SIZE ** 2, " elements")
    else:
        for r in elements:
            col = i - PUZZLE_SIZE * (i//PUZZLE_SIZE)
            row = i//PUZZLE_SIZE
            matrix[row][col] = r
            i = i + 1
     
    if not valid_puzzle(matrix):
        raise ValueError("The values you entered are not valid")
        matrix = []
           
    return Puzzle_node(matrix)
    
#check if the puzzle consists of valid elements, i.e. there is not a 99 number in a 15 puzzle    
def valid_puzzle(m):
    is_valid = True
    for row in m:
        for cell in row:
            is_valid = is_valid and ((cell == BLANK_SQUARE) or ((0 < int(cell)) and (int(cell) < (PUZZLE_SIZE ** 2))))
    return is_valid
    
#return true if the puzzle is solved
def solved_puzzle(puzzle):
    i = 0
    is_solved = True
    puzzle_matrix = puzzle.getState()
    while i < (PUZZLE_SIZE * PUZZLE_SIZE):
        col = int(i - PUZZLE_SIZE * (i // PUZZLE_SIZE))
        row = int(i // PUZZLE_SIZE)
        if (i < (PUZZLE_SIZE * PUZZLE_SIZE - 1)):
            is_solved = is_solved and (puzzle_matrix[row][col] == str(i + 1))
        else:
            is_solved = is_solved and (puzzle_matrix[row][col] == BLANK_SQUARE)

        i = i + 1
                
    return is_solved
    
#output a matrix representation of the node to the screen
def print_puzzle(s):
    i = 0
    c = 0
    r = 0
    while i < (PUZZLE_SIZE * PUZZLE_SIZE):
        c = int(i - PUZZLE_SIZE * (i // PUZZLE_SIZE))
        r = int(i // PUZZLE_SIZE)
        print(s.getState()[r][c].ljust(2), end=" ")
        if ((i + 1) % PUZZLE_SIZE) == 0:
            print("")
            
        i = i + 1
        
#make a copy of bidimentional list, returns a duplicate puzzle state      
def copy_puzzle(puzzle):
    duplicate = puzzle.copy()
    for i in range(PUZZLE_SIZE):
        duplicate[i] = puzzle[i].copy()
        
    return duplicate        
        
#attemps to move the blank square to the right, up, down or left,
#and return a new puzzle state in which the action has been done.
#If the action cannot be done (i.e. move blank to the right when
#it is already on the rightmost column) return nothing
def move_on_puzzle(puzzle, action):
    #find where is the "BLANK_SQUARE"
    puzzle_array = puzzle.getState()
    i = 0
    found = False
    while not found:
        r = int(i // PUZZLE_SIZE)
        c = int(i - PUZZLE_SIZE * (i // PUZZLE_SIZE))
        if puzzle_array[r][c]==BLANK_SQUARE:
            found=True
        else:
            i += 1

    #print("I found * at ", "x:", r, "y:", c, "see?", puzzle_array[r][c])
    #now c and r point to where the "BLANK_SQUARE" is
    
    new_state = []
    if (action == "up"):
        if (0 < r):
            #print("I can do UP")
            new_state = copy_puzzle(puzzle_array)
            new_state[r][c] = new_state[r - 1][c]
            new_state[r - 1][c] = BLANK_SQUARE
    elif action == "down":
        if (r < (PUZZLE_SIZE - 1)):
            #print("I can do DOWN")
            new_state = copy_puzzle(puzzle_array)
            new_state[r][c] = new_state[r + 1][c]
            new_state[r + 1][c] = BLANK_SQUARE
    elif action == "left":
        if (0 < c):
            #print("I can do LEFT")
            new_state = copy_puzzle(puzzle_array)
            new_state[r][c] = new_state[r][c - 1]
            new_state[r][c - 1] = BLANK_SQUARE
    elif action == "right":
        if (c < (PUZZLE_SIZE - 1)):
            #print("I can do RIGHT")
            new_state = copy_puzzle(puzzle_array)
            new_state[r][c] = new_state[r][c + 1]
            new_state[r][c + 1] = BLANK_SQUARE        
    else:
        raise ValueError("Internal error: invalid move")

    return Puzzle_node(new_state)
        
#expand node (try all possible moves), returns a list of child nodes
def get_children(node):
    child_list = []
    #print(len(child_list))
    #check for left
    c = move_on_puzzle(node, "up")
    if len(c.getState()) > 0:
        c.setMove("u")
        c.setPrevious(node)
        child_list.append(c)
        #print("after up", c)
    c = move_on_puzzle(node, "right")
    if len(c.getState()) > 0:
        c.setMove("r")
        c.setPrevious(node)
        child_list.append(c)
        #print("after right", c)
    c = move_on_puzzle(node, "down")
    if len(c.getState()) > 0:
        c.setMove("d")
        c.setPrevious(node)
        child_list.append(c)
        #print("after down", c)
    c = move_on_puzzle(node, "left")
    if len(c.getState()) > 0:
        c.setMove("l")
        c.setPrevious(node)
        child_list.append(c)
        #print("after left", c)
    return child_list
    
#compares two states, return true if they are the same
#as i.e. they have the same numbers at the same positions
def compare_puzzles(puzzle_a, puzzle_b):
    result = True
    for r in range(PUZZLE_SIZE):
        for c in range(PUZZLE_SIZE):
            #print("r and c are:", r, c)
            #print("i am comparing", puzzle_a[r][c], "and", puzzle_b[r][c])
            if str(puzzle_a[r][c]) != str(puzzle_b[r][c]):
                #print("not same")
                result = False
                break;
            #else:
                #print("same")
        
        if result == False:
            break;
                
    #print("and the result is", result)
    return result
    
#search for one node in the frontier and explored nodes lists
#return true if an equal state already exists
def have_i_seen_this_already(node, frontier, explored):
    result = False;
    #print("gonna look in frontier")
    for i in range(len(frontier)):
        #print("the range is", len(frontier))
        #print("i is", i)
        #print("frontier", frontier[i])
        if compare_puzzles(frontier[i].getState(), node.getState()):
            #print("finished comparing frontier")
            result = True
            break
            
    #print("gonna look in explored") 
    if result == False:
        for i in range(len(explored)):
            #print("the range is", len(explored))
            #print("i is", i)
            #print("explored", explored[i].getState())
            #print("about to compare explored")
            if compare_puzzles(explored[i].getState(), node.getState()):
                #print("finished comparing explored")
                result = True
                break
    
    return result
    
#print the solution as a sequence of "moves" and prints
#all states up to the solution
def print_complete_solution(first_node, solution_stack):
    print("So, the game begins with:")
    print_puzzle(first_node)
    next_move = first_node
    for step in reversed(solution_stack):
        if step == 'r':
            next_move = move_on_puzzle(next_move, "right")
            print("Move BLANK RIGHT to get")
            print_puzzle(next_move)
        elif step == 'd':
            next_move = move_on_puzzle(next_move, "down")
            print("Move the BLANK DOWN to get")
            print_puzzle(next_move)            
        elif step == 'l':
            next_move = move_on_puzzle(next_move, "left")
            print("Move the BLANK LEFT to get")
            print_puzzle(next_move)            
        elif step == 'u':
            next_move = move_on_puzzle(next_move, "up")
            print("Move the BLANK UP to get")
            print_puzzle(next_move)
    print("SOLVED!")
    
    
#Perform Depth Limited Search
def DLS(node, depth):
    if (depth == 0) and solved_puzzle(node):
        return node
        
    if (depth > 0):
        children = get_children(node)
        #memory tracking for each children created
        mem.global_memory_usage = mem.global_memory_usage + len(children) * mem.puzzle_mem
        for child in children:
            found = DLS(child, depth - 1)
            if (found != None):
                return found
                
    return None