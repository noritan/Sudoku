import tkinter

TILE_WIDTH = 30
TILE_HEIGHT = 30
TILE_FONT = ("monospace", 24)
TILE_GAP = 2
TILE_GROUP = 3
TILE_LENGTH = TILE_GROUP * TILE_GROUP
TILE_AVAILABLE = frozenset({i+1 for i in range(TILE_LENGTH)})
CANVAS_WIDTH = TILE_WIDTH * TILE_LENGTH + TILE_GAP
CANVAS_HEIGHT = TILE_HEIGHT * TILE_LENGTH + TILE_GAP
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CANVAS_X = (WINDOW_WIDTH - CANVAS_WIDTH) / 2
CANVAS_Y = 30

# square class
class Square:
    # constructor
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.status = "free"
        self.number = [] # unassigned
    
    # Assign a number to the Square
    def assign(self, number, status="assigned"):
        assert(number in TILE_AVAILABLE)
        self.number = number
        self.status = status

    # Unassign number of the Square
    def unassign(self):
        self.status = "free"

    # Draw a Square in a color
    def drawInColor(self, color):
        canvas.create_text(
            (self.col + 0.5) * TILE_WIDTH,
            (self.row + 0.5) * TILE_HEIGHT,
            text=str(self.number),
            fill=color,
            font=TILE_FONT,
            tag="square"
        )

    # Draw a Square
    def draw(self):
        if self.status == "fixed":
            self.drawInColor("red")
        elif self.status == "assigned":
            self.drawInColor("blue")

# Draw Board
def drawBoard(board):
    canvas.delete("square")
    for row in range(TILE_LENGTH):
        for col in range(TILE_LENGTH):
            board[row][col].draw()

# Create initial board
def initialBoard():
    board = [[]]*TILE_LENGTH
    for row in range(TILE_LENGTH):
        line = [0]*TILE_LENGTH
        for col in range(TILE_LENGTH):
            line[col] = Square(col, row)
        board[row] = line
    return board

# Initialize with example board
def exampleBoard():
    x = -1
    Q1 = [
        x,x,x,3,x,4,x,x,x,
        x,x,x,x,7,x,9,x,x,
        x,x,x,x,x,1,x,8,x,
        1,x,x,x,x,x,4,x,7,
        x,9,x,x,6,x,x,2,x,
        4,x,5,x,x,x,x,x,6,
        x,6,x,2,x,x,x,x,x,
        x,x,7,x,4,x,x,x,x,
        x,x,x,8,x,3,x,x,x
    ]
    Q2 = [
        x,x,6,x,x,x,5,x,x,
        x,x,x,5,x,7,x,x,x,
        2,x,x,x,x,x,x,x,8,
        x,4,x,x,6,x,x,7,x,
        x,x,3,8,x,5,6,x,x,
        x,9,x,x,3,x,x,8,x,
        1,x,x,x,x,x,x,x,2,
        x,x,x,2,x,4,x,x,x,
        x,x,4,x,x,x,1,x,x
    ]
    Q98 = [
        x,x,x,x,x,9,x,x,4,
        x,x,x,x,1,x,x,3,x,
        x,x,x,2,x,8,x,x,7,
        3,x,2,x,x,x,6,x,x,
        x,6,x,x,x,x,x,9,x,
        x,x,4,x,x,x,1,x,8,
        5,x,x,6,x,1,x,x,x,
        x,4,x,x,5,x,x,x,x,
        7,x,x,3,x,x,x,x,x
    ]
    Q100 = [
        x,3,x,x,5,x,x,6,x,
        7,x,x,1,x,x,x,x,8,
        x,x,2,x,x,x,x,x,x,
        x,9,x,x,x,8,4,x,x,
        x,4,x,x,x,x,x,1,x,
        x,x,6,7,x,x,x,2,x,
        x,x,x,x,x,x,3,x,x,
        5,x,x,x,x,4,x,x,6,
        x,6,x,x,9,x,x,5,x
    ]
    Qbaka = [
        x,x,5,3,x,x,x,x,x,
        x,x,x,x,x,x,x,x,x,
        x,x,x,x,1,x,5,x,x,
        4,x,x,x,x,5,3,x,x,
        x,x,x,x,x,x,x,x,x,
        x,x,3,2,x,x,x,8,x,
        x,6,x,x,x,x,x,x,9,
        x,x,x,x,x,x,x,x,x,
        x,x,x,x,x,9,7,x,x
    ]
    Qhard = [
        x,x,5,3,x,x,x,x,x,
        8,x,x,x,x,x,x,2,x,
        x,7,x,x,1,x,5,x,x,
        4,x,x,x,x,5,3,x,x,
        x,1,x,x,7,x,x,x,6,
        x,x,3,2,x,x,x,8,x,
        x,6,x,5,x,x,x,x,9,
        x,x,4,x,x,x,x,3,x,
        x,x,x,x,x,9,7,x,x
    ]
    board = initialBoard()
    q = Q98
    for i in range(len(q)):
        if q[i] != x:
            row = int(i/TILE_LENGTH)
            col = i % TILE_LENGTH
            board[row][col].assign(q[i], "fixed")
    return board

# Create a window
root = tkinter.Tk()
root.title("Sudoku")
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

# Create a canvas
canvas = tkinter.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=CANVAS_X, y=CANVAS_Y)
canvas.create_rectangle(
    0,
    0,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    fill="gray80",
    width=0,
    tag="board"
)

# Gray border lines
c = "gray"
for i in range(TILE_LENGTH + 1) :
    x = TILE_WIDTH * i + TILE_GAP * 0.5
    canvas.create_line(
        x, 0,
        x, CANVAS_HEIGHT,
        fill=c,
        width=TILE_GAP,
        tag="board"
    )
    y = TILE_HEIGHT * i + TILE_GAP * 0.5
    canvas.create_line(
        0, y,
        CANVAS_WIDTH, y,
        fill=c,
        width=TILE_GAP,
        tag="board"
    )
# Black border lines
c = "black"
for i in range(0, TILE_LENGTH + 1, TILE_GROUP) :
    x = TILE_WIDTH * i + TILE_GAP * 0.5
    canvas.create_line(
        x, 0,
        x, CANVAS_HEIGHT,
        fill=c,
        width=TILE_GAP,
        tag="board"
    )
    y = TILE_HEIGHT * i + TILE_GAP * 0.5
    canvas.create_line(
        0, y,
        CANVAS_WIDTH, y,
        fill=c,
        width=TILE_GAP,
        tag="board"
    )

# Solve button
solveButton = tkinter.Button(root, text="SOLVE")
solveButton.place(x=WINDOW_WIDTH/2, y=CANVAS_Y*2+CANVAS_HEIGHT)

# Callback from canvas
def canvasOnClick(event):
    x = event.x + TILE_GAP
    y = event.y + TILE_GAP

    col = int(x / TILE_WIDTH)
    x_frac = x % TILE_WIDTH
    row = int(y / TILE_HEIGHT)
    y_frac = y % TILE_HEIGHT
    if (col < 0 or col >= TILE_LENGTH or row < 0 or row >= TILE_LENGTH):
        return
    if x_frac < TILE_GAP * 3 or y_frac < TILE_GAP * 3:
        print("Farc %d, %d" % (x_frac, y_frac))
        return
    print("Clicked %d, %d" % (col, row))

canvas.bind("<Button-1>", canvasOnClick)

# add negative flag in a group
def addNegative(square):
    global groups
    square.negative = set(TILE_AVAILABLE)
    for group in groups:
        if square in group:
            for member in group:
                member.negative.add(square.number)

# Solver function
def solve():
    # Serial square list
    allSquare = []
    for line in board:
        for square in line:
            allSquare.append(square)
    # Construct group structure
    global groups
    groups = []
    # row group
    for col in range(TILE_LENGTH):
        group = []
        for row in range(TILE_LENGTH):
            group.append(board[row][col])
        groups.append(list(group))
    # column group
    for row in range(TILE_LENGTH):
        group = []
        for col in range(TILE_LENGTH):
            group.append(board[row][col])
        groups.append(group)
    # sector group
    for cbase in range(0, TILE_LENGTH, TILE_GROUP):
        for rbase in range(0, TILE_LENGTH, TILE_GROUP):
            group = []
            for col in range(cbase,cbase+TILE_GROUP):
                for row in range(rbase,rbase+TILE_GROUP):
                    group.append(board[row][col])
            groups.append(group)
    # Clear all negative set
    for square in allSquare:
        square.negative = set()
    # initialize negative set
    for square in allSquare:
        if square.status == "fixed":
            square.negative = set(TILE_AVAILABLE)
            addNegative(square)
        elif square.status == "assigned":
            square.negative = set(TILE_AVAILABLE)
            addNegative(square)
    # 
    solved = False  # Flag indicating solver completion
    while not solved:
        solved = True
        # assign number to last positive
        for square in allSquare:
            if len(square.negative) == TILE_LENGTH - 1:
                square.assign((set(TILE_AVAILABLE) - square.negative).pop())
                print("Last positive %d at (%d,%d)" % (square.number, square.col, square.row))
                addNegative(square)
                solved = False
        # scan last positive in a group
        for number in TILE_AVAILABLE:
            for group in groups:
                nNegative = 0
                for square in group:
                    if number in square.negative:
                        nNegative = nNegative + 1
                if nNegative == TILE_LENGTH - 1:
                    for square in group:
                        if not (number in square.negative):
                            square.assign(number)
                            print("Last in group %d at (%d,%d)" % (square.number, square.col, square.row))
                            addNegative(square)
                            solved = False
    # Solved or no other solutions
    print("SOLVED")

# Callback from SOLVE button
def solveButtonOnClick():
    solve()
    drawBoard(board)
    root.update()

solveButton["command"]=solveButtonOnClick

# Create an example board
board = exampleBoard()

# Draw the board
drawBoard(board)

# the main loop
root.mainloop()

print("Done")
