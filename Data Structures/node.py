class Node:
    def __init__(self, position: [int, int], parent=None) -> None:
        self.position = position
        self.parent = parent
        self.distance = 0
        self.weight = 1
        self.type = -1

    def setWeight(self, weight: int) -> None:
        self.weight = weight

    def setDistance(self, distance: int) -> None:
        self.distance = distance

    def setType(self, type) -> None:
        self.type = type

    def getWeight(self) -> int:
        return self.weight

    def getPosition(self) -> [int, int]:
        return self.position

    def getDistance(self) -> int:
        return self.distance

    def getType(self) -> int:
        return self.type


