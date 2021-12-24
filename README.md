# Sudoku Solver
## About
This program was made in Python 3 using pygame and numpy arrays. The program uses backtracking algorithm to solve the sudoku board. There are two versions, game_animated.py shows each step of solving the board because of which it uses a iterative algorithm. Whereas game.py does not show each step and uses a recursive algorithm.

## How To Use
Press S to save the current board and L to load the pre-loaded sample game or to load the last saved game, modify samples.txt such that the last saved game is the only/first gameboard in the samples.txt file. The user can choose to solve the board by selecting the numbers on the sidebar, and filling the board by clicking the desired box or the user can press A and wait for the computer to solve the board. This program only works if the sudoku board has atleast one solution.

## Demo
Below is a gif demonstrating the program solving the pre-loaded game. This gif has been sped up by 20 times. The program took approximately 18 minutes to solve the given board below whereas the recursive version where each step is not show took approximately 20 seconds.

![Demo](media/demo.gif)