#  Nots-and-crosses-on-steroids
A unique variant of ultimate tic tac toe with 2 boards.  This was done by me and my friend Tanmay as a part of our Artificial Intelligence course.

---------------------------------------
*Coded by:*
**Prajwal Krishna** and **Tanmay Kumar Sinha**

## Result

There was a tournament for bots were a total of 72 teams participated and we were lucky to be the winner with 1548 points out of possible 1892 points. Losing 4 out of 22 matches played by us, and each of our loss was when we moved second.

## Strategy
 - We first tried to use min-max tree search with alpha-beta pruning but we were unable to find any good heuristic and were not convinced by the strength of the bot, however, later we found that the people had made decent bots using it.
 - This promoted us to use Monte Carlo Tree Search which was recently used by Google AlphaGo program, then we proceeded to learn and code it.
 - . The Monte Carlo tree search is a tree search algorithm which uses random sampling and play outs to keep track of which states are favorable and may lead to favorable results. It uses random simulations to check whether the next step is favorable or not.
 - The major differences of MCTS with others is that the tree constructed is asymmetric denser in regions which shows greater potential to have optimal move and the  playouts are not optimal as in case of min-max but randomized.
 - A MCTS has four steps which are as follows
	1. **Expansion**  
		In this step we construct the nodes upto a certain depth 'd', till which we want to store and have memory to do so. Here we only expanded upto **depth 3** though we could have done 4 also. Also we sorted the nodes expanded in order of a heuristic that I will give later, and if game if won or lost at any branch I have pruned the branch. It happens only once in a move.
	2. **Selection**
		Selection is 2nd step, which happens in every iteration. Here we recursively select the starting point of our simulations from the expanded nodes. This step is the heart of the MCTS, our selection function is free of all heuristics and uses **Upper Confidence Bound(UCB)** as selection parameter. The main problem here is to strike a balance between expansion of good nodes and exploration of unattended nodes, that is what ucb does. The n variable of selected node is updated.
	3. **Simulation**
	Once a node is selected we need to  start a random simulation from the node, this in pure MCTS would be to select a random move from valid moves for each player and stop only when game ends. However, we used **heavy playouts** for this, that is we used a heuristic same as one used for expansion and give a weighted probability to each move based on the result of heuristic and then randomly select one finally. We played many matches with heavy playouts version and the vanilla version both were winning equally, neither was dominating but the heavy playouts version seemed better against Min-max bots of our friends specially during initial stages so we went with it. There is 3 times boast in number of simulations per move in vanilla simulations.
	4. **Backpropagation**
	Once the game ends, we need to inform the expanded nodes about it, so that we can use that while selection. If there is a loss we don't do anything, but if there is a win we propagate the win to node selected and its parents.
	5. **Finding best move**
	This is the last step we need to do, here we only see level 1 expanded nodes and select the best node amongst them. For this we only see win % from each node and as a tie breaker use the node with more simulations as they have more experience. This step is done only when MCTS is over for a move.

 - The MCTS method is dependent on number of iterations, the more the game simulation better accuracy in the guessing of optimal move, initially the board is quite spare and each game requires many moves to complete so number of games played per move is less, so the moves given by MCTC is not that good. So we had tried to use the heuristic mentioned for ordering the nodes while expansion, this is helpful as initially MCTS can't really distinguish between nodes,
 - **Heuristic** 	
	 - **For small board**
		 - If small board can we won by move - 10 points
		 - Per potential row, column diagonal where we place 2nd peg third being empty - 1 point
		 -  Per potential row, column diagonal where we place 3rd peg other two being enemy's - 1 point
		 - These are additive in nature
	 - **For big board**
		 - If small board is won only then it comes into play.
		 - Big board is won - 100 points
		 - Per potential row, column diagonal where we place 2nd peg third being empty - 10 point
		 - Per potential row, column diagonal where we place 3rd peg other two being enemy's - 10 point
- **Upper confidence bound**
	- Used in selection stage, manages exploration and expansion factors.
	#### **UCB(i)** - {w<sub>i</sub>/n<sub>i</sub>} + C * (ln N<sub>i</sub>)/n<sub>i</sub>
	Where,
	- w<sub>i</sub> = Number of Wins from i<sup>th</sup> node
	- n<sub>i</sub> = Number of simulations from i<sup>th</sup> node
	- N<sub>i</sub> = Number of simulations from parent of i<sup>th</sup> node
	- C = factor of balance of expansion and exploration, set of sqrt(2) generally.
- **Node structure**
	- self.n = Number of simulations from the node
	- self.w = Number of simulations won from the node
	- self.parent = Parent of node
	- self.children = Set of children of the node
	- self.board = Current board position if moves uptil node are made
	- self.heuristic = Heuristic value of the current node

- **Caution**
	- If using python2 remember 1/2 == 0, use float(1/2), we were stuck with this mistake for 2 days cursing the MCTS
## Scope of improvement

- To overcome the problem faced in the initial stages of the game, we can provide our bot with a table of opening moves.
- Using some heuristic in the selection procedure of the MCTS to increase efficiency.
- Optimize code and subroutines like find_valid_moves, find_terminal_state etc.
- Reuse tree, remember and use tree branches previously seen.

## Vote of thanks
 We would like to thank our TA mentors Gunjan mam, Tirth and Anshul sir and Professor Praveen Paruchuri for giving us this opportunity and interesting assignment,
