import pygame
import math
import json
from graph import Graph


class PyGUI:
    def __init__(self) -> None:
        with open("SETTINGS.json", 'r') as file:
            settings = json.load(file)
            self.windowSize = (settings['windowSize']['width'], settings['windowSize']['height'])
            self.xLOffset = settings['margins']['xLOffset']
            self.xROffset = settings['margins']['xROffset']
            self.yTOffset = settings['margins']['yTOffset']
            self.yBOffset = settings['margins']['yBOffset']
            self.margin = settings['margins']['margin']
            self.colours = settings['colors']
        self.caption = "PyPath Visualiser"
        self.isRunning = None
        self.window = pygame.display.set_mode(self.windowSize)
        self.fadeRectSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA)
        self.gridSurface = pygame.Surface(self.windowSize)
        self.clock = pygame.time.Clock()
        size = self.getGridSize()
        self.nodeGraph = Graph([size[0], size[1]])
        del size

    def run(self) -> None:
        """run() is the main loop of the GUI, it handles the events"""
        pygame.init()
        self.window.fill((0, 0, 0))
        pygame.display.set_caption(self.caption)
        # Without this you could select an option that is over the grid and the grid would automatically place for you
        potentialCollision = False
        # This makes 'Nodes' option do nothing
        curNodeOption = -1

        self.isRunning = True
        nodesMenu = DropdownBox(
            self.xLOffset, 40, 160, 40, pygame.Color(150, 150, 150), pygame.Color(100, 200, 255),
            pygame.font.SysFont("freesansbold", 30),
            ["Nodes", "Start node", "End node", "Auxiliary node", "Wall"])

        algorithmsMenu = DropdownBox(
            (160 + self.xLOffset), 40, 160, 40, pygame.Color(150, 150, 150), pygame.Color(100, 200, 255),
            pygame.font.SysFont("freesansbold", 30),
            ["Algorithms", "Dijkstra's", "A*"])

        visualiseButton = Button(
            (self.windowSize[0] - self.xLOffset - self.xROffset) // 2, 40, 160, 40, pygame.Color(150, 150, 150),
            pygame.Color(100, 200, 255),
            pygame.font.SysFont("freesansbold", 30), "Visualise")

        while self.isRunning:
            # Sets FPS to 60
            self.clock.tick(60)
            # Decreases the opacity for the rectangles by 50 for every tick
            self.fadeRectSurface.fill((0, 0, 0, 50))

            self.drawGrid()

            eventList = pygame.event.get()
            selectedNode = nodesMenu.update(eventList)
            if selectedNode >= 0:
                # Remembers the most recently pressed option for nodes
                curNodeOption = selectedNode
                potentialCollision = True
            selectedAlgorithm = algorithmsMenu.update(eventList)

            for event in eventList:
                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not potentialCollision:
                    pos = pygame.mouse.get_pos()
                    if self.checkMouseOnGrid(pos):
                        mouseIndex = self.mouseToIndex(pos)
                        self.placeNode(curNodeOption, mouseIndex)

            curPos = pygame.mouse.get_pos()
            curIndex = self.mouseToIndex(curPos)
            if self.checkMouseOnGrid(curPos):
                # Creates a yellow rectangle and increases the opacity by 50 for every tick
                self.drawRectOnHover(curIndex)

            # Draws rectangle surface to screen at 0, 0
            self.window.blits(((self.gridSurface, (0, 0)), (self.fadeRectSurface, (0, 0))))

            nodesMenu.draw(self.window)

            if selectedAlgorithm >= 0:
                pass

            algorithmsMenu.draw(self.window)
            visualiseButton.draw(self.window)
            # Updates all elements that aren't part of a surface
            potentialCollision = False
            pygame.display.update()

    def drawGrid(self) -> None:
        """drawGrid() draws a grid on the GUI in a way which allows the window size and offsets to be changed"""
        for i in range(self.xLOffset, self.windowSize[0] - self.xROffset, self.margin):
            for j in range(self.yTOffset, self.windowSize[1] - self.yBOffset, self.margin):
                node = pygame.Rect(i, j, self.margin, self.margin)
                pygame.draw.rect(self.gridSurface, (200, 200, 200), node, 1)

    def getGridEnds(self) -> [int, int]:
        """getGridEnds() performs a calculation which will get the x and y values of where the grid stops"""
        xEnd = math.ceil(
            ((self.windowSize[0] - self.xLOffset - self.xROffset) / self.margin)) * self.margin + self.xLOffset - 1
        yEnd = math.ceil(
            (self.windowSize[1] - self.yTOffset - self.yBOffset) / self.margin) * self.margin + self.yTOffset - 1
        return [xEnd, yEnd]

    def checkMouseOnGrid(self, pos: [int, int]) -> bool:
        """checkMouseOnGrid() evaluates the position given, checking if the values are between the grid start and end"""
        endValues = self.getGridEnds()
        if self.xLOffset <= pos[0] <= endValues[0]:
            if self.yTOffset <= pos[1] <= endValues[1]:
                return True
        return False

    def getGridSize(self) -> [int, int]:
        return self.mouseToIndex(self.getGridEnds())

    def mouseToIndex(self, pos: [int, int]) -> [int, int]:
        """mouseToIndex() converts a mouse position to the appropriate index for the grid/node array"""
        xIndex = math.floor((pos[0] - self.xLOffset) / self.margin)
        yIndex = math.floor((pos[1] - self.yTOffset) / self.margin)
        return [xIndex, yIndex]

    def drawRectOnHover(self, pos: [int, int]) -> None:
        """drawRectOnHover() takes in an x and y index position and draws a rectangle to highlight where the mouse is"""
        tmpRect = pygame.Rect(self.xLOffset + self.margin * pos[0], self.yTOffset + self.margin * pos[1], self.margin,
                              self.margin)
        pygame.draw.rect(self.fadeRectSurface, (255, 255, 255, 60), tmpRect, 3)

    def placeNode(self, nodeType: int, pos) -> None:
        rect = pygame.Rect(self.xLOffset + self.margin * pos[0], self.yTOffset + self.margin * pos[1], self.margin,
                           self.margin)
        if nodeType == -1:
            return

        nodes = self.nodeGraph.getNodes()
        if nodeType == 1:
            start = self.nodeGraph.findStart()
            if start:
                # Logically removes start
                startPos = start.getPosition()
                nodes[startPos[0]][startPos[1]].setType(-1)
                # Removes start from GUI
                blankRect = pygame.Rect(self.xLOffset + self.margin * startPos[0], self.yTOffset + self.margin *
                                        startPos[1], self.margin, self.margin)
                pygame.draw.rect(self.gridSurface, (0, 0, 0), blankRect, 0)
            nodes[pos[0]][pos[1]].setType(1)
            pygame.draw.rect(self.gridSurface, self.colours["0"], rect, 0)
            return
        elif nodeType == 2:
            end = self.nodeGraph.findEnd()
            if end:
                # Logically removes end
                endPos = end.getPosition()
                nodes[endPos[0]][endPos[1]].setType(-1)
                # Removes end from GUI
                blankRect = pygame.Rect(self.xLOffset + self.margin * endPos[0], self.yTOffset + self.margin *
                                        endPos[1], self.margin, self.margin)
                pygame.draw.rect(self.gridSurface, (0, 0, 0), blankRect, 0)
            nodes[pos[0]][pos[1]].setType(2)
            pygame.draw.rect(self.gridSurface, self.colours["1"], rect, 0)
            return

        pygame.draw.rect(self.gridSurface, self.colours[str(nodeType - 1)], rect, 0)


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, color: pygame.Color, highlight: pygame.Color, font: pygame.font,
                 text: str, ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.highlight = highlight
        self.font = font
        self.text = text

    def draw(self, surface: pygame.Surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(surface, self.highlight, (self.x, self.y, self.w, self.h))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
        text = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text,
                     (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))
        return False


class DropdownBox:
    def __init__(self, x: int, y: int, w: int, h: int, color: pygame.Color, highlight: pygame.Color,
                 font: pygame.font, optionList: [str], selected: int = 0) -> None:
        self.color = color
        self.highlight = highlight
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.optionList = optionList
        self.selected = selected
        self.drawMenu = False
        self.menuActive = False
        self.activeOption = -1

    def draw(self, surface: pygame.Surface) -> None:
        """draw() draws the dropdown menu"""
        pygame.draw.rect(surface, self.highlight if self.menuActive else self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.optionList[self.selected], 1, (0, 0, 0))
        surface.blit(msg, msg.get_rect(center=self.rect.center))

        if self.drawMenu:
            for i, text in enumerate(self.optionList):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surface, self.highlight if i == self.activeOption else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surface.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
                self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.optionList))
            pygame.draw.rect(surface, (0, 0, 0), outer_rect, 2)

    def update(self, event_list: [pygame.event]) -> int:
        """update() Handles logic for pressing an option in the dropdown menu"""
        curPos = pygame.mouse.get_pos()
        self.menuActive = self.rect.collidepoint(curPos)

        self.activeOption = -1
        for i in range(len(self.optionList)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(curPos):
                self.activeOption = i
                break

        if not self.menuActive and self.activeOption == -1:
            self.drawMenu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menuActive:
                    self.drawMenu = not self.drawMenu
                elif self.drawMenu and self.activeOption >= 1:
                    self.selected = self.activeOption
                    self.drawMenu = False
                    return self.activeOption
        return -1


z = PyGUI()
z.run()
