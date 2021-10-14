from UCT import UCT

from abc import abstractmethod
from math import log, sqrt
import random

class State:
    def __init__():
        pass

    @abstractmethod
    def is_terminal(self):
        """
        return true if current state is the terminal.
        """
        pass 

    @abstractmethod
    def possible_moves(self):
        """
        Return all possible moves from the current state.
        """
        pass

    @abstractmethod
    def update(self, move):
        """
        Return the new state after a move from the current state.
        """
        pass

    @abstractmethod
    def get_score(self):
        """
        Calculate the score of a terminal state.
        """
        pass

    # @abstractmethod
    # def update_score(self):
    #     pass

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.count = 1
        self.win = 0
        self.untaken_moves = set(state.possible_moves())

    def is_fully_expanded(self):
        return not self.untaken_moves

    def get_best_child(self, c=sqrt(2)):
        return max(self.children,
                key= lambda n: UCT(n.win, n.count, n.parent.count, c))

    def get_new_child(self):
        move = self.untaken_moves.pop()
        state = self.state.update(move)
        child = Node(state, self)
        self.children.append(child)

    def update_score(self, result):
        self.count += 1
        self.win += result[self.state.id]

    def is_terminal(self):
        return self.state.is_terminal()

class MCTS:
    """ Monte Carlo Tree Search
    """
    def __init__(self, state, c=sqrt(2)):
        self.root = Node(state, None)
        self.c = c

    def search(self, node):
        """
        Update Monte Carlo Tree
        """
        # Selction
        while not node.is_terminal():
            if node.is_fully_expanded():
                node = node.get_best_child(self.c)
            else:
                break
        
        # Expansion
        if not node.is_fully_expanded():
            node.get_new_child()

        # Simulation
        result = self.rollout(node)

        # Backpropagation
        self.backpropagate(node, result)

    def train(self, epoch):
        for _ in range(epoch):
            self.search(self.root)

    def rollout(self, node):
        state = node.state
        while not state.is_terminal(): # and state.possible_moves():
            move = random.choice(state.possible_moves())
            state = state.update(move)
        return state.get_score()

    def backpropagate(self, node, result):
        while node:
            node.update_score(result)
            node = node.parent