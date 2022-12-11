from graph import Graph
from node import Node


def aStar(start: Node, goal: Node, graph: Graph):
    openList = [start]
    closedList = []
    start.distance = 0

    # Calculate the heuristic (estimated distance to goal) for the start node
    start.estimated = heuristic(start.getPosition(), goal.getPosition())

    # Keep looping while there are nodes in the open list
    while openList is not None:
        # Find the node with the lowest estimated distance in the open list
        current = min(openList, key=lambda node: node.estimated)

        # If the current node is the goal node, we have found the shortest path
        if current is goal:
            path = []
            # Trace the path by following the parent nodes back to the start
            while current is not start:
                path.append(current)
                current = current.parent
            # Return the path, with the start node at the front and the goal node at the end
            return path[::-1]

        openList.remove(current)
        closedList.append(current)

        neighbours = graph.getNeighbours(current)
        for neighbour in neighbours:
            if neighbour in closedList or not neighbour.isWalkable:
                continue
            # Calculate the distance from the current node to the neighbour
            distance = current.distance + neighbour.getWeight()

            if neighbour not in openList:
                # Set the neighbour's distance and estimated distance
                neighbour.distance = distance
                neighbour.estimated = distance + heuristic(neighbour.getPosition(), goal.getPosition())
                # Set the neighbour's parent node to the current node
                neighbour.parent = current
                openList.append(neighbour)
            else:
                # Otherwise, if the current distance to the neighbour is shorter than the previously
                # recorded distance, update the neighbour's distance and estimated distance
                if neighbour.distance > distance:
                    neighbour.distance = distance
                    neighbour.estimated = distance + heuristic(neighbour.getPosition(), goal.getPosition())

                    neighbour.parent = current
    # If the open list is empty, we have explored all reachable nodes and there is no path to the goal
    return []


def heuristic(startNode, endNode):
    # Calculate the heuristic using the Manhattan distance formula
    return abs(startNode[0] - endNode[0]) + abs(startNode[1] - endNode[1])


def runAStar(start, goal, auxiliaryNodes, graph):
    if auxiliaryNodes:
        for _ in auxiliaryNodes:
            tmp = auxiliaryNodes.pop(0)
            aStar(start, tmp, graph)
            start = tmp
    aStar(start, goal, graph)
