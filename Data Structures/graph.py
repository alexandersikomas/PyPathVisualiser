from node import Node


class Graph:
    def __init__(self, size: [int, int]) -> None:
        print(size)
        self.nodes = [[0 for _ in range(0, size[1] + 1)] for _ in range(0, size[0] + 1)]
        self.generateNodes(size)

    def generateNodes(self, size: [int, int]) -> None:
        for i in range(0, size[0] + 1):
            for j in range(0, size[1] + 1):
                self.nodes[i][j] = Node([i, j])

    def getNodes(self) -> [Node]:
        return self.nodes

    def findStart(self) -> int | bool:
        for rows in self.nodes:
            for node in rows:
                if node.getType() == 1:
                    return node
        return False

    def findEnd(self) -> int | bool:
        for rows in self.nodes:
            for node in rows:
                if node.getType() == 2:
                    return node
        return False
