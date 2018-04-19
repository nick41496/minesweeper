import random

class Cell:
    def __init__(self):
        self.isVisible = False 
        self.value = 0
        self.isFlagged = False 

    def __str__(self):
        if self.isFlagged:
            return '🚩'
        elif self.isVisible:
            if self.value == -1:
                return '💣'
            if self.value == 0:
                return ' '
            else:
                return str(self.value)
        else:
            return '*'

class Game:
    WIDTH = 10
    HEIGHT = 10
    MINES = 10

    SURROUNDING_ARRAY = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self):
        self.board = [[Cell() for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        self.flagged = 0

        self.initializeBoard()

    def printHelp(self):
        print("To play, enter one of the following commands, followed by x,y-coordinates:")
        print("\to[pen] - opens the given node, revealing it")
        print("\tf[lag] - flags the given node, marking it as a (potential) mine")
        print("\tu[nflag] - unflags the given node, removing a flag")
        print("\tq[uit] - quits the game")
        print("\thelp - shows this help")
        print("")

    def printWelcome(self):
        print("Welcome to Minesweeper!")
        self.printHelp()

    def printStatus(self):
        print()
        print('{0} flagged / {1} mines'.format(self.flagged, self.MINES))
        print()

    def printBoard(self):
        print('', end='  ')
        for i in range(self.WIDTH):
            print(i % 10, end='  ')
        print('')
        for i in range(self.WIDTH):
            print('___', end='')
        print('')
        for i in range(self.HEIGHT):
            print('{0}|'.format(i % 10), end='')
            for j in range(self.WIDTH):
                print('{0}'.format(self.board[i][j]), end='  ')
            print('')

    def printDebug(self):
        print('', end='  ')
        for i in range(self.WIDTH):
            print(i % 10, end='  ')
        print('')
        for i in range(self.WIDTH):
            print('___', end='')
        print('')
        for i in range(self.HEIGHT):
            print('{0}|'.format(i % 10), end='')
            for j in range(self.WIDTH):
                cell = self.board[i][j]
                cell.isVisible = True
                print('{0}'.format(cell), end='  ')
                cell.isVisible = False
            print('')

    def isWon(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                cell = self.board[i][j]
                if cell.value >= 0 and not cell.isVisible:
                    return False
        
        return True

    def setMines(self):
        mines = 0

        while mines < self.MINES:
            x = random.randint(0, self.WIDTH - 1)
            y = random.randint(0, self.HEIGHT - 1)
            cell = self.board[y][x]
            if cell.value != -1:
                cell.value = -1
                mines += 1

    def setCellValue(self, x, y):
        cell = self.board[y][x]
        if cell.value != -1:
            mines = 0
            for dx, dy in self.SURROUNDING_ARRAY:
                newx = x + dx
                newy = y + dy
                if 0 <= newx < self.WIDTH and 0 <= newy < self.HEIGHT and self.board[newy][newx].value == -1:
                    mines += 1

            cell.value = mines

    def initializeBoard(self):
        self.setMines()

        # set all the values
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.setCellValue(x, y)
 
    def clearFlags(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.board[y][x].isFlagged = False

    def openCellsAround(self, x, y):
        surrounding_cells = []
        visited_cells = [(x, y)]
        for dx, dy in self.SURROUNDING_ARRAY:
            newx = x + dx
            newy = y + dy
            if 0 <= newx < self.WIDTH and 0 <= newy < self.HEIGHT:
                surrounding_cells.append((newx, newy))

        while surrounding_cells:
            u, v = surrounding_cells.pop()
            cell = self.board[v][u]
            visited_cells.append((u, v))
            if not cell.isFlagged:
                cell.isVisible = True

            if cell.value == 0:
                for du, dv in self.SURROUNDING_ARRAY:
                    newu = u + du
                    newv = v + dv
                    if 0 <= newu < self.WIDTH and 0 <= newv < self.HEIGHT:
                        newcell = (newu, newv)
                        if newcell not in surrounding_cells and newcell not in visited_cells:
                            surrounding_cells.append(newcell)

        return 0

    def processCommand(self, command, x, y):
        if "open".startswith(command.lower()):
            cell = self.board[y][x]
            if cell.isVisible:
                return cell.value

            cell.isVisible = True
            if cell.value == 0:
                return self.openCellsAround(x, y)
            else:
                return cell.value
        elif "flag".startswith(command.lower()):
            cell = self.board[y][x]
            if not cell.isVisible:
                self.flagged += 1
                cell.isFlagged = True
            return 0
        elif "unflag".startswith(command.lower()):
            cell = self.board[y][x]
            if cell.isFlagged:
                self.flagged -= 1
                cell.isFlagged = False
            return 0
        elif "quit".startswith(command.lower()):
            return -1
        else:
            game.printHelp()

game = Game()

game.printWelcome()
game.printBoard()

while not game.isWon():
    full_command = input("> ").split()
    try:
        command = full_command[0]
        if len(full_command) > 1:
            x = int(full_command[1]) 
            y = int(full_command[2])
        else:
            x = 0
            y = 0
        result = game.processCommand(command, x, y)
        if result == -1:
            game.printBoard()
            print("Thanks for playing!")
            break;
        else:
            game.printStatus()
            game.printBoard()
    except Exception as e:
        game.printHelp()

if game.isWon():
    game.clearFlags()
    game.printDebug()
    print("Congratulations! You won!")
