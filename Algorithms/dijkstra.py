from graph import Graph
from node import Node
import utility

class Dijkstra:
    def __init__(self, graph: Graph, startNodePos: [int, int], endNodePos: [int, int], size: [int, int]) -> None:
        self.graph = graph
        self.startNodePos = startNodePos
        self.endNodePos = endNodePos
        self.size = size
        self.route = []
        self.routeFound = False
        self.openList = []
        self.closedList = []

    # def checkBounds(self, nodePos: [int, int]) -> bool:
    #     """checkBounds() checks if a node is beyond the size of the grid"""
    #     if 0 <= nodePos[0] <= self.size[0] - 1:
    #         return False
    #     if 0 <= nodePos[1] <= self.size[1] - 1:
    #         return False
    #     return True
    #
    # @staticmethod
    # def checkObstacle(node: Node) -> bool:
    #     """checkObstacle() checks if a node is an obstacle by comparing its distance to infinity"""
    #     if node.getDistance() == float('inf'):
    #         return True
    #     return False
    #
    # @staticmethod
    # def calculateDistance(parent: Node, neighbour: Node, move: [int, int]) -> None:
    #     """calculateDistance() calculates if a move from one node to a neighbour is diagonal
    #     and updates the neighbour nodes distance"""
    #     moveCost = abs(sum(move))
    #     if moveCost == 1:
    #         neighbour.setDistance(parent.getDistance() + 10 * neighbour.getWeight())
    #     else:
    #         neighbour.setDistance(parent.getDistance() + 14 * neighbour.getWeight())
    #
    # def generateNeighbours(self, parent: Node) -> None:
    #     """generateNeighbours() finds the neighbours of a node and updates the distance from it to its neighbours"""
    #     parentPos = parent.getPosition()
    #     for i in range(3):
    #         for j in range(3):
    #             neighbourPos = [parentPos[0] + (i - 1), parentPos[1] + (j - 1)]
    #             if (self.checkBounds(neighbourPos)) and (neighbourPos not in self.closedList) \
    #                     and (not self.checkObstacle()):
    #                 neighbour = Node(neighbourPos, parent)
    #                 neighbour.setWeight(self.graph.getNodes()[parentPos + i - 1][parentPos + j - 1].getWeight())
    #                 self.calculateDistance(parent, neighbour, [i - 1, j - 1])
    #                 if neighbour not in self.openList:
    #                     self.openList.append(neighbour)

    def dijkstra(self) -> None:
        """dijkstra() performs Dijkstra's shortest path algorithm from class attributes"""
        startNode = Node(self.startNodePos)
        endNode = Node(self.endNodePos)
        self.openList.append(startNode)

        while self.openList:
            curIndex = 0
            curNode = self.openList[0]
            for index, iNode in enumerate(self.openList):
                if iNode.getDistance() < curNode.getDistance():
                    curNode = iNode
                    curIndex = index
            if curNode.getPosition() == endNode.getPosition():
                # TODO: FINISH
                self.routeFound = True

            # TODO: DISPLAY PATH
            utility.generateNeighbours(curNode, self.openList, self.closedList)
            self.openList.remove(curIndex)
            self.closedList.append(curNode.getPosition())

    def runDijkstra(self, auxiliaryNodes: [Node]) -> None:
        """runDijkstra() takes a list of nodes as a parameter and performs dijkstra between many nodes."""
        startNode = self.startNodePos
        endNode = self.endNodePos
        if auxiliaryNodes:
            for aNode in auxiliaryNodes:
                self.endNodePos = aNode.getPosition()
                self.dijkstra()
                self.startNodePos = aNode.getPosition()
        self.startNodePos = startNode
        self.endNodePos = endNode
        self.dijkstra()
