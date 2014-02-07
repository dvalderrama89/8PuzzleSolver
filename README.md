8PuzzleSolver
=============

Uses A* search and semi-iterative deepening.

astar_puzzle.py
---------------
Run using python astar_puzzle.py < TESTINPUT.txt > SOLUTION.txt
where TESTINPUT is made up of a 3x3 puzzle using 'X' as the blank space

Example
--------
If TESTINPUT.txt = 
2 3 X
1 4 5
7 8 6

Then SOLUTION.txt contains:

lldrrd
0 seconds

Known Issues
------------
Maximum recursion depth exceeded on some inputs due to path extensions.
