from graph import Graph
from node import Node


def dijkstra(start: Node, goal: Node, graph: Graph) -> [[Node], int]:
    """dijkstra() is used to run dijkstra's shortest path algorithm"""
    # Create a list of nodes to be explored (the "open list")
    openList = [start]
    # Create a list of nodes that have been explored (the "closed list")
    closedList = []
    # Set the starting node's distance to 0
    start.distance = 0

    # Keep looping while there are nodes in the open list
    while openList:
        # Find the node with the lowest distance in the open list
        current = min(openList, key=lambda node: node.distance)

        # If the current node is the goal node, we have found the shortest path
        if current == goal:
            # Create an array to store the path
            path = []
            totalDistance = current.getDistance()
            # Trace the path by following the parent nodes back to the start
            while current != start:
                path.append(current)
                current = current.parent
            # Return the path, with the start node at the front and the goal node at the end
            return path[::-1], totalDistance

        # Remove the current node from the open list
        openList.remove(current)
        # Add the current node to the closed list
        closedList.append(current)

        # Get a list of the current node's neighbours
        neighbours = graph.getNeighbours(current)
        # Loop through the neighbours
        for neighbour in neighbours:
            # Skip the neighbour if it is in the closed list or is not walkable
            if neighbour in closedList or not neighbour.isWalkable:
                continue

            # Calculate the distance from the current node to the neighbour, it assumes that all diagonals are a
            # distance of 2 and all horizontals and verticals are a distance of 1
            distance = current.distance + neighbour.getWeight() * (int(neighbour.diagonal) + 1)

            # If the neighbour is not in the open list, add it to the open list
            if neighbour not in openList:
                openList.append(neighbour)
                neighbour.distance = distance
                neighbour.parent = current

    # If the open list is empty, we have explored all reachable nodes and there is no path to the goal
    return [[], 0]


def runDijkstra(start: Node, goal: Node, auxiliaryNodes: [Node], graph: Graph) -> [[Node], int]:
    """runDijkstra() is used to run dijkstra() with auxiliary nodes"""
    path = []
    totalDistance = 0
    # If there are auxiliary nodes, run Dijkstra's algorithm with each one in turn
    if auxiliaryNodes:
        for aNode in auxiliaryNodes:
            curPath, curDistance = dijkstra(start, aNode, graph)
            # Add the current path to the overall path
            for node in curPath:
                path.append(node)
            # Set the current node as the new starting node
            start = aNode
            # Add the current distance to the total distance
            # If at any point an auxiliary node is unreachable, return an empty path
            if curDistance == 0:
                return [], 0
            totalDistance += curDistance
    # Run Dijkstra's algorithm with the final start and goal nodes
    curPath, curDistance = dijkstra(start, goal, graph)
    totalDistance += curDistance
    for node in curPath:
        path.append(node)
    return path, totalDistance
