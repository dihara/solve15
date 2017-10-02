from puzzle_utils import *
import time

try:
    #initialize
    frontier = []
    explored = []
    solution_found = False
    
    #receive input and parse
    x = input("Enter puzzle: ")
    puzzle_node = parse_to_puzzle(x)
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
        print("I am starting now at time 0")
            
        #search while we haven't found a solution
        while not solution_found:
            #if we run out of elements in the frontier (we have exhausted the search), there is no solution
            if len(frontier)==0:
                raise ValueError("I have not failed, i've just found 10,000 ways that won't work (actually, I quit)")
            
            #get the shallowest element in the frontier, add it to explored list and expand
            puzzle_node = frontier.pop(0)
            explored.append(puzzle_node) 
            children = get_children(puzzle_node)
            
            for child in children:
                #check for duplicate states (already in visited or frontier)
                if not have_i_seen_this_already(child, frontier, explored):
                    #pointer to parent node, this is to print the final solution if there is any
                    child.setPrevious(puzzle_node)
                    #if the child is not the solution, add that to the frontier
                    if solved_puzzle(child):
                        solution_found = True
                        break
                    else:
                        frontier.append(child)
            
            print("The frontier now has", len(frontier), "states, and the visited nodes list has", len(explored), "states")
            elapsed_time = time.time() - start_time
            print("Still working, now at %.1f seconds" % elapsed_time)

        #if a solution was found, build the list of moves (solution_stack) and
        #print the solution as the sequence of moves from the beggining to the end
        if solution_found:
            solution_stack=[]
            while True:
                solution_stack.append(child.getMove())
                child = child.getPrevious()
                if child.getPrevious() == None:
                    break;
                    
            print_complete_solution(first_node, solution_stack)
                
except ValueError as valerr:
    print(valerr)