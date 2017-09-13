import sys
import collections
from copy import deepcopy


INFINITY = 999999
list_of_nodes = []
CUT_OFF = 3
player = 1





class state:
    def __init__(self, graph, current_player, color_weights_one, color_weights_two):
        self.board = graph
        self.colors = set(color_weights_one.keys())
        self.color_weights = {color:(color_weights_one[color],
                                     color_weights_two[color]) for color in color_weights_one}
        self.current_player = current_player
        self.player_one_score = 0
        self.player_two_score = 0

    def next_possible_moves(self):
        solution = []
        for node in sorted(self.board.get_vacant_neighbors()):
            used_colors = set([])
            for neighbor in sorted(self.board.get_neighbors(node)):
                if self.board.get_color(neighbor) is not None:
                    used_colors.add(self.board.get_color(neighbor))
            available_colors = self.colors - used_colors
            if available_colors:
                solution.append((node, sorted(list(available_colors))))

        return solution

    def move(self, node, color):
        self.board.set_color(node, color)
        if self.current_player == 1:
            self.player_one_score += self.color_weights[color][0]
        else:
            self.player_two_score += self.color_weights[color][1]
        self.current_player = 2 if self.current_player == 1 else 1
        return self

    def eval_score(self):
        return self.player_one_score - self.player_two_score

import collections
class graph:
    def __init__(self, adjacency_list):
        self.node_color = {node:None for node in adjacency_list}
        self.adjacency_list = adjacency_list
        self.vacant_neighbor_nodes = set([])

    def set_color(self, node, color):
        """
        Set color to a given node.
        """
        self.node_color[node] = color
        if node in self.vacant_neighbor_nodes:
            self.vacant_neighbor_nodes.remove(node)
        for each in self.get_neighbors(node):
            if self.node_color[each] is None:
                self.vacant_neighbor_nodes.add(each)
        # print self.node_color

    def get_color(self, node):

        return  self.node_color[node]

    def get_neighbors(self, node):
        """
        returns all neighbors of the nodde
        :return:
        """
        return self.adjacency_list[node]

    def get_vacant_neighbors(self):
        return list(self.vacant_neighbor_nodes)



def successors(state):
    succ = []
    for play in state.next_possible_moves():
        for color in play[1]:
            succ.append(((play[0], color), deepcopy(state).move(play[0], color)))
    return succ

log = []

def logger(node, color, depth, evalue, alpha, beta):
    global log
    if alpha ==  -INFINITY: alpha = '-inf'
    if beta == INFINITY: beta = 'inf'
    if evalue  == INFINITY: evalue = 'inf'
    if evalue == -INFINITY: evalue = '-inf'
    log.append('{}, {}, {}, {}, {}, {}\n'.format(node, color, depth, evalue, alpha, beta))


bestMove = None

def alphabeta_search(state, move, max_depth=3):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""


    def max_value(state, alpha, beta, depth, move):
        global bestMove
        if cutoff_test(state, depth):
            logger(move[0], move[1], depth, eval_fn(state), alpha, beta)
            return eval_fn(state)

        v = -INFINITY
        logger(move[0], move[1], depth, v, alpha, beta)

        for (a, s) in successors(state):
            # v = max(v, min_value(s, alpha, beta, depth + 1, a))
            temp_v = min_value(s, alpha, beta, depth + 1, a)
            if v != max(v, temp_v):
                v = temp_v
                if depth == 0: bestMove = (a[0], a[1], v)

            if v >= beta:
                logger(move[0], move[1], depth, v, alpha, beta)
                break
            alpha = max(alpha, v)

            logger(move[0], move[1], depth, v, alpha, beta)
        return v

    def min_value(state, alpha, beta, depth, move):
        if cutoff_test(state, depth):
            logger(move[0], move[1], depth, eval_fn(state), alpha, beta)
            return eval_fn(state)

        v = INFINITY
        logger(move[0], move[1], depth, v, alpha, beta)

        for (a, s) in successors(state):
            v = min(v, max_value(s, alpha, beta, depth + 1, a))
            if v <= alpha:
                logger(move[0], move[1], depth, v, alpha, beta)
                break
            beta = min(beta, v)
            logger(move[0], move[1], depth, v, alpha, beta)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = lambda state, depth: depth >= max_depth or len(state.next_possible_moves()) == 0
    eval_fn = lambda state: state.eval_score()
    alpha = -INFINITY
    beta = INFINITY
    max_value(state, alpha, beta, 0, move)


def main():
    color = []
    # p1_points = collections.OrderedDict({})
    # p2_points = collections.OrderedDict({})
    p1_points = {}
    p2_points = {}
    p1_moves = {}
    p_moves = {}
    p_moves_order = []
    # states = collections.OrderedDict({})
    states = {}
    temp = []
    count = 0
    toggle = 0
    with open(sys.argv[2]) as input:
        for line in input:
            if count == 0:
                color = line.strip().split(",")
                color = [c.strip() for c in color]
            elif count == 1:
                temp = line.strip().split(",")
                for i in range(len(temp)):
                    # if toggle==0:
                    #     p1_moves[temp[i].split(":")[0]] = temp[i].split(":")[1].split("-")[0]
                    #     toggle+=1
                    # else:
                    #     p2_moves[temp[i].split(":")[0]] = temp[i].split(":")[1].split("-")[0]
                    #     toggle-=1
                    p_moves[temp[i].split(":")[0].strip()] = temp[i].split(":")[1].split("-")[0].strip()
                    p_moves_order.append(temp[i].split(":")[0].strip())
                del temp[:]
                # p1_moves = {k.strip(): v.strip() for k, v in p1_moves.iteritems()}
                # p2_moves = {k.strip(): v.strip() for k, v in p2_moves.iteritems()}
                # p_moves = {k.strip(): v.strip() for k, v in p_moves.iteritems()}
                p_moves = [(k, p_moves[k]) for k in p_moves_order]
                print p_moves

            elif count == 2:
                depth = int(line)
            elif count == 3:
                temp = line.strip().split(",")
                for p in temp:
                    p1_points[p.strip().split(":")[0]] = int(p.strip().split(":")[1])
                sorted_p1_points = collections.OrderedDict(sorted(p1_points.items(), reverse=True))
                del temp[:]
            elif count == 4:
                temp = line.strip().split(",")
                for p in temp:
                    p2_points[p.strip().split(":")[0]] = int(p.strip().split(":")[1])
                sorted_p2_points = collections.OrderedDict(sorted(p2_points.items(), reverse=True))
                del temp[:]
            else:
                states[line.strip().split(":")[0]] = line.strip().split(":")[1].split(",")
            for key in states:
                states[key] = [s.strip() for s in states[key]]
            count += 1
        # sorted_states = collections.OrderedDict(sorted(states.items()))
        # print sorted_states
        start_graph = graph(states)
        state1 = state(start_graph, 1, p1_points, p2_points)
        # for k, v in p1_moves.iteritems():
        #     state1.move(k, v)
        # for k, v in p2_moves.iteritems():
        #     state1.move(k, v)
        for k,v in p_moves:
            state1.move(k,v)

        root = state1
        #alphabeta_search(root, (k, v), depth)
        alphabeta_search(root,p_moves[-1],depth)
        with open('output.txt', 'w') as f:
            for line in log:
                f.write(line)
            f.write('{}, {}, {}'.format(*bestMove))




if __name__ == "__main__":
    main()
