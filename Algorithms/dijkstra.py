from graph import Graph
from node import Node


def dijkstra(start: Node, goal: Node, graph: Graph):
    # Create a list of nodes to be explored (the "open list")
    openList = [start]
    # Create a list of nodes that have been explored (the "closed list")
    closedList = []
    start.distance = 0

    # Keep looping while there are nodes in the open list
    while openList is not None:
        # Finds the node with the lowest distance
        current = min(openList, key=lambda node: node.distance)

        # If the current node is the goal node, we have found the shortest path
        if current is goal:
            # Create an array to store the path
            path = []
            # Trace the path by following the parent nodes back to the start
            while current is not start:
                path.append(current)
                current = current.parent
            # Return the path, with the start node at the front and the goal node at the end
            return path[::-1]

        openList.remove(current)
        closedList.append(current)

        # Get a list of the current node's neighbours
        neighbours = graph.getNeighbours(current)
        for neighbour in neighbours:
            if neighbour in closedList or not neighbour.isWalkable:
                continue

            # Finds the distance from the current node to the neighbour
            distance = current.distance + neighbour.getWeight()

            if neighbour not in openList:
                openList.append(neighbour)
            else:
                if neighbour.distance > distance:
                    neighbour.distance = distance
                    neighbour.parent = current

    # If the open list is empty, we have explored all reachable nodes and there is no path to the goal
    return []


def runDijkstra(start, goal, auxiliaryNodes, graph):
    if auxiliaryNodes:
        for _ in auxiliaryNodes:
            tmp = auxiliaryNodes.pop(0)
            dijkstra(start, tmp, graph)
            start = tmp
    dijkstra(start, goal, graph)
