"""
Sources used:
"Floyd Warshall All Pairs Shortest Path Algorithm | Graph Theory | Dynamic Programming," Youtube, William Fiset
"Travelling Salesman Problem," opengenus.org

    In order to solve this problem, we need to save the most bunnies we can
    in the shortest amount of time. We have to find the longest possible path,
    which will require us to bruteforce all possible paths in the matrix. When we
    brutforce these paths, to be sure that there are no longer paths that result
    in shorter times, we need to find the shortest path between all pairs of bunnies.
    First we use the Floyd-Warshall algorithm to find this graph, and then run a bruteforce
    check on all possible path to find the optimal solution.

    floyd()

        The Floyd-Warshall algorithm loops over every pair of nodes in the matrix
        to find the optimal path between the two nodes given an intermediate node
        k. If the cost of going through an intermediate is found to be shorter than
        the direct route, the matrix is updated. Since negative cycles (infinite time loops)
        might exist, we use checkNegatives() to remove negative cycles.

        checkNegatives()

            We rerun the Floyd algorithm on the same matrix and see if we can find
            a better path for any of our nodes. Since our graphed already has optimal
            path costs, if we find any shorter distances, we know that there is a negative
            cycle and turn the cost into negative infinity.

    getPath()

        getPath() takes our shortest path matrix and finds the longest path that
        can be made in the given time limit. First, it creates an iterable object
        with all the possible permutations of paths that can be taken given the
        number of bunnies. Next, it iterates through these permutations of paths,
        going through each path with runPath() and finding the largest path that
        does not go over time. Once it finds an optimal path, it returns this
        as an iterable.

        runPath()

            runPath() simulates each path it's given by going from the start
            node to the bulkhead by iterating through the bunnyids in the path.
            After each new bunny is traversed, the time used up is tallied to
            compare with other paths.
"""

import itertools as it


def floyd(memo):
    for intermediate in range(size):
        for i in range(size):
            for j in range(size):
                if memo[i][intermediate] + memo[intermediate][j] < memo[i][j]:
                    memo[i][j] = memo[i][intermediate] + memo[intermediate][j]
    return checkNegatives(memo)


def checkNegatives(memo):
    for intermediate in range(size):
        for i in range(size):
            for j in range(size):
                if memo[i][intermediate] + memo[intermediate][j] < memo[i][j]:
                    memo[i][j] = float('-inf')
    return memo


def runPath(shorts, path):
    time = start = 0
    for bunny in path:
        next = bunny + 1
        time += shorts[start][next]
        start = next
    time += shorts[start][size - 1]
    return time


def getPath(shorts, limit):
    bunnies = range(size - 2)
    allPaths = it.chain.from_iterable(it.permutations(bunnies, r) for r in range(len(bunnies) + 1))
    bestPath = []
    for path in allPaths:
        time = runPath(shorts, path)
        if time <= limit and len(path) > len(bestPath):
            bestPath = path
    return bestPath


def solution(times, times_limit):
    global size
    size = len(times)
    shorts = floyd(times)
    return sorted(list(getPath(shorts, times_limit)))
