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

    def getNeighbours(self, node):
        neighbours = []

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            pos = node.getPosition()
            x = pos[0] + dx
            y = pos[1] + dy

            if x < 0 or y < 0 or x >= len(self.nodes) or y >= len(self.nodes[0]):
                continue
            else:
                neighbours.append(self.nodes[x][y])
        return neighbours
