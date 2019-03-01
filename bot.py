from copy import deepcopy
import random
from math import sqrt, log
from time import time

C = sqrt(2)
INF = 100000000000

class Node:
    def __init__(self, parent, board, old_move, flag, heuristic):
        # Number of visits
        self.n = 0
        # Number of wins from that state
        self.w = 0
        self.children = []
        self.parent = parent
        self.board = board
        self.flag = flag
        self.old_move = old_move
        self.heuristic = heuristic

    def ucb(self, N, cooperative):
        '''If cooperative then maximize ucb'''
        if cooperative:
            return INF if not self.n else self.w/self.n + C * sqrt(log(N)/self.n)
        return INF if not self.n else 1 - self.w/self.n + C * sqrt(log(N)/self.n)

    def selection(self, player):
        if not len(self.children):
            return self
        self.n += 1
        good_child = None
        max_ucb = -1
        for child in self.children:
            if child.ucb(self.n, player==self.flag) > max_ucb:
                max_ucb = child.ucb(self.n, player==self.flag)
                good_child = child
        return good_child.selection(player)

    def expansion(self, player):
        valid_moves = self.board.find_valid_move_cells(self.old_move)
        random.shuffle(valid_moves)
        for action in valid_moves:
            h = small_heuristic(self.board, action, self.flag)
            transition_board = deepcopy(self.board)
            _, bonus = transition_board.update(self.old_move, action, self.flag)
            ch = self.flag if bonus else ('x' if self.flag == 'o' else 'o')
            self.children.append(Node(self, transition_board, action, ch, h))
        self.children.sort(key = lambda x: x.heuristic, reverse = True)

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
            if child.n and child.w/child.n > max[0]:
                max[0] = child.w/child.n
                max[1] = child.n
                best_child = child
            elif child.n and child.w/child.n == max[0] and child.n > max[1]:
                max[1] = child.n
                best_child = child
        return best_child if not best_child else best_child.old_move

class Bot:
    def __init__(self):
        self.player = None
        pass

    def move(self, board, old_move, flag):
        '''
        All index are zero based
        old_move : Returns a 3 tuple (board, row, column)
        '''
        # Make a copy of current state
        curr_state = deepcopy(board)
        startTime = time()

        if not self.player:
            self.player = flag

        # Find all valid moves for current board state
        valid_moves = board.find_valid_move_cells(old_move)

        # Store random move if needed
        best_move = valid_moves[random.randrange(len(valid_moves))]


        root = Node(None, curr_state, old_move, self.player, 0)

        # Expand till desired depth
        root.expansion(self.player)
        for child in root.children:
            child.expansion(self.player)
            if len(child.children) > 32:
                continue
            for grandChild in child.children:
                grandChild.expansion(self.player)

        # Simulate for iter times
        iter = 100000
        for i in range(iter):
            if time() - startTime > 5:
                print "iter" + str(i)
                break
            leaf = root.selection(self.player)
            status = leaf.simulation()
            if self.player == status[0]:
                leaf.backpropagation(1)
            else:
                leaf.backpropagation(0)

        result = root.best_move()
        if result:
            best_move = result

        print time() - startTime
        return best_move

def simulator(board, old_move, flag):
    while(1):
        valid_moves = board.find_valid_move_cells(old_move)

        sum = 0
        h = []
        for action in valid_moves:
            x = small_heuristic(board, action, flag)
            h.append(x)
            sum += x
        rand = random.randrange(sum)
        count = 0
        action = None
        for i in range(len(h)):
            count += h[i]
            if count >= rand:
                action = valid_moves[i]
                break

        # action = valid_moves[random.randrange(len(valid_moves))]
        _, bonus = board.update(old_move, action, flag)
        status = board.find_terminal_state()

        if not status[1]=='-':
            return status

        flag = flag if bonus else ('x' if flag == 'o' else 'o')
        old_move = action

def small_heuristic(board, action , flag):
    ''' Check for best small board'''
    index = (action[0], 3 * (action[1]//3), 3 * (action[2]//3))
    small_board = [['-' for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            small_board[i][j] = board.big_boards_status[index[0]][i + index[1]][j + index[2]]
    local_action = (action[1]%3, action[2]%3)
    enemy = 'x' if flag == 'o' else 'o'
    value = 10

    # Check in row
    if small_board[local_action[0]][(local_action[1] + 1) % 3] == flag:
        if small_board[local_action[0]][(local_action[1] - 1) % 3] == flag:
            return 100 * big_heuristic(board, action, flag)
        elif small_board[local_action[0]][(local_action[1] - 1) % 3] == '-':
            value += 20
    if small_board[local_action[0]][(local_action[1] - 1) % 3] == flag:
        if small_board[local_action[0]][(local_action[1] + 1) % 3] == '-':
            value += 20
    if small_board[local_action[0]][(local_action[1] - 1) % 3]==small_board[local_action[0]][(local_action[1] + 1) % 3]==enemy:
        value += 20

    # Check in column
    if small_board[(local_action[0] + 1) % 3][local_action[1]] == flag:
        if small_board[(local_action[0] - 1) % 3][local_action[1]] == flag:
            return 100 * big_heuristic(board, action, flag)
        elif small_board[(local_action[0] - 1) % 3][local_action[1]] == '-':
            value += 20
    if small_board[(local_action[0] - 1) % 3][local_action[1]] == flag:
        if small_board[(local_action[0] + 1) % 3][local_action[1]] == '-':
            value += 20
    if small_board[(local_action[0] - 1) % 3][local_action[1]]==small_board[(local_action[0] + 1) % 3][local_action[1]]==enemy:
        value += 20

    # Check priciple diagonal
    if local_action[0]==local_action[1]:
        if small_board[(local_action[0] + 1) % 3][(local_action[1] + 1) % 3] == flag:
            if small_board[(local_action[0] - 1) % 3][(local_action[1] - 1) % 3] == flag:
                return 100 * big_heuristic(board, action, flag)
            elif small_board[(local_action[0] - 1) % 3][(local_action[1] - 1) % 3] == '-':
                value += 20
        if small_board[(local_action[0] - 1) % 3][(local_action[1] - 1) % 3] == flag:
            if small_board[(local_action[0] + 1) % 3][(local_action[1] + 1) % 3] == '-':
                value += 20
        if small_board[(local_action[0] - 1) % 3][(local_action[1] - 1) % 3]==small_board[(local_action[0] + 1) % 3][(local_action[1] + 1) % 3]==enemy:
            value += 20
    # Check other diagonal
    if local_action[0]+local_action[1]==2:
        if small_board[(local_action[0] + 1) % 3][(local_action[1] - 1) % 3] == flag:
            if small_board[(local_action[0] - 1) % 3][(local_action[1] + 1) % 3] == flag:
                return 100 * big_heuristic(board, action, flag)
            elif small_board[(local_action[0] - 1) % 3][(local_action[1] + 1) % 3] == '-':
                value += 20
        if small_board[(local_action[0] - 1) % 3][(local_action[1] + 1) % 3] == flag:
            if small_board[(local_action[0] + 1) % 3][(local_action[1] - 1) % 3] == '-':
                value += 20
        if small_board[(local_action[0] - 1) % 3][(local_action[1] + 1) % 3]==small_board[(local_action[0] + 1) % 3][(local_action[1] - 1) % 3]==enemy:
            value += 20

    return value

def big_heuristic(board, action , flag):
    ''' Check for best big board'''
    local_board = ( action[1]//3, action[2]//3 )
    big_board = board.small_boards_status[action[0]]
    enemy = 'x' if flag == 'o' else 'o'
    value = 1
    # Check in row
    if big_board[local_board[0]][(local_board[1] + 1) % 3] == flag:
        if big_board[local_board[0]][(local_board[1] - 1) % 3] == flag:
            return 10
        elif big_board[local_board[0]][(local_board[1] - 1) % 3] == '-':
            value += 2
    if big_board[local_board[0]][(local_board[1] - 1) % 3] == flag:
        if big_board[local_board[0]][(local_board[1] + 1) % 3] == '-':
            value += 2
    if big_board[local_board[0]][(local_board[1] - 1) % 3]==big_board[local_board[0]][(local_board[1] + 1) % 3]==enemy:
        value += 2

    # Check in column
    if big_board[(local_board[0] + 1) % 3][local_board[1]] == flag:
        if big_board[(local_board[0] - 1) % 3][local_board[1]] == flag:
            return 10
        elif big_board[(local_board[0] - 1) % 3][local_board[1]] == '-':
            value += 2
    if big_board[(local_board[0] - 1) % 3][local_board[1]] == flag:
        if big_board[(local_board[0] + 1) % 3][local_board[1]] == '-':
            value += 2
    if big_board[(local_board[0] - 1) % 3][local_board[1]]==big_board[(local_board[0] + 1) % 3][local_board[1]]==enemy:
        value += 2

    # Check priciple diagonal
    if local_board[0]==local_board[1]:
        if big_board[(local_board[0] + 1) % 3][(local_board[1] + 1) % 3] == flag:
            if big_board[(local_board[0] - 1) % 3][(local_board[1] - 1) % 3] == flag:
                return 10
            elif big_board[(local_board[0] - 1) % 3][(local_board[1] - 1) % 3] == '-':
                value += 2
        if big_board[(local_board[0] - 1) % 3][(local_board[1] - 1) % 3] == flag:
            if big_board[(local_board[0] + 1) % 3][(local_board[1] + 1) % 3] == '-':
                value += 2
        if big_board[(local_board[0] - 1) % 3][(local_board[1] - 1) % 3]==big_board[(local_board[0] + 1) % 3][(local_board[1] + 1) % 3]==enemy:
            value += 2

    # Check other diagonal
    if local_board[0]+local_board[1]==2:
        if big_board[(local_board[0] + 1) % 3][(local_board[1] - 1) % 3] == flag:
            if big_board[(local_board[0] - 1) % 3][(local_board[1] + 1) % 3] == flag:
                return 10
            elif big_board[(local_board[0] - 1) % 3][(local_board[1] + 1) % 3] == '-':
                value += 2
        if big_board[(local_board[0] - 1) % 3][(local_board[1] + 1) % 3] == flag:
            if big_board[(local_board[0] + 1) % 3][(local_board[1] - 1) % 3] == '-':
                value += 2
        if big_board[(local_board[0] - 1) % 3][(local_board[1] + 1) % 3]==big_board[(local_board[0] + 1) % 3][(local_board[1] - 1) % 3]==enemy:
            value += 2

    return value
    # print '==============BigBoard Overview =============='
    # print local_board
    # print flag
    # for i in range(3):
    #     for j in range(3):
    #         print big_board[i][j],
    #     print '\n'
    # print value
    # print '=============================================='
