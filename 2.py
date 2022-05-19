import numpy as np
from decimal import Decimal

iterations = 1_000_000

# ______________________________________В) Поиск стационарного распределения____________________________________________


class TrasitionMatrix:
    def __init__(self, p1):
        """
        Args:
            p1(float): probability of the winning a round by the 1rst player
        """
        self.p1 = p1
        self.difference_in_score_indexes = {(0): 0, (1): 1, (2): 2, (-1): 3, (-2): 4}
        self.trans_matrix = self._trans_matrix_init()
        self.state_vector = np.zeros(shape=5)
        self._self_vector_init()

    def stat_distr_with_output(self):
        a = self.stat_distr()
        print("_" * 100)
        print("Stationary Distribution")
        print(f"Player 1 probability to win - {a[2]*100}%")
        print(f"Player 2 probability to win - {a[4]*100}%")

    def stat_distr(self):
        a = self.trans_matrix
        for i in range(100):
            a = np.dot(a, a)
        return np.dot(self.state_vector, a)

    def _trans_matrix_init(self):
        # In our case initializing transition matrix "by hands" is much easier and is much cleaner
        w = self.p1
        l = float(1-Decimal(f"{w}"))
        return np.array([[0, w, 0, l, 0],
                         [l, 0, w, 0, 0],
                         [0, 0, 1, 0, 0],
                         [w, 0, 0, 0, l],
                         [0, 0, 0, 0, 1]])

    def _self_vector_init(self):
        self.state_vector[0] = 1

# _____________________________________Б) Проход возможных исходов по дереву____________________________________________


class Node:
    def __init__(self, score_difference, p1):
        """
        Args:
            score_difference(int): difference in score (1 if (1, 0), -1 if (0, 1))
            p1(float): probability of the winning a round by the 1rst player
        """
        self.index = score_difference
        self.w = None
        self.l = None
        self.ptw = p1


class Graph:
    def __init__(self, p1):
        """
        Args:
            p1(float): probability of the winning a round by the 1rst player
        """
        self.p1 = p1
        self.root = Node(0, p1)
        self._build_graph(self.root)
        self.get_percentages()

    def get_percentages(self):
        results = {(1, 0): 0, (0, 1): 0}

        for i in range(iterations):
            temp = self.root
            while temp.w:
                if np.random.random() < temp.ptw:
                    temp = temp.w
                else:
                    temp = temp.l

            if temp.index > 0:
                results[(1, 0)] += 1
            else:
                results[(0, 1)] += 1

        results[(1, 0)] /= iterations
        results[(0, 1)] /= iterations

        print("_" * 100)
        print("DTree")
        print(f"Player 1 probability to win - {results[(1,0)] * 100}%")
        print(f"Player 2 probability to win - {results[(0,1)] * 100}%")

    def _build_graph(self, node):
        """
        Args:
            node(Node): Node class object
        """
        if node.index == 0:
            node.w = Node(1, self.p1)
            node.w.l = node
            self._build_graph(node.w)

            node.l = Node(-1, self.p1)
            node.l.w = node
            self._build_graph(node.l)
        elif node.index == 1:
            node.w = Node(2, 1)
        else:
            node.l = Node(-2, 1)

    def print_graph(self):
        next = self.root
        while next:
            print(next.index)
            next = next.w

        next = self.root
        while next:
            print(next.index)
            next = next.l

# _____________________________________А) Оценка методом Монте-Карло____________________________________________________


def monte_carlo(p1):
    """
    Args:
        p1(float): probability of the winning a round by the 1rst player
    """
    stats = {(1, 0): 0, (0, 1): 0}

    for i in range(iterations):
        diff = 0
        while True:
            if np.random.random() < p1:
                diff += 1
            else:
                diff -= 1
            if abs(diff) == 2:
                break
        if diff > 0:
            stats[(1, 0)] += 1
        else:
            stats[(0, 1)] += 1

    stats[(0, 1)] /= iterations
    stats[(1, 0)] /= iterations

    print("_" * 100)
    print("Monte Carlo")
    print(f"Player 1 probability to win - {stats[(1,0)] * 100}%")
    print(f"Player 2 probability to win - {stats[(0,1)] * 100}%")


p1 = 0.25

monte_carlo(p1)

Graph(p1)

TrasitionMatrix(p1).stat_distr_with_output()
