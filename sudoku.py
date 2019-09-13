import tkinter

TILE_WIDTH = 36
TILE_HEIGHT = 36
TILE_FONT = ("monospace", 28)
TILE_GAP = 2
TILE_UNIT = 3
TILE_LENGTH = TILE_UNIT * TILE_UNIT
TILE_AVAILABLE = frozenset({i+1 for i in range(TILE_LENGTH)})
CANVAS_WIDTH = TILE_WIDTH * TILE_LENGTH + TILE_GAP
CANVAS_HEIGHT = TILE_HEIGHT * TILE_LENGTH + TILE_GAP
PAD = 20

# square class
class Square:
    # constructor
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.unassign()
        self.resetNegative()
    
    # Assign a number to the Square
    def assign(self, number, status="assigned"):
        assert(number in TILE_AVAILABLE)
        self.number = number
        self.status = status

    # Unassign number of the Square
    def unassign(self):
        self.status = "free"
        self.number = None

    # Draw the number in a Square with a color
    def drawInColor(self, canvas, color):
        canvas.create_text(
            (self.col + 0.5) * TILE_WIDTH,
            (self.row + 0.5) * TILE_HEIGHT,
            text=str(self.number),
            fill=color,
            font=TILE_FONT,
            tag="square"
        )

    # Fill the Square with a color
    def fillInColor(self, canvas, color):
        canvas.create_rectangle(
            (self.col + 0.1) * TILE_WIDTH,
            (self.row + 0.1) * TILE_HEIGHT,
            (self.col + 0.9) * TILE_WIDTH,
            (self.row + 0.9) * TILE_WIDTH,
            fill=color,
            width=0,
            tag="square"
        )

    SQUARE_COLOR = [
        "#5533FF",
        "#5533CC",
        "#553399",
        "#553366",
        "#553355",
        "#663333",
        "#993333",
        "#CC3333",
        "#FF3355",
        "#000000"
    ]

    # Draw a Square
    def draw(self, canvas):
        if self.status == "fixed":
            self.drawInColor(canvas, "red")
        elif self.status == "assigned":
            self.drawInColor(canvas, "blue")
        else:
            nNegative = len(self.negative())
            self.fillInColor(canvas, Square.SQUARE_COLOR[nNegative])

    # Reset negative set
    def resetNegative(self):
        self.f_negative = set()
    
    def addNegative(self, number):
        self.f_negative.add(number)

    def negative(self):
        return self.f_negative

# cluster class
class Cluster:
    #constructor
    def __init__(self):
        self.f_squareList = list()
        self.linearGroup = None
        self.bulkGroup = None

    # append a Square to this Cluster
    def append(self, square):
        self.f_squareList.append(square)

    # a set of elements never contained in this Cluster
    def negative(self):
        negSet = set(TILE_AVAILABLE)
        for square in self.squareList():
            negSet &= square.negative()
        return negSet
    
    # add a number to the negative of cluster member
    def addNegative(self, number):
        for square in self.squareList():
            square.addNegative(number)
    
    # a list of Square in this Cluster
    def squareList(self):
        for square in self.f_squareList:
            yield square
    
    def groupList(self):
        yield self.linearGroup
        yield self.bulkGroup

class Group:
    #constructor
    def __init__(self):
        self.f_clusterList = list()

    # append a Cluster to this Group    
    def append(self, cluster):
        self.f_clusterList.append(cluster)

    # add a number to the negative of cluster member
    def addNegative(self, number):
        for cluster in self.clusterList():
            cluster.addNegative(number)
    
    # the list of Cluster in this Group
    def clusterList(self):
        for cluster in self.f_clusterList:
            yield cluster

    # the list of Square in this Group
    def squareList(self):
        for cluster in self.clusterList():
            for square in cluster.squareList():
                yield square

# board class
class Board:
    # constructor
    def __init__(self, unit):
        self.unit = unit
        # define board length
        self.length = unit * unit
        # Fill Square on board
        self.f_squareList = list()
        for row in range(self.length):
            for col in range(self.length):
                self.f_squareList.append(Square(col, row))
        # Construct horizontal cluster
        self.hClusterList = list()
        for row in range(self.length):
            for cbase in range(0, self.length, self.unit):
                cluster = Cluster()
                for col in range(cbase, cbase + self.unit):
                    cluster.append(self.square(col, row))
                self.hClusterList.append(cluster)
                for square in cluster.squareList():
                    square.hcluster = cluster
        # Construct vertial cluster
        self.vClusterList = list()
        for col in range(self.length):
            for rbase in range(0, self.length, self.unit):
                cluster = Cluster()
                for row in range(rbase, rbase + self.unit):
                    cluster.append(self.square(col, row))
                self.vClusterList.append(cluster)
                for square in cluster.squareList():
                    square.vcluster = cluster
        # Construct groupList
        self.hGroupList = list()
        for row in range(self.length):
            group = Group()
            for col in range(self.unit):
                group.append(self.hClusterList[row * self.unit + col])
            self.hGroupList.append(group)
            for cluster in group.clusterList():
                cluster.linearGroup = group
        for rbase in range(0, self.length, self.unit):
            for col in range(self.unit):
                group = Group()
                for row in range(rbase, rbase + self.unit):
                    group.append(self.hClusterList[row * self.unit + col])
                self.hGroupList.append(group)
                for cluster in group.clusterList():
                    cluster.bulkGroup = group
        self.vGroupList = list()
        for col in range(self.length):
            group = Group()
            for row in range(self.unit):
                group.append(self.vClusterList[col * self.unit + row])
            self.vGroupList.append(group)
            for cluster in group.clusterList():
                cluster.linearGroup = group
        for cbase in range(0, self.length, self.unit):
            for row in range(self.unit):
                group = Group()
                for col in range(cbase, cbase + self.unit):
                    group.append(self.vClusterList[col * self.unit + row])
                self.vGroupList.append(group)
                for cluster in group.clusterList():
                    cluster.bulkGroup = group

    # return a Square on the board
    def square(self, col, row):
        return self.f_squareList[row*self.length+col]

    def squareAt(self, position):
        (col, row) = position
        return self.square(col, row)

    # return a serial list of Square
    def squareList(self):
        for square in self.f_squareList:
            yield square

    # draw the board on the canvas
    def draw(self, canvas):
        canvas.delete("square")
        for row in range(self.length):
            for col in range(self.length):
                self.square(col, row).draw(canvas)
    
    # return combined Group list
    def groupList(self):
        for group in self.hGroupList:
            yield group
        for group in self.vGroupList:
            yield group

    # return combined Cluster list
    def clusterList(self):
        for cluster in self.hClusterList:
            yield cluster
        for cluster in self.vClusterList:
            yield cluster

    def resetNegative(self):
        for square in self.squareList():
            square.resetNegative()

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
    Q130 = [
        x,1,x,6,x,x,x,5,x,
        7,2,x,x,x,x,x,x,9,
        x,x,x,x,x,8,x,x,x,
        3,x,x,x,1,x,6,x,x,
        x,x,x,2,x,9,x,x,x,
        x,x,5,x,4,x,x,x,8,
        x,x,x,1,x,x,x,x,x,
        5,x,x,x,x,x,x,3,2,
        x,9,x,x,x,5,x,1,x
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
    board = Board(TILE_UNIT)
    q = Qhard
    for i in range(len(q)):
        if q[i] != x:
            row = int(i/TILE_LENGTH)
            col = i % TILE_LENGTH
            board.square(col, row).assign(q[i], "fixed")
    return board

# Create a window
root = tkinter.Tk()
root.title("Sudoku")
root.option_add("*font", ["メイリオ", 14])

# Frame in the root
frame=tkinter.Frame()

# Create a canvas
canvas = tkinter.Canvas(frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=0, highlightthickness=0, relief="ridge")
canvas.grid(row=0, column=0, columnspan=2, padx=PAD, pady=PAD)
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
for i in range(0, TILE_LENGTH + 1, TILE_UNIT):
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
solveButton = tkinter.Button(frame, text="SOLVE")
solveButton.grid(row=1, column=0, padx=PAD, pady=PAD)
clearButton = tkinter.Button(frame, text="CLEAR")
clearButton.grid(row=1, column=1, padx=PAD, pady=PAD)

# Assign field and button
assignEntry = tkinter.Entry(frame, width=2)
assignEntry.grid(row=2, column=0, padx=PAD, pady=PAD)
assignButton = tkinter.Button(frame, text="ASSIGN")
assignButton.grid(row=2, column=1, padx=PAD, pady=PAD)

frame.pack()

# Callback from canvas
def canvasOnClick(event):
    global pivot
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
        pivot = None
        return
    print("Clicked (%d, %d) %s" % (col, row, board.square(col,row).negative()))
    setPivot(col, row)
    

canvas.bind("<Button-1>", canvasOnClick)

def setPivot(col, row):
    global pivot
    pivot = (col, row)
    square = board.squareAt(pivot)
    number = square.number
    assignEntry.delete(0, tkinter.END)
    if number is not None:
        assignEntry.insert(0, str(number))

# add negative flag in a group
def negateGroupOf(square):
    square.negative().update(TILE_AVAILABLE)
    number = square.number
    for cluster in [square.hcluster, square.vcluster]:
        for g in cluster.groupList():
            g.addNegative(number)

# Solver function
def solve():
    # Clear all negative set
    board.resetNegative()
    # initialize negative set
    for square in board.squareList():
        if square.status == "fixed":
            negateGroupOf(square)
        elif square.status == "assigned":
            negateGroupOf(square)
    # 
    solved = False  # Flag indicating solver completion
    while not solved:
        solved = True
        # assign number to last positive
        for square in board.squareList():
            if len(square.negative()) == TILE_LENGTH - 1:
                square.assign(set(TILE_AVAILABLE).difference(square.negative()).pop())
                print("Last positive %d at (%d,%d)" % (square.number, square.col, square.row))
                negateGroupOf(square)
                solved = False
        # scan last positive in a group
        for number in TILE_AVAILABLE:
            for group in board.groupList():
                nNegative = 0
                for square in group.squareList():
                    if number in square.negative():
                        nNegative = nNegative + 1
                if nNegative == TILE_LENGTH - 1:
                    for square in group.squareList():
                        if not (number in square.negative()):
                            square.assign(number)
                            print("Last in group %d at (%d,%d)" % (square.number, square.col, square.row))
                            negateGroupOf(square)
                            solved = False
        # scan indirect negative cluster
        for cluster in board.clusterList():
            # linear group matching
            negative = set(TILE_AVAILABLE)
            for c in cluster.linearGroup.clusterList():
                if c is not cluster:
                    negative &= c.negative()
            positive = negative - cluster.negative()
            if len(positive) > 0:
                for c in cluster.bulkGroup.clusterList():
                    if c is not cluster:
                        for s in c.squareList():
                            if len(positive - s.negative()) > 0:
                                print("Negate %s at bulk(%d,%d)" % (str(positive), s.col, s.row))
                                s.negative().update(positive)
                                solved = False
            # bulk group matching
            negative = set(TILE_AVAILABLE)
            for c in cluster.bulkGroup.clusterList():
                if c is not cluster:
                    negative &= c.negative()
            positive = negative - cluster.negative()
            if len(positive) > 0:
                for c in cluster.linearGroup.clusterList():
                    if c is not cluster:
                        for s in c.squareList():
                            if len(positive - s.negative()) > 0:
                                print("Negate %s at linear(%d,%d)" % (str(positive), s.col, s.row))
                                s.negative().update(positive)
                                solved = False
                         
    # Solved or no other solutions
    print("SOLVED")

# Callback from SOLVE button
def solveButtonOnClick():
    solve()
    board.draw(canvas)
    root.update()

solveButton["command"]=solveButtonOnClick

# Callback from CLEAR button
def clearButtonOnClick():
    for square in board.squareList():
        if square.status == "assigned":
            square.unassign()
    board.resetNegative()
    board.draw(canvas)
    root.update()

clearButton["command"] = clearButtonOnClick

# Callback from ASSIGN button
def assignButtonOnClick():
    global pivot
    if pivot is not None:
        try:
            number = int(assignEntry.get())
            board.squareAt(pivot).assign(number)
        except ValueError:
            board.squareAt(pivot).unassign()
        board.draw(canvas)
        root.update()

assignButton["command"] = assignButtonOnClick

# Create an example board
board = exampleBoard()

# Draw the board
board.draw(canvas)

# the main loop
root.mainloop()

print("Done")
