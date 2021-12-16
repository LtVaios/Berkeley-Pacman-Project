# Berkeley Pacman Project
 ➡️ Official project website and documentation about it: http://ai.berkeley.edu/project_overview.html) <br />  
 ➡️ I used various algorithms explained below to make a pacman eat all the dots (project 1) by itself and also made more complex algorithms to make it play and win the game by itself ghosts included (project 2). These files also include a real pacman game version you can play in your terminal. The graphics and the game files needed to play the actual game are not implemented by me, I only implemented the AI algorithms. You can find more info about the project in the link above.<br /><br />
:pencil2: Inside each .zip you will also find some of mine documentation (in Greek) on how the functions work but there are also a lot of code comments.

## Installation / run

### 🏁 Project-1
Download the .zip file and extract locally. Then open the code as project in an IDE and you can run these commands on the terminal while being in the folder /search:
<br /><br />
:small_blue_diamond: DFS (Depth-first-search) Algorithm:
```
  $ python pacman.py -l tinyMaze -p SearchAgent
  $ python pacman.py -l mediumMaze -p SearchAgent
  $ python pacman.py -l bigMaze -z .5 -p SearchAgent
```
:small_blue_diamond: BFS (Breadth-first-search) Algorithm:
```
  $ python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
  $ python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```
:small_blue_diamond: Solving the eightpuzzle which puts all numbers of a box in order, using BFS:
```
  $ python eightpuzzle.py
```
:small_blue_diamond: Implemented Uniform-Cost-Search function:
```
  $ python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
  $ python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
  $ python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```
:small_blue_diamond: A* (A star) graph search Algorithm:
```
  $ python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```
:small_blue_diamond: Data decoding of the corners problem and run with BFS:
```
  $ python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
  $ python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```
:small_blue_diamond: Using A* to solve the corners problem but with a new heuristic implemented by me:
```
  $ python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```
:small_blue_diamond: Using A* to solve the corners problem:
```
  $ python pacman.py -l testSearch -p AStarFoodSearchAgent
```
:small_blue_diamond: Upgrade A* to make the pacman eat all the dots:
```
  $ python pacman.py -l trickySearch -p AStarFoodSearchAgent
```
:small_blue_diamond: Implementing a greedy algorithm that always eats the closest dot and it is the most efficient one for this problem.
```
  $ python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 
 ```
 
### :ghost: Project-2
Download the .zip file and extract locally. Then open the code as project in an IDE and you can run these commands on the terminal while being in the folder /multiagents: <br /> <br />
:small_blue_diamond: Reflex Agent:
```
  $ python pacman.py --frameTime 0 -p ReflexAgent -k 1
  $ python pacman.py --frameTime 0 -p ReflexAgent -k 2
  $ python autograder.py -q q1
```
:small_blue_diamond: Minimax algorithm:
```
  $ python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
  $ python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
  $ python autograder.py -q q2
```
:small_blue_diamond: Alpha-Beta pruning algorithm:
```
  $ python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
  $ python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
  $ python autograder.py -q q3
```
:small_blue_diamond: Expectimax algorithm:
```
  $ python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
  $ python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
  $ python autograder.py -q q4
```
:small_blue_diamond: Evaluation Function:
```
  $ python autograder.py -q q5
```

### :video_game: Play a game of pacman
```
  $ python pacman.py
```

## Built With
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png" alt="MarineGEO circle logo" style="height: 100px; width:100px;"/>


