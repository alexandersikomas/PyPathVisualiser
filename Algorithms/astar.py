from graph import Graph
from node import Node


def aStar(start: Node, goal: Node, graph: Graph):
    openList = [start]
    closedList = []

    for row in graph.getNodes():
        for node in row:
            node.fCost = float('inf')
            node.gCost = float('inf')

    start.gCost = 0
    start.fCost = heuristic(start.getPosition(), goal.getPosition())

    while openList:
        # Find the node with the lowest estimated distance in the open list
        current = min(openList, key=lambda n: (n.fCost, n.hCost))

        if current == goal:
            path = []
            totalDistance = current.gCost
            # Trace the path by following the parent nodes back to the start
            while current is not start:
                path.append(current)
                current = current.parent
            # Return the path, with the start node at the front and the goal node at the end
            return path[::-1], totalDistance, closedList

        openList.remove(current)
        closedList.append(current)

        neighbours = graph.getNeighbours(current, diagonalOption=True)
        for neighbour in neighbours:
            if neighbour in closedList or not neighbour.isWalkable:
                continue

            tmpGCost = current.gCost + (neighbour.weight - 1) + heuristic(current.getPosition(),
                                                                          neighbour.getPosition())

            if (tmpGCost < neighbour.gCost) or neighbour not in openList:
                neighbour.parent = current
                neighbour.gCost = tmpGCost
                neighbour.fCost = tmpGCost + heuristic(neighbour.getPosition(), goal.getPosition())
                neighbour.hCost = heuristic(neighbour.getPosition(), goal.getPosition())

                if neighbour not in openList:
                    openList.append(neighbour)

    # If the open list is empty, we have explored all reachable nodes and there is no path to the goal
    return [[], 0, closedList]


def heuristic(startNode: [int, int], endNode: [int, int]) -> float:
    # Calculate the heuristic using the Manhattan distance formula
    dx = abs(startNode[0] - endNode[0])
    dy = abs(startNode[1] - endNode[1])

    if dx > dy:
        return 2 * dy + (dx - dy)
    return 2 * dx + (dy - dx)


def runAStar(start: Node, goal: Node, auxiliaryNodes: [Node], graph: Graph) -> tuple[list, int, list]:
    path = []
    closedList = []
    totalDistance = 0
    if auxiliaryNodes:
        for aNode in auxiliaryNodes:
            curPath, curDistance, curClosedList = aStar(start, aNode, graph)
            for node in curPath:
                path.append(node)

            for node in curClosedList:
                closedList.append(node)

            start = aNode
            # If at any point an auxiliary node is unreachable, return an empty path
            if curDistance == 0:
                return [], 0, []
            totalDistance += curDistance
    curPath, curDistance, curClosedList = aStar(start, goal, graph)
    totalDistance += curDistance
    for node in curPath:
        path.append(node)

    for node in curClosedList:
        closedList.append(node)

    return path, totalDistance, closedList
