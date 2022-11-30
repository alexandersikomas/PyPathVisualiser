from node import Node


class Graph:
    def __init__(self, sizeX: int, sizeY: int) -> None:
        self.nodes = []
        self.generateNodes([sizeX, sizeY])

    def generateNodes(self, size: [int, int]) -> None:
        for i in range(size[0]):
            for j in range(size[1]):
                self.nodes.append(Node([i, j]))

    def getNodes(self) -> [Node]:
        return self.nodes
