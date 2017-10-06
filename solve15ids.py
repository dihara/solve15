from puzzle_utils import *
import time
import sys

try:
    #initialize
    frontier = []
    explored = []
    solution_found = None
    
    #receive input and parse
    x = input("Enter puzzle: ")
    puzzle_node = parse_to_puzzle(x)
    mem.puzzle_mem = sys.getsizeof(puzzle_node)
    print("The memory usage of one node is:",mem.puzzle_mem, "bytes")
    first_node = puzzle_node;

    #if the input is valid
    if len(puzzle_node.getState()) > 0:
        print("This is what you want me to solve:")
        print_puzzle(puzzle_node)
    
        #check if input is already solved, if not let it be the initial frontier
        if solved_puzzle(puzzle_node):
            raise ValueError("Too easy, this Puzzle is already solved")
        else:
            frontier.append(puzzle_node)

        start_time = time.time()

        #Do iterative deepening depth-first search            
        depth = 0
        while solution_found == None:
            solution_found = DLS(puzzle_node, depth)
            elapsed_time = time.time() - start_time
            print("Searched up to depth", depth, "now at %.1f seconds" % elapsed_time)
            print("Used", mem.global_memory_usage, "bytes to work up to depth", depth)
            depth = depth + 1
            global_memory_usage = 0
        
        #If we found the solution, print the instructions on how to solve
        if solution_found != None:
            print("Solution found!")
            #Print the solution, etc
            solution_stack=[]
            while True:
                solution_stack.append(solution_found.getMove())
                solution_found = solution_found.getPrevious()
                if solution_found.getPrevious() == None:
                    break;
                
            print_complete_solution(first_node, solution_stack)            
        
except ValueError as valerr:
    print(valerr)