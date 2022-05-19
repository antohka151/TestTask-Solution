import numpy as np
from decimal import Decimal
from collections import OrderedDict

iterations = 1_000_000

# ______________________________________В) Поиск стационарного распределения____________________________________________


class TransitionMatrix:
    def __init__(self, p1, p2):
        """
        Args:
            p1(float): probability of the winning a round by the 1rst player on his serve
            p2(float): probability of the winning a round by the 1rst player on his opponents serve
        """
        self.p1 = p1
        self.p2 = p2
        self.score_indexes = self._get_score_indexes()
        self.trans_matrix = np.zeros(shape=(len(self.score_indexes), len(self.score_indexes)))
        self._trans_matrix_init()
        self.state_vector = np.zeros(shape=(len(self.score_indexes)))
        self._state_vector_init()

    def stat_distr_filtered(self):
        a = list(self.score_indexes)[-21:]
        b = self.stat_distr()[-21:]
        result_dict = OrderedDict(sorted({a[i]: b[i] for i in range(len(a))}.items(), key=lambda t: t[0]))
        return result_dict

    def stat_distr(self):
        a = self.trans_matrix
        for i in range(200):
            a = np.dot(a, a)
        return np.dot(self.state_vector, a)

    def _trans_matrix_init(self):
        for i in range(10):
            self.trans_matrix[self.score_indexes[(11, i)]][self.score_indexes[(11, i)]] = 1
            self.trans_matrix[self.score_indexes[(i, 11)]][self.score_indexes[(i, 11)]] = 1
        self.trans_matrix[self.score_indexes[(10, 10)]][self.score_indexes[(10, 10)]] = 1
        self._trans_matrix_init2((0, 0), self.p1, self.p2)

    def _trans_matrix_init2(self, score, prob1, prob2):
        """
        prob1 and prob2 changes after 2 rounds

        Args:
            score(tuple): score at the match (f.e. (4, 2))
            prob1(float): probability of the winning a round by the 1rst player on his or on his opponents serve
            prob2(float): probability of the winning a round by the 1rst player on his or on his opponents serve
        """
        if max(score) < 11 and score != (10, 10):
            if sum(score) % 2 == 0 and sum(score) != 0:
                prob1, prob2 = prob2, prob1
            self.trans_matrix[self.score_indexes[score]][self.score_indexes[(score[0]+1, score[1])]] = prob1
            self._trans_matrix_init2((score[0]+1, score[1]), prob1, prob2)
            self.trans_matrix[self.score_indexes[score]][self.score_indexes[(score[0], score[1] + 1)]] = float(1-Decimal(f"{prob1}"))
            self._trans_matrix_init2((score[0], score[1]+1), prob1, prob2)

    def _state_vector_init(self):
        self.state_vector[self.score_indexes[(0, 0)]] = 1

    @staticmethod
    def _get_score_indexes():
        score_dict = {}
        for i in range(12):
            for j in range(11):
                score_dict[(i, j)] = 11 * i + j
        del score_dict[(11, 10)]
        for i in range(10):
            score_dict[(i, 11)] = 131 + i
        return score_dict

# _____________________________________Б) Проход возможных исходов по дереву____________________________________________


class Node:
    def __init__(self, score, p1, p2):
        """
        Args:
            score(tuple): score at the match (f.e. (4, 2))
            p1(float): probability of the winning a round by the 1rst player on his serve
            p2(float): probability of the winning a round by the 1rst player on his opponents serve
        """
        self.score = score
        self.l = None
        self.r = None
        if (sum(score) % 2 == 0) and (sum(score) != 0):
            p1, p2, = p2, p1
        self.p2 = p2
        # lp - probability to go left (rp is 1-lp)
        self.lp = p1


class Tree:
    def __init__(self, p1, p2):
        """
        Args:
            p1(float): probability of the winning a round by the 1rst player on his serve
            p2(float): probability of the winning a round by the 1rst player on his opponents serve
        """
        self.root = Node((0, 0), p1, p2)
        self._add(self.root)

    def _add(self, node):
        """
        Args:
            node(Node): Node class object
        """
        if (11 not in node.score) and (sum(node.score) != 20):
            node.l = Node((node.score[0] + 1, node.score[1]), node.lp, node.p2)
            self._add(node.l)
            node.r = Node((node.score[0], node.score[1] + 1), node.lp, node.p2)
            self._add(node.r)

    def descending(self):
        # Creating a dict.
        score_p = {}
        for _ in range(10):
            score_p[(_, 11)] = 0
            score_p[(11, _)] = 0
        score_p[(10, 10)] = 0
        score_p = OrderedDict(sorted(score_p.items(), key=lambda t: t[0]))

        for i in range(iterations):
            # Coinflip - who will start first
            coinflip = np.random.randint(0, 2)
            # If 0 (1st player starts) - we continue normally, elif we use p2
            score_p[self._descending(self.root, coinflip)] += 1
        for key in score_p:
            score_p[key] /= iterations
        return score_p

    def _descending(self, node, coinflip):
        """
        Args:
            node(Node): Node class object
            coinflip(int): This var. says who started the game first
        """
        while (node.l is not None) and (node.r is not None):
            if not coinflip:
                if np.random.random() < node.lp:
                    node = node.l
                else:
                    node = node.r
            else:
                if np.random.random() < node.p2:
                    node = node.l
                else:
                    node = node.r
        return node.score

    def printTree(self):
        # I do not recommend using this function :)  *Tree is too big*
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        """
        Args:
            node(Node): Node class object
        """
        if (node.l is not None) and (node.r is not None):
            self._printTree(node.l)
            self._printTree(node.r)
        else:
            print(str(node.score))

# _____________________________________А) Оценка методом Монте-Карло____________________________________________________


def monte_carlo(p1, p2):
    """
    Args:
        p1(float): probability of the winning a round by the 1rst player on his serve
        p2(float): probability of the winning a round by the 1rst player on his opponents serve
    """
    # Creating a dict.
    score_p = {}
    for _ in range(10):
        score_p[(_, 11)] = 0
        score_p[(11, _)] = 0
    score_p[(10, 10)] = 0
    score_p = OrderedDict(sorted(score_p.items(), key=lambda t: t[0]))

    for i in range(iterations):
        score = [0, 0]
        # serve = 0 if we are 100% sure that player 1 will start the game
        serve = np.random.randint(0, 2)
        j = 0
        while (11 not in score) and (sum(score) != 20):
            if np.random.random() < (p1 if serve == 0 else p2):
                score[0] += 1
            else:
                score[1] += 1
            j += 1
            if j % 2 == 0:
                serve = not serve
        score_p[tuple(score)] += 1
    for key in score_p:
        score_p[key] /= iterations
    return score_p


# _________________________________________________Main_________________________________________________________________

p1, p2 = 0.9, 0.1

print("_"*100)
print("Monte Carlo")
a = monte_carlo(p1, p2)
for _ in a:
    print("{}: {:.5f}%".format(_, a[_]*100))

print("_"*100)
print("DTree")
b = Tree(p1, p2).descending()
for _ in b:
    print("{}: {:.5f}%".format(_, b[_]*100))

# if we are not sure who will start first
print("_"*100)
print("Stationary Distribution")
v_p1 = TransitionMatrix(p1, p2).stat_distr_filtered()
v_p2 = TransitionMatrix(p2, p1).stat_distr_filtered()
v = {i: (v_p1[i]+v_p2[i])/2 for i in v_p1}
for _ in v:
    print("{}: {:.5f}%".format(_, v[_]*100))

# if we are 100% sure that p1 will start first
# print("_"*100)
# print("Stationary Distribution")
# v = Transition_matrix(p1, p2).stat_distr_filtered()
# for _ in v:
#     print("{}: {:.5f}%".format(_, v[_]*100))
