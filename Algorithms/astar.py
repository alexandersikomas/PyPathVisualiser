from typing import List, Any, Tuple

from graph import Graph
from node import Node


def aStar(start: Node, goal: Node, graph: Graph):
    openList = [start]
    closedList = []
    start.distance = 0

    # Calculate the heuristic (estimated distance to goal) for the start node
    start.estimated = heuristic(start.getPosition(), goal.getPosition())

    # Keep looping while there are nodes in the open list
    while openList:
        # Find the node with the lowest estimated distance in the open list
        current = min(openList, key=lambda node: node.estimated)
        #current = openList.sort(key=lambda node: node.estimated)

        # If the current node is the goal node, we have found the shortest path
        if current is goal:
            path = []
            totalDistance = current.distance
            # Trace the path by following the parent nodes back to the start
            while current is not start:
                path.append(current)
                current = current.parent
            # Return the path, with the start node at the front and the goal node at the end
            return path[::-1], totalDistance, closedList

        openList.remove(current)
        closedList.append(current)

        neighbours = graph.getNeighbours(current)
        for neighbour in neighbours:
            if neighbour in closedList or not neighbour.isWalkable:
                continue
            # Calculate the distance from the current node to the neighbour
            distance = current.distance + neighbour.getWeight() * (int(neighbour.diagonal) + 1)

            if neighbour not in openList:
                # Set the neighbour's distance and estimated distance
                neighbour.distance = distance
                neighbour.estimated = heuristic(neighbour.getPosition(), goal.getPosition())
                # Set the neighbour's parent node to the current node
                neighbour.parent = current
                openList.append(neighbour)
            if neighbour.estimated < neighbour.distance:
                neighbour.distance = neighbour.estimated
                neighbour.parent = current


    # If the open list is empty, we have explored all reachable nodes and there is no path to the goal
    return [[], 0, []]


def heuristic(startNode: [int, int], endNode: [int, int]) -> int:
    # Calculate the heuristic using the Manhattan distance formula
    return abs(startNode[0] - endNode[0]) + abs(startNode[1] - endNode[1])


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
                return [], 0
            totalDistance += curDistance
    curPath, curDistance, curClosedList = aStar(start, goal, graph)
    totalDistance += curDistance
    for node in curPath:
        path.append(node)

    for node in curClosedList:
        closedList.append(node)

    return path, totalDistance, closedList
