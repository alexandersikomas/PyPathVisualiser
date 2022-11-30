class Node:
    def __init__(self, position: [int, int], parent=None) -> None:
        self.position = position
        self.parent = parent
        self.distance = 0
        self.weight = 1

    def setWeight(self, weight: int) -> None:
        self.weight = weight

    def setDistance(self, distance: int) -> None:
        self.distance = distance

    def getWeight(self) -> int:
        return self.weight

    def getPosition(self) -> [int, int]:
        return self.position

    def getDistance(self) -> int:
        return self.distance

