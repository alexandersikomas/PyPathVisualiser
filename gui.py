import pygame
import math
import json
from dijkstra import runDijkstra
from astar import runAStar
from graph import Graph

# GLOBAL VARIABLES
FREE_SANS_FONT = lambda size: pygame.font.SysFont("freesansbold", size)


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
            self.speed = settings['renderSpeed']['speed']
        self.caption = "PyPath Visualiser"
        self.isRunning = None
        self.window = pygame.display.set_mode(self.windowSize)
        self.fadeRectSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.gridSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.gridSurface = self.gridSurface.convert_alpha()
        self.fadeRectSurface = self.fadeRectSurface.convert_alpha()
        # Weight surface is made transparent
        self.weightSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.weightSurface = self.weightSurface.convert_alpha()
        self.pathSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.pathSurface = self.pathSurface.convert_alpha()
        self.textSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.textSurface = self.textSurface.convert_alpha()
        self.settingsSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.settingsSurface = self.settingsSurface.convert_alpha()
        self.settingsOpen = False
        self.clock = pygame.time.Clock()
        size = self.getGridSize()
        self.nodeGraph = Graph([size[0], size[1]])
        del size

    def run(self) -> None:
        """run() is the main loop of the GUI, it handles the events"""
        pygame.init()
        self.window.fill((0, 0, 0, 0))
        self.window.set_alpha(255)
        pygame.display.set_caption(self.caption)
        # Without this you could select an option that is over the grid and the grid would automatically place for you
        potentialCollision = False
        # This makes 'Nodes' option do nothing
        curNodeOption = -1
        self.isRunning = True
        ranVisualise = False

        # BUTTON DEFINITION START
        nodesMenu = DropdownBox(
            self.xLOffset, 40, 160, 40, pygame.Color(150, 150, 150), pygame.Color(100, 200, 255),
            FREE_SANS_FONT(30),
            ["Nodes", "Start node", "End node", "Auxiliary node", "Wall", "Eraser", "Weight"])

        algorithmsMenu = DropdownBox(
            (160 + self.xLOffset), 40, 160, 40, pygame.Color(150, 150, 150), pygame.Color(100, 200, 255),
            FREE_SANS_FONT(30),
            ["Algorithms", "Dijkstra's", "A*"])

        weightInput = InputBox((160 * 2 + self.xLOffset + 2), 42, 160, 36, 'Weight:')

        visualiseButton = Button(
            (self.windowSize[0] - self.xLOffset - self.xROffset) // 2, 40, 160, 40, pygame.Color(150, 150, 150),
            pygame.Color(100, 200, 255),
            FREE_SANS_FONT(30), "Visualise")


        clearButton = Button(self.windowSize[0] - self.xROffset - 160, 40, 160, 40, pygame.Color(150, 150, 150),
                             pygame.Color(100, 200, 255),
                             FREE_SANS_FONT(30), "Clear all")
        # BUTTON DEFINITION END

        while self.isRunning:
            # This is the main loop of the GUI, it handles the events
            # Sets FPS to 60
            self.clock.tick(60)
            # Decreases the opacity for the rectangles by 50 for every tick
            self.fadeRectSurface.fill((0, 0, 0, 50))

            self.drawGrid()

            eventList = pygame.event.get()
            selectedNode = nodesMenu.update(eventList)
            visualisePress = visualiseButton.update(eventList)
            if selectedNode >= 0:
                # Remembers the most recently pressed option for nodes
                curNodeOption = selectedNode
                potentialCollision = True

            selectedAlgorithm = algorithmsMenu.update(eventList)
            if selectedAlgorithm >= 0:
                curAlgorithm = selectedAlgorithm
                potentialCollision = True

            if visualisePress >= 0:
                try:
                    self.visualise(curAlgorithm)
                    ranVisualise = True
                except UnboundLocalError:
                    print("No algorithm selected")

            for event in eventList:
                weightInput.handleEvent(event)

                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not potentialCollision:
                    if ranVisualise:
                        ranVisualise = False
                        pygame.event.clear()
                    else:
                        pos = pygame.mouse.get_pos()
                        # Makes weight option not place node
                        if self.checkMouseOnGrid(pos):
                            pos = self.mouseToIndex(pos)
                            if curNodeOption <= 5:
                                self.placeNode(curNodeOption, pos)
                            elif curNodeOption == 6:
                                self.placeWeight(pos, weightCost=weightInput.value)

            curPos = pygame.mouse.get_pos()
            curIndex = self.mouseToIndex(curPos)
            if self.checkMouseOnGrid(curPos):
                # Creates a white rectangle around hovering node
                self.drawRectOnHover(curIndex)

            # Draws all surfaces at 0,0

            self.window.blit(self.pathSurface, (0, 0))
            self.window.blit(self.gridSurface, (0, 0))
            self.window.blit(self.fadeRectSurface, (0, 0))
            # Draw the self.weightSurface surface onto the screen
            self.window.blit(self.weightSurface, (0, 0))
            self.window.blit(self.settingsSurface, (0, 0))
            self.window.blit(self.textSurface, (0, 0))


            if clearButton.update(eventList) >= 0:
                self.clearGrid()

            nodesMenu.draw(self.window)
            weightInput.draw(self.window)
            algorithmsMenu.draw(self.window)
            visualiseButton.draw(self.window)
            clearButton.draw(self.window)

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
        """getGridSize() calculates the size of the grid, this is used to create the node graph"""
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
        pygame.draw.rect(self.fadeRectSurface, (255, 255, 255, 60), tmpRect, 1)

    def placeNode(self, nodeType: int, pos) -> None:
        """placeNode() takes in a node type and position and places a node of that type at that position"""

        rect = pygame.Rect(self.xLOffset + self.margin * pos[0], self.yTOffset + self.margin * pos[1], self.margin,
                           self.margin)
        if nodeType == -1:
            return

        nodes = self.nodeGraph.getNodes()
        # Sets the node to be walkable this is then changed to False if it is a wall
        nodes[pos[0]][pos[1]].setWalkable(True)
        if nodeType == 1:
            start = self.nodeGraph.findStart()
            # If start node is already placed, remove it
            if start:
                # Logically removes start
                startPos = start.getPosition()
                nodes[startPos[0]][startPos[1]].setType(-1)
                # Removes start from GUI
                blankRect = pygame.Rect(self.xLOffset + self.margin * startPos[0], self.yTOffset + self.margin *
                                        startPos[1], self.margin, self.margin)
                pygame.draw.rect(self.gridSurface, (0, 0, 0, 0), blankRect, 0)
        elif nodeType == 2:
            end = self.nodeGraph.findEnd()
            # If end node is already placed, remove it
            if end:
                # Logically removes end
                endPos = end.getPosition()
                nodes[endPos[0]][endPos[1]].setType(-1)
                # Removes end from GUI
                blankRect = pygame.Rect(self.xLOffset + self.margin * endPos[0], self.yTOffset + self.margin *
                                        endPos[1], self.margin, self.margin)
                # Set to (0,0,0,0) because otherwise if colour is (0,0,0) then the path drawn cannot draw
                # over this due to the alpha
                pygame.draw.rect(self.gridSurface, (0, 0, 0, 0), blankRect, 0)
        elif nodeType == 4:
            nodes[pos[0]][pos[1]].setWalkable(False)
        elif nodeType == 5:
            # Changes eraser nodeType to blank node
            nodeType = -1
        if nodes[pos[0]][pos[1]].getWeight() > 1:
            self.removeWeight(pos)
        # print(nodes[pos[0]][pos[1]].getType())
        if nodes[pos[0]][pos[1]].getType() <= 4:
            nodes[pos[0]][pos[1]].setType(nodeType)
            pygame.draw.rect(self.gridSurface, self.colours[str(nodeType)], rect, 0)


    def clearGrid(self) -> None:
        """clearGrid() clears the grid of all nodes and weights"""
        size = self.getGridSize()
        self.nodeGraph = Graph([size[0], size[1]])
        self.gridSurface.fill((0, 0, 0, 0))
        self.weightSurface.fill((0, 0, 0, 0))
        self.pathSurface = pygame.Surface(self.windowSize, pygame.SRCALPHA, 32)
        self.pathSurface = self.weightSurface.convert_alpha()

    def placeWeight(self, pos: [int, int], weightCost: int = 1) -> None:
        """placeWeight() takes in a mouse index and places a weight node at that position"""
        self.removeWeight(pos)
        rect = pygame.Rect(self.xLOffset + self.margin * pos[0],
                           self.yTOffset + self.margin * pos[1] + self.margin // 4, self.margin,
                           self.margin)
        font = FREE_SANS_FONT(17)

        nodes = self.nodeGraph.getNodes()
        # Check to make sure node is 'air' node otherwise don't place weight
        if nodes[pos[0]][pos[1]].getType() == -1:
            textSurface = font.render(str(weightCost), True, (255, 255, 255))
            # Weight greater than 999 is unreadable, so it isn't rendered but it is added logically
            if weightCost < 1000:
                self.weightSurface.blit(textSurface, rect)

            nodes[pos[0]][pos[1]].setWeight(weightCost)

    def removeWeight(self, pos):
        """removeWeight() takes in a position and removes the weight at that position"""
        rect = pygame.Rect(self.xLOffset + self.margin * pos[0], self.yTOffset + self.margin * pos[1], self.margin,
                           self.margin)
        nodes = self.nodeGraph.getNodes()
        nodes[pos[0]][pos[1]].setWeight(1)
        self.weightSurface.fill((0, 0, 0, 0), rect)

    def visualise(self, selectedAlgorithm):
        """visualise() takes in a selected algorithm and visualises the pathfinding process"""
        self.pathSurface.fill((0, 0, 0, 0))

        start = self.nodeGraph.findStart()
        end = self.nodeGraph.findEnd()
        auxiliaries = self.nodeGraph.findAuxiliaries()
        # The algorithms change the distances of the nodes, so the distances need to be reset
        tmp = self.nodeGraph
        if selectedAlgorithm == 1:
            nodes, totalDistance, closedList = runDijkstra(start, end, auxiliaries, self.nodeGraph)
        elif selectedAlgorithm == 2:
            nodes, totalDistance, closedList = runAStar(start, end, auxiliaries, self.nodeGraph)

        self.nodeGraph = tmp

        speedFunction = lambda x: 1 if x == 10 else 100 if x == 1 else (10 - x) * 9 + 1
        for node in closedList[1::]:
            # Draws the blue explored nodes
            self.placePath(node.getPosition(), True)
            self.window.blit(self.pathSurface, (0, 0))
            self.window.blit(self.gridSurface, (0, 0))
            pygame.time.wait(speedFunction(self.speed))
            pygame.display.flip()
            pygame.display.update()
            pygame.event.clear(pump=True)

        for node in nodes[0:-1]:
            # Draws the yellow path nodes
            self.placePath(node.getPosition())
        if totalDistance > 0:
            self.textSurface.fill((0, 0, 0, 0))
            outputText = FREE_SANS_FONT(30)
            efficiencyText = outputText.render(f'Calculations: {len(closedList)}', True, 'white', None)
            distanceText = outputText.render(f'Distance: {totalDistance}', True, 'white', None)
            self.textSurface.blit(efficiencyText,
                                  pygame.Rect(int(self.margin * 2.5), self.windowSize[1] - (2 * self.margin), 20, 20))
            self.textSurface.blit(distanceText,
                                  pygame.Rect(self.windowSize[0] - int(self.margin * 10),
                                              self.windowSize[1] - (2 * self.margin), 20, 20))
        else:
            print("No path found")

    def placePath(self, pos: [int, int], closed=False) -> None:
        """placePath() takes in a list of nodes and places a path between them"""
        rect = pygame.Rect(self.xLOffset + self.margin * pos[0], self.yTOffset + self.margin * pos[1], self.margin,
                           self.margin)
        if closed:
            colour = self.colours["5"]
        else:
            colour = self.colours["6"]

        pygame.draw.rect(self.pathSurface, colour, rect, 0)



