from copy import deepcopy
import random
from math import sqrt, log

C = sqrt(2)
INF = 100000000000

class Node:
    def __init__(self, parent, board, old_move, flag):
        # Number of visits
        self.n = 0
        # Number of wins from that state
        self.w = 0
        self.children = []
        self.parent = parent
        self.board = board
        self.flag = flag
        self.old_move = old_move

    def ucb(self, N):
        return INF if self.n==0 else self.w/self.n + C * sqrt(log(N)/self.n)

    def selection(self):
        if not len(self.children):
            return self
        self.n += 1
        good_child = None
        max_ucb = -1
        for child in self.children:
            if child.ucb(self.n) > max_ucb:
                max_ucb = child.ucb(self.n)
                good_child = child
        return good_child.selection()

    def expansion(self):
        valid_moves = self.board.find_valid_move_cells(self.old_move)
        for action in valid_moves:
            transition_board = deepcopy(self.board)
            _, bonus = transition_board.update(self.old_move, action, self.flag)
            ch = self.flag if bonus else ('x' if self.flag == 'o' else 'o')
            self.children.append(Node(self, transition_board, action, ch))

    def simulation(self):
        board = deepcopy(self.board)
        return simulator(board, self.old_move, self.flag)

    def backpropagation(self, result):
        parent = self.parent
        self.w += result
        while parent:
            parent.w += result
            parent = parent.parent

    def best_move(self):
        max = [-1 , 0]
        best_child = None
        for child in self.children:
            if child.w/child.n > max[0]:
                max[0] = child.w/child.n
                max[1] = child.n
                best_child = child
            elif child.w/child.n == max[0] and child.n > max[1]:
                max[1] = child.n
                best_child = child
        return best_child.old_move

class Bot:
    def __init__(self):
        self.flag = None
        pass

    def move(self, board, old_move, flag):
        '''
        All index are zero based
        old_move : Returns a 3 tuple (board, row, column)
        '''
        # Make a copy of current state
        curr_state = deepcopy(board)

        if not self.flag:
            self.flag = flag

        # Find all valid moves for current board state
        valid_moves = board.find_valid_move_cells(old_move)

        # Store random move if needed
        best_move = valid_moves[random.randrange(len(valid_moves))]


        root = Node(None, curr_state, old_move, flag)

        # Expand till desired depth
        root.expansion()
        for child in root.children:
            child.expansion()

        # Simulate for iter times
        iter = 100
        for i in range(iter):
            leaf = root.selection()
            status = leaf.simulation()
            if self.flag == status[0]:
                leaf.backpropagation(1)
            else:
                leaf.backpropagation(0)

        best_move = root.best_move()
        return best_move

def simulator(board, old_move, flag):
    while(1):
        valid_moves = board.find_valid_move_cells(old_move)
        action = valid_moves[random.randrange(len(valid_moves))]
        _, bonus = board.update(old_move, action, flag)
        status = board.find_terminal_state()

        if not status[1]=='-':
            return status

        flag = flag if bonus else ('x' if flag == 'o' else 'o')
        old_move = action
