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
        self.move = None
        self.children = []
        self.count = 0
        self.win = 0
        self.score = 0

    def has_children(self):
        return bool(self.children)

    def is_fully_expanded(self):
        return bool(len(self.state.possible_moves()))

    def get_best_child(self):
        return max(self.children, key= lambda n: n.score)

    def get_new_child(self):
        move = random.choice(self.state.possible_moves())
        state = self.state.update(move)
        child = Node(state, self)

    def update_score(self, result):
        self.count = self.count + 1
        self.win = self.count + result
        self.score = self.win/self.count \
                     + sqrt(2)*sqrt(log(self.parent.count)/self.count)

    def is_terminal(self):
        return self.state.is_terminal()

class MCTS:
    """ Monte Carlo Tree Search
    """
    def __init__(self, state):
        self.root = Node(state, None)

    def search(self, node):
        """
        Update Monte Carlo Tree
        """
        while (not node.is_terminal()) and (node.is_fully_expanded()):
            node = node.get_best_child()
        
        if not node.is_fully_expanded():
            node.get_new_child()

        result = self.rollout(node)
        self.backpropagate(node, result)


    def train(self, epoch):
        for _ in range(epoch):
            self.search(self.root)

    def rollout(self, node):
        state = node.state
        while not state.is_terminal():
            move = random.choice(state.possible_moves())
            state = state.update(move)
        return state.result

    def expand(self, node):
        move = random.choice(node.state.possible_moves())
        state = node.state.update(move)
        new_node = Node(state, node)
        node.children.append(new_node)
        return new_node

    def simulate(self, node):
        return self.rollout(node).get_score()

    def backpropagate(self, node, result):
        while node:
            node.update_score(result)
            node = node.parent