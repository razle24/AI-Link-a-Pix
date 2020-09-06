# AI-Link-a-Pix

![](images/board_5.png =250x250)

This is an AI solver for the Link-a-Pix game. 

First, sit back and enjoy a nice game of Link-a-Pix :

https://www.conceptispuzzles.com/index.aspx?uri=puzzle/link-a-pix

## What is Link-a-Pix?

A board game puzzle that form whimsical pixel-art pictures when solved. Each puzzle consists of a grid containing numbers in various places.
Every number, except for the 1’s, is half of a pair.The purpose is to reveal a hidden picture by linking the pairs and painting the paths 
so that the number of squares in the path, including the squares at the ends, equals the value of the numbers being linked together. 


## Solutions 

The solution of the game is finding a series of legal paths under the constraints in order to get the final picture (each board has a unique solution)

We decided to use multiple solutions in order to solve our problem : 

1. CSP backtrack algorithm
2. Search algorithms : DFS, BFS, UCS and A*
3. Machine learning algorithm 

### Variable Selection
We managed to solve the small boards (up to 10x15) with no variable selection. 

In order to solve bigger boards, we needed to add ways to go over the numbered cells on the board – Variable selection : 

1. Top to Bottom - the basic order -  goes over the numbered cells by their positions on the board, from top to bottom and from left to right. 
2. MRV - Most Remaining Value - Orders the cells by their possible paths – descending order. 
3. LCV – Least Constrained Value - Orders the cells by their possible paths – ascending order.
4. Small to Big - Orders the cells by their number – ascending order. 
5. By Bullet - Divide the board into 9 bullets. And order the cells by the bullets (first bullet’s cells first and so on…) 
6. By color - Orders the cells by their color (RGB color numbers)
7. Random selection - Orders the cells randomly.

### Heuristics
1. Null Heuristic - Return 0 for every board and path. 
2. Stick to walls - Counts the number of cells in the path that “stick to the walls” of the board. Gives a higher score for paths closer to the walls.
3. Stick to other paths - Counts the number of cells in the path that “stick to other paths” on the board. Gives a higher score for paths closer to other paths – avoiding holes in the picture.
4. Count possible paths - Returns the maximum between the possible paths from the starting point of the path, and the possible paths from the ending point of the path. 
5. Linear combination - Returns a linear combination of all the heuristics above. 

## How to run the code?

1. Make sure you use Python 3. 
2. Make sure you hava all the required packages (look in the requirements.txt file for more info) 
            Download all packages using the command : "pip install <package>"
            
3. In your terminal go to the project's directory and run : "python3 gui.py". 
4. The GUI will appear and you can choose one of the boards in the boards directory, and enjoy the game! 








