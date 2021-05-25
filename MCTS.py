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

    def update(self, move):
        return

    def get_score(self):
        pass

    def _update_score(self):
        pass

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = None
        self.score = None
        self.count = 0

    def has_children(self):
        return False if self.children is None else True

    def is_fully_expanded(self):
        if len(self.children) == len(self.state.possible_moves()):
            return True
        else:
            return False

    def get_best_move(self):
        return max(self.children, key= lambda n: n.score)

    def update_score(self, result):
        self.score = self.state._update_score(result)

class MCTS:
    """ Monte Carlo Tree Search
    """
    def __init__(self, state, spirit):
        self.root = Node(state, None)
        self.SPIRIT = spirit # float, from 0 to 1

    def search(self, node):
        """
        """
        while node.state.is_terminal():
            is_explore = random.uniform(0, 1) if node.has_children() else 1
            # SELECT
            if node.is_fully_expanded() or is_explore<self.SPIRIT:
                # get the best node from the current node's children 
                node = self.get_best_move(node)
            else:
                # no action has been taken from this node
                # EXPAND
                node = self.expand(node)
                # SIMULATE
                result = self.simulate(node)
                break

        # BACKPROPAGATE
        self.backpropagate(node, result)

    def rollout(self, node):
        state = node.state
        while not state.is_terminal():
            move = random.choice(state.possible_moves())
            state = state.update(move)
        return state

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