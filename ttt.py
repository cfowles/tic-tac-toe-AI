'''
Chris Fowles - AI - Tic Tac Toe
Plays a game of tic tac toe, with the human going first as 'X's and the computer going second with 'O's.
The computer uses minimax & should never lose - only win or draw.

Resources:

tkinter for GUI:
I used these for learning to program the user interface, I also googled a lot for how to change text and what not.
http://tkinter.unpythonic.net/wiki/
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html

minimax:
http://web.cs.wpi.edu/~rich/courses/imgd4000-d10/lectures/E-MiniMax.pdf
'''

from Tkinter import *
from tkFont import Font
from copy import deepcopy


'''
Board Class has 'player' 'opponent'
It keeps track of the squares, and takes care of the minimax logic.
'''
class Board:
    '''
    Initialize the board.
    '''
    def __init__(self, other=None):
        self.player = 'X'
        self.opponent = 'O'
        self.empty = '-'
        self.size = 3
        self.squares = {}
        for y in range(self.size):
            for x in range(self.size):
                self.squares[x, y] = self.empty
        #Copy
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    '''
    Make a new move - called from the GUI at move()
    '''
    def makeMove(self, x, y):
        #create board
        board = Board(self)
        #place correct X or O
        board.squares[x, y] = board.player
        (board.player, board.opponent) = (board.opponent, board.player)
        return board

    '''
    The magic: looks at terminal states & then returns utility value.
    '''
    def minimax(self, player):
        # Terminal State - WON
        if self.won():
            if player:
                return (-1, None)
            else:
                return (+1, None)
        #Terminal State - TIED
        elif self.tied():
            return (0, None)
        #For Max Node
        elif player:
            max = (-2, None)
            for x, y in self.squares:
                if self.squares[x, y] == self.empty:
                    #look at moves for other player.
                    invPlayer = not player
                    value = self.makeMove(x, y).minimax(invPlayer)[0]
                    #set
                    if value > max[0]:
                        max = (value, (x, y))
            return max
        #For Min Node
        else:
            min = (+2, None)
            #for dictionary - makemove
            for x, y in self.squares:
                if self.squares[x, y] == self.empty:
                    #look at other player
                    invPlayer = not player
                    value = self.makeMove(x, y).minimax(invPlayer)[0]
                    if value < min[0]:
                        min = (value, (x, y))
            return min

    '''
    Helper for minimax
    '''
    def best(self):
        return self.minimax(True)[1]

    '''
    Tie game? Checks if all fields are filled or not.
    '''
    def tied(self):
        for (x, y) in self.squares:
            if self.squares[x, y] == self.empty:
                return False
        return True

    '''
    Is there a winner? Checks h, v, and both diagonals.
    '''
    def won(self):
        # Check Horizontal
        for y in range(self.size):
            winning = []
            for x in range(self.size):
                if self.squares[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # Check Vertical
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.squares[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # Check Diagonal1
        winning = []
        for y in range(self.size):
            x = y
            if self.squares[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # Check Diagonal2
        winning = []
        for y in range(self.size):
            x = self.size - 1 - y
            if self.squares[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # If no winner return 'None'
        else:
            return None


'''
GUI using tkinter.
'''
class GUI:

    '''
    Initialize the game board.
    '''
    def __init__(self):
        # Create the app
        self.app = Tk()
        self.app.title('AI#6 - TTT')
        self.app.resizable(width=True, height=True)
        #create board
        self.board = Board()
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}
        self.text = Label(self.app, width=40, height=10, font=self.font, text='GAME ONGOING')
        #SET THE CURSOR TO PIRATE - (most important step!)
        self.app.config(cursor="pirate")
        #Create all of our buttons - cmd listens and sets button field.
        for x, y in self.board.squares:
            cmd = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=cmd, font=self.font, width=2, height=1)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button
        cmd = lambda: self.reset()
        button = Button(self.app, text='Start Over!', command=cmd)
        button.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky="WE")
        self.text.grid(row=self.board.size + 2, column=0, columnspan=self.board.size, sticky="WE")
        self.updateBoard()

    '''
    Reset the ticTacToe board, so that it is reinitialized & then updated
    '''
    def reset(self):
        self.board = Board()
        self.updateBoard()

    '''
    Moves - calls makeMove in Board Class.
    '''
    def move(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.makeMove(x, y)
        self.updateBoard()
        move = self.board.best()
        if move:
            self.board = self.board.makeMove(*move)
            self.updateBoard()
        self.app.config(cursor="pirate")

    '''
    Update the game board.
    '''
    def updateBoard(self):
        # For each square
        for (x, y) in self.board.squares:
            text = self.board.squares[x, y]
            self.buttons[x, y]['text'] = text
            #self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.board.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                #If square has been played we disable it
                self.buttons[x, y]['state'] = 'disabled'
        winning = self.board.won()
        tie = self.board.tied()
        #Someone wins
        if winning:
            self.text['text'] = 'The Computer Won!'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        #There is a draw
        if tie:
            self.text['text'] = 'It was a draw /:'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        #update
        for (x, y) in self.board.squares:
            self.buttons[x, y].update()

    '''
    Loop while playing - can either reset the game or exit to quit.
    '''
    def mainloop(self):
        # loop indefinitely while playing.
        self.app.mainloop()

'''
Main method - simply starts mainloop in gui.
'''
if __name__ == '__main__':
    print "Game Started."
    GUI().mainloop()