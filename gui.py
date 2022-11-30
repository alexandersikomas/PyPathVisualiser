import pygame
import math


class PyGUI:
    def __init__(self) -> None:
        self.caption = "PyPath Visualiser"
        self.windowSize = (1336, 768)
        self.isRunning = None
        self.window = pygame.display.set_mode(self.windowSize)
        self.fadeRectSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.xLOffset = 50
        self.xROffset = 50
        self.yTOffset = 150
        self.yBOffset = 50
        self.margin = 20

    def run(self) -> None:
        """run() is the main loop of the GUI, it handles the events"""
        pygame.init()
        self.window.fill((0, 0, 0))
        pygame.display.set_caption(self.caption)

        self.isRunning = True

        while self.isRunning:
            # Decreases the opacity for the rectangles by 50 for every tick
            self.fadeRectSurface.fill((0, 0, 0, 50))

            self.drawGrid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.checkMouseOnGrid(pos):
                        for i in self.mouseToIndex(pos):
                            print(i)

            curPos = pygame.mouse.get_pos()
            curIndex = self.mouseToIndex(curPos)
            if self.checkMouseOnGrid(curPos):
                # Creates a yellow rectangle and increases the opacity by 50 for every tick
                self.drawRectOnHover(curIndex)

            # Sets FPS to 60
            self.clock.tick(60)
            # Draws rectangle surface to screen at 0, 0
            self.window.blit(self.fadeRectSurface, (0, 0))
            # Updates all elements that aren't part of a surface
            pygame.display.update()

    def drawGrid(self) -> None:
        """drawGrid() draws a grid on the GUI in a way which allows the window size and offsets to be changed"""
        for i in range(self.xLOffset, self.windowSize[0] - self.xROffset, self.margin):
            for j in range(self.yTOffset, self.windowSize[1] - self.yBOffset, self.margin):
                node = pygame.Rect(i, j, self.margin, self.margin)
                pygame.draw.rect(self.window, (200, 200, 200), node, 1)

    def getGridEnds(self) -> [int, int]:
        """getGridEnds() performs a calculation which will get the x and y values of where the grid stops"""
        xEnd = math.ceil(((self.windowSize[0]-self.xLOffset-self.xROffset) / self.margin))*self.margin + self.xLOffset - 1
        yEnd = math.ceil((self.windowSize[1]-self.yTOffset-self.yBOffset) / self.margin)*self.margin + self.yTOffset - 1
        return [xEnd, yEnd]

    def checkMouseOnGrid(self, pos: [int, int]) -> bool:
        """checkMouseOnGrid() evaluates the position given, checking if the values are between the grid start and end"""
        endValues = self.getGridEnds()
        if self.xLOffset <= pos[0] <= endValues[0]:
            if self.yTOffset <= pos[1] <= endValues[1]:
                return True
        return False

    def mouseToIndex(self, pos: [int, int]) -> [int, int]:
        """mouseToIndex() converts a mouse position to the appropriate index for the grid/node array"""
        xIndex = math.floor((pos[0]-self.xLOffset)/20)
        yIndex = math.floor((pos[1]-self.yTOffset)/20)
        return [xIndex, yIndex]

    def drawRectOnHover(self, pos: [int, int]) -> None:
        """drawRectOnHover() takes in an x and y index position and draws a rectangle to highlight where the mouse is"""
        tmpRect = pygame.Rect(self.xLOffset+self.margin*pos[0], self.yTOffset+self.margin*pos[1], self.margin, self.margin)
        pygame.draw.rect(self.fadeRectSurface, (255, 255, 0, 50), tmpRect, 0)


z = PyGUI()
z.run()
