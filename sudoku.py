import tkinter

TILE_WIDTH = 30
TILE_HEIGHT = 30
TILE_GAP = 2
TILE_GROUP = 3
TILE_LENGTH = TILE_GROUP * TILE_GROUP
CANVAS_WIDTH = TILE_WIDTH * TILE_LENGTH + TILE_GAP
CANVAS_HEIGHT = TILE_HEIGHT * TILE_LENGTH + TILE_GAP
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CANVAS_X = (WINDOW_WIDTH - CANVAS_WIDTH) / 2
CANVAS_Y = 30

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
    width=0
)

# Gray border lines
c = "gray"
for i in range(TILE_LENGTH + 1) :
    x = TILE_WIDTH * i + TILE_GAP * 0.5
    canvas.create_line(
        x, 0,
        x, CANVAS_HEIGHT,
        fill=c,
        width=TILE_GAP
    )
    y = TILE_HEIGHT * i + TILE_GAP * 0.5
    canvas.create_line(
        0, y,
        CANVAS_WIDTH, y,
        fill=c,
        width=TILE_GAP
    )
# Black border lines
c = "black"
for i in range(0, TILE_LENGTH + 1, TILE_GROUP) :
    x = TILE_WIDTH * i + TILE_GAP * 0.5
    canvas.create_line(
        x, 0,
        x, CANVAS_HEIGHT,
        fill=c,
        width=TILE_GAP
    )
    y = TILE_HEIGHT * i + TILE_GAP * 0.5
    canvas.create_line(
        0, y,
        CANVAS_WIDTH, y,
        fill=c,
        width=TILE_GAP
    )

# the main loop
root.mainloop()

print("Done")
