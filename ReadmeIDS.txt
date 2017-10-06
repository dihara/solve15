Description
-----------

This program is based on the pseudocode for IDS search in AIAMA. It receives a 15 puzzle as input and tries to solve it
by using IDS. After exploring to a certain depth, it prints the elapsed time and how much memory was used by nodes
created at that level. This is done by calculating the memory usage of one state and counting the number of states created
for each depth of IDS.

Usage
-----
To run the program
    python solve15ids.py
    
You will be prompted to introduce the puzzle that must be solved. This should be done by writing the numbers in the puzzle
starting on the first column of row one. Every number must be separated by a space. The BLANK is represented by an asterisk.

So, if the puzzle is something like:

1   2  3  4
5   6  7  8
9  10 11 12
13 14  * 15

You would input:

1 2 3 4 5 6 7 8 9 10 11 12 13 14 * 15

when prompted.

If a different size of puzzle must be solved, you can change the PUZZLE_SIZE variable in puzzle_utils,
this takes the size of one side of the puzzle, so for a 15 puzzle (16 squares or 4 by 4) it is set to 4.