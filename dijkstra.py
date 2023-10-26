from graph import Graph
from node import Node


def dijkstra(start: Node, goal: Node, graph: Graph) -> tuple[list, int, list]:
    """dijkstra() is used to run dijkstra's shortest path algorithm"""
    openList = [start]
    closedList = []
    start.distance = 0

    while openList:
        current = min(openList, key=lambda node: node.distance)

        if current == goal:
            path = []
            totalDistance = current.getDistance()
            while current != start:
                path.append(current)
                current = current.parent
            return path[::-1], totalDistance, closedList

        openList.remove(current)
        closedList.append(current)

        neighbours = graph.getNeighbours(current)
        for neighbour in neighbours:
            if neighbour in closedList or not neighbour.isWalkable:
                continue

            # Calculate the distance from the current node to the neighbour, it assumes that all diagonals are a
            # distance of 2 and all horizontals and verticals are a distance of 1
            distance = current.distance + neighbour.getWeight() + neighbour.diagonal

            # If the neighbour is not in the open list, add it to the open list
            if neighbour not in openList:
                openList.append(neighbour)
                neighbour.distance = distance
                neighbour.parent = current

    return [[], 0, []]


def runDijkstra(start: Node, goal: Node, auxiliaryNodes: [Node], graph: Graph) -> tuple[list, int, list]:
    """runDijkstra() is used to run dijkstra() with auxiliary nodes"""
    path = []
    closedList = []
    totalDistance = 0
    if auxiliaryNodes:
        for aNode in auxiliaryNodes:
            curPath, curDistance, curClosedList = dijkstra(start, aNode, graph)
            for node in curPath:
                path.append(node)
            for node in curClosedList:
                closedList.append(node)
            start = aNode
            if curDistance == 0:
                return [], 0, []
            totalDistance += curDistance
    # Run Dijkstra's algorithm with the final start and goal nodes
    curPath, curDistance, curClosedList = dijkstra(start, goal, graph)
    totalDistance += curDistance
    for node in curPath:
        path.append(node)

    for node in curClosedList:
        closedList.append(node)

    return path, totalDistance, closedList
