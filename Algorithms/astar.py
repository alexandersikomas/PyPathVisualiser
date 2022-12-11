from graph import Graph
from node import Node
import utility


class AStar:
    def __init__(self, graph: Graph, startNodePos: [int, int], endNodePos: [int, int], size: [int, int]):
        self.graph = graph
        self.startNodePos = startNodePos
        self.endNodePos = endNodePos
        self.size = size
        self.route = []
        self.routeFound = False
        self.openList = []
        self.closedList = []

    def aStar(self) -> []:
        # Create a list to store the open nodes (nodes to be explored)
        startNode = Node(self.startNodePos)
        endNode = Node(self.endNodePos)
        open_nodes = [startNode]
        # Create a list to store the closed nodes (nodes that have been explored)
        closed_nodes = []
        # Set the starting node's G score (distance from start) to 0
        startNode.g = 0
        # Set the starting node's F score (estimated total distance) to its heuristic
        startNode.f = utility.heuristic(self.startNodePos, self.endNodePos)

        # While there are still nodes in the open nodes list
        while open_nodes:
            # Find the node in the open nodes list with the lowest F score
            current_node = open_nodes[0]
            for node in open_nodes:
                if node.f < current_node.f:
                    current_node = node

            # If the current node is the end node, we have found a path
            if current_node == endNode:
                # Create a list to store the path
                path = []

                # Traverse the path from the end node to the start node
                current = endNode
                while current is not startNode:
                    path.append(current)
                    current = current.parent

                # Reverse the path and return it
                return path[::-1]

            # Remove the current node from the open nodes list and add it to the closed nodes list
            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            # For each neighbor of the current node
            for neighbor in current_node.neighbors:
                # Skip the neighbor if it is in the closed nodes list or if it is not walkable
                if neighbor in closed_nodes or not neighbor.is_walkable:
                    continue

                # Calculate the G score of the neighbor (distance from start)
                g_score = current_node.g + 1

                # If the neighbor is not in the open nodes list
                if neighbor not in open_nodes:
                    # Set the neighbor's G score and F score
                    neighbor.g = g_score
                    neighbor.f = g_score + utility.heuristic(neighbor, endNode)

                    # Set the neighbor's parent to the current node
                    neighbor.parent = current_node

                    # Add the neighbor to the open nodes list
                    open_nodes.append(neighbor)
                else:
                    # If the neighbor is already in the open nodes list and its G score is higher than the calculated G
                    # score
                    if neighbor.g > g_score:
                        # Update the neighbor's G score and F score
                        neighbor.g = g_score
                        neighbor.f = g_score + utility.heuristic(neighbor, endNode)

                        # Set the neighbor's parent to the current node
                        neighbor.parent = current_node

                        # If the search failed, return an empty list
                    return []

    def search(self):
        return a_star_search(self.start, self.end)


# Define a function to calculate the heuristic for a given node



