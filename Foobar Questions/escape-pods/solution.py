"""

    Just like the transitioning of our doomsday fuel, the layout of our rooms can be
    represented with a directed graph/matrix. Rather than probabilities, in this case
    the edges of our flow graph represent the bandwidth between two nodes/rooms.
    In order to find the maximum possible flow between our entrances/sources and our exits/
    sinks, we have several choices of algorithms to use. (Such as the Ford-Fulkerson, Karger's
    and min-cut.) The simplest and most accurate among these algorithms (since Karger's involves
    choosing random nodes to combine resulting in different answers) is the Ford-Fulkerson algorithm,
    where we will search through our flow graph to find a path from source to sink, and make adjustments
    using the residual graph, until we arrive at the optimal flow. The steps can be explained further
    by the functions we use to solve this problem:

    oneEntrance()/oneExit()

        Since our problems will involve multiple sources and sinks, we can make our solution easier
        by using a new single source that flows to all the previous sources, and a new single sink
        that takes flow of the previous sinks. The rule of conservation states that non-source/sink
        nodes must have an inflow that is equal to their outflow. Since we are turning our old sinks and
        sources into regular nodes, they must follow this rule. Therefore, our new source will send
        flow to the old sources equal to their outflow (using getCapacity()), and our new sinks will
        receive from the old sinks equal to their inflow (using getInflow()). First, we resize our paths
        matrix, using addRoom(), to accomodate the new source/sink, and then update the new source / old
        sinks according to the conservation rule.

    solution()

        In order to start off the Ford-Fulkerson algorithm, we must find any path from the source
        node to the sink. Once we have this path, we can use a residual graph that represents the changes
        we can make to the flow of the path that we took. If we run our search algorithm on this
        residual graph and find a valid path, that means we can modify our flows to direct still more
        flow to the sink. We then apply these new paths found in the residual graph, update the residual
        graph, and repeat the cycle until no new path is found in the residual. A while loop comes in
        handy for this algorithm by allowing us to add to increment our homeFree variable until there is
        no better path to take.

        search()

            search() implements a depth-first search algorithm to find a path through the paths matrix. It stops
            when either its stack is empty, or when it reaches the sink node. Once it is finished, it returns
            several important values: whether it found a valid path, the path it took, and minimum flow in the
            path that it took.

        updateResidual()

            updateResidual() uses the info from our search to update the paths matrix. We can convert paths into
            a residual graph by subtracting the smallest flow from the path that we took from each edge in the path
            and adding the same value in the opposite direction. We do this by iterating through the path that
            we took, and subtracting/adding from/to paths[] using the room numbers as indices.

"""


def getCapacity(paths, room):
    return sum(paths[room])


def getInflow(paths, toRoom):
    out = 0
    for row in paths:
        out += row[toRoom]
    return out


def addRoom(m, i):
    if i == 0:
        for row in m:
            row.insert(0, 0)
        m.insert(0, [0] * len(m[0]))
    elif i == 1:
        for row in m:
            row.append(0)
        m.append([0] * len(m[0]))
    return m


def oneEntrance(paths, entrances):
    paths = addRoom(paths, 0)
    for i in range(len(paths)):
        if i in entrances:
            paths[0][i] = getCapacity(paths, i)
    return paths


def oneExit(paths, exits):
    paths = addRoom(paths, 1)
    for i in range(len(paths)):
        if i in exits:
            paths[i][-1] = getInflow(paths, i)
    return paths


def search(m):
    pathTaken = []
    visited = [False] * len(m)
    stack = [0]
    flows = []
    visited[0] = True
    while stack and not visited[-1]:
        currentRoom = stack.pop(-1)
        for i in range(len(m[currentRoom])):
            if m[currentRoom][i] > 0 and not visited[i]:
                flows.append(m[currentRoom][i])
                stack.append(i)
                visited[i] = True
        pathTaken.append(currentRoom)
    return [visited[-1], pathTaken, min(flows or [0])]


def updateResidual(m, flow, pathTaken):
    for i in range(len(pathTaken) - 1):
        m[pathTaken[i]][pathTaken[i + 1]] -= flow
    m[pathTaken[-1]][-1] -= flow
    m[-1][pathTaken[-1]] += flow
    return m


def solution(entrances, exits, paths):
    if len(entrances) > 1:
        entrances = [item + 1 for item in entrances]
        paths = oneEntrance(paths, entrances)
    if len(exits) > 1:
        exits = [item + 1 for item in exits]
        paths = oneExit(paths, exits)
    homeFree = 0
    betterPathExists = True
    while betterPathExists:
        pathData = search(paths)
        betterPathExists = pathData[0]
        if not betterPathExists:
            break
        pathTaken = pathData[1]
        narrowestCorr = pathData[2]
        homeFree += narrowestCorr
        paths = updateResidual(paths, narrowestCorr, pathTaken)
    return homeFree


