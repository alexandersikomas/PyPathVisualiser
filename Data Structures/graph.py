from node import Node


class Graph:
    def __init__(self, size: [int, int]) -> None:
        self.nodes = [[Node([j, i]) for i in range(0, size[1] + 1)] for j in range(0, size[0] + 1)]

    def getNodes(self) -> [Node]:
        return self.nodes

    def findStart(self) -> Node | bool:
        for rows in self.nodes:
            for node in rows:
                if node.getType() == 1:
                    return node
        return False

    def findEnd(self) -> Node | bool:
        for rows in self.nodes:
            for node in rows:
                if node.getType() == 2:
                    return node
        return False
