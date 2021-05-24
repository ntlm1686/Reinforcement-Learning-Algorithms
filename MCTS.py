import random

class state:
    def __init__():
        pass

    def is_terminal(self):
        """
         return true if current state is the terminal
        """
        return 

    def possible_moves(self):
        return


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = None
        self.value = None
        self.count = 0

    def has_children(self):
        return False if self.children is None else True

    def is_fully_expanded(self):
        if len(self.children) == len(self.state.possible_moves()):
            return True
        else:
            return False

    def get_best_move(self):
        return max(self.children, key= lambda n: n.value)

class MCTS:
    """ Monte Carlo Tree Search
    """
    def __init__(self, state, spirit):
        self.root = Node(state, None)
        self.SPIRIT = spirit # flota, from 0 to 1

    def search(self, node):
        """
        """
        while state.is_terminal():
            is_explore = random.uniform(0, 1) if node.has_children() else 1
            # SELECT
            if node.is_fully_expanded() or is_explore<self.SPIRIT:
                # get the best node from the node's current children 
                node = self.get_best_move(node)
            else:
                # no action has been taken from this node
                # EXPAND
                node = self.expand(node)
                # SIMULATE
                node = self.rollout(node)

        # BACKPROPAGATE
        self.backpropagate(node)


    def select():
        pass

    def expand():
        pass

    def simulate():
        pass

    def backpropagate(self, node):
        pass