from node import Node
from graph import Graph


def checkBounds(self, nodePos: [int, int]) -> bool:
    """checkBounds() checks if a node is beyond the size of the grid"""
    if 0 <= nodePos[0] <= self.size[0] - 1:
        return False
    if 0 <= nodePos[1] <= self.size[1] - 1:
        return False
    return True


def checkObstacle(node: Node) -> bool:
    """checkObstacle() checks if a node is an obstacle by comparing its distance to infinity"""
    if node.getDistance() == float('inf'):
        return True
    return False


def calculateDistance(parent: Node, neighbour: Node, move: [int, int]) -> None:
    """calculateDistance() calculates if a move from one node to a neighbour is diagonal
    and updates the neighbour nodes distance"""
    moveCost = abs(sum(move))
    if moveCost == 1:
        neighbour.setDistance(parent.getDistance() + 10 * neighbour.getWeight())
    else:
        neighbour.setDistance(parent.getDistance() + 14 * neighbour.getWeight())


def generateNeighbours(self, parent: Node, openList: [], closedList) -> None:
    """generateNeighbours() finds the neighbours of a node and updates the distance from it to its neighbours"""
    parentPos = parent.getPosition()
    for i in range(3):
        for j in range(3):
            neighbourPos = [parentPos[0] + (i - 1), parentPos[1] + (j - 1)]
            if (checkBounds(neighbourPos)) and (neighbourPos not in closedList) \
                    and (not self.checkObstacle()):
                neighbour = Node(neighbourPos, parent)
                neighbour.setWeight(self.graph.getNodes()[parentPos + i - 1][parentPos + j - 1].getWeight())
                self.calculateDistance(parent, neighbour, [i - 1, j - 1])
                if neighbour not in openList:
                    openList.append(neighbour)


def heuristic(startNode, endNode):
    # Calculate the heuristic using the Manhattan distance formula
    return abs(startNode[0] - endNode[0]) + abs(startNode[1] - endNode[1])