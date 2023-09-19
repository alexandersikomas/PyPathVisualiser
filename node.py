class Node:
    def __init__(self, position: [int, int], parent=None) -> None:
        """type values: -1 is empty, 1 is start, 2 is end, 3 is auxiliary, 4 is wall node"""
        self.position = position
        self.parent = parent
        self.distance = 0
        self.estimated = 0
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.isWalkable = True
        self.diagonal = False
        self.weight = 1
        self.type = -1

    def setWeight(self, weight: int) -> None:
        self.weight = weight

    def setDistance(self, distance: int) -> None:
        self.distance = distance

    def setType(self, newType) -> None:
        self.type = newType

    def getWeight(self) -> int:
        return self.weight

    def getPosition(self) -> [int, int]:
        return self.position

    def getDistance(self) -> int:
        return self.distance

    def getType(self) -> int:
        return self.type

    def setWalkable(self, walkable: bool) -> None:
        self.isWalkable = walkable