class Button:
    def __init__(self, x: int, y: int, w: int, h: int, color: pygame.Color, highlight: pygame.Color, font: pygame.font,
                 text: str, ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.highlight = highlight
        self.font = font
        self.text = text

    def draw(self, surface: pygame.Surface) -> bool:
        """draw() draws the button to the surface given"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(surface, self.highlight, self.rect)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
        text = self.font.render(self.text, True, (0, 0, 0, 0))
        surface.blit(text,
                     (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))
        return False

    def update(self, event_list: [pygame.event]) -> int:
        """update() updates the dropdown box based on the events"""
        curPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(curPos):
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 1
        return -1


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
        """draw() draws the dropdown box to the surface given"""
        # Draw the box
        pygame.draw.rect(surface, self.highlight if self.menuActive else self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0, 0), self.rect, 2)
        msg = self.font.render(self.optionList[self.selected], 1, (0, 0, 0, 0))
        surface.blit(msg, msg.get_rect(center=self.rect.center))

        # Draw the menu
        if self.drawMenu:
            for i, text in enumerate(self.optionList):
                # Create a new rect for each option
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surface, self.highlight if i == self.activeOption else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0, 0))
                surface.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
                self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.optionList))
            pygame.draw.rect(surface, (0, 0, 0, 0), outer_rect, 2)

    def update(self, event_list: [pygame.event]) -> int:
        """update() updates the dropdown box based on the events"""
        curPos = pygame.mouse.get_pos()
        self.menuActive = self.rect.collidepoint(curPos)

        self.activeOption = -1
        # Check if the mouse is hovering over an option sets it as activeOption for highlighting
        for i in range(len(self.optionList)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(curPos):
                self.activeOption = i
                break

        if not self.menuActive and self.activeOption == -1:
            self.drawMenu = False

        # Check for events
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menuActive:
                    self.drawMenu = not self.drawMenu
                # Makes the top option unselectable
                elif self.drawMenu and self.activeOption >= 1:
                    self.selected = self.activeOption
                    self.drawMenu = False
                    return self.activeOption
        return -1


class InputBox:
    def __init__(self, x, y, width, height, placeholder=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = FREE_SANS_FONT(30)
        self.placeholder = placeholder
        self.text = self.placeholder
        self.value = 1

    def draw(self, screen):
        # Draw the input box background
        pygame.draw.rect(screen, (150, 150, 150), self.rect)

        # Render the text in the input box
        text_surface = self.font.render(self.text, True, (0, 0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if self.text == self.placeholder:
                self.text = ''
            if event.key == pygame.K_BACKSPACE:
                # Handle backspace key
                self.text = self.text[:-1]
            else:
                # Add character to input box
                self.text += event.unicode
            self.handleInput(self.text)

    def handleInput(self, text):
        try:
            self.value = int(text)
        except ValueError:
            self.value = 1
            self.text = ""
        if self.value > 999:
            self.value = 999
            self.text = "999"


z = PyGUI()
z.run()
