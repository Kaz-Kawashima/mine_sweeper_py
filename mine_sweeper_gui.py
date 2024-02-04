import sys
import tkinter as tk
from tkinter import messagebox

from mine_sweeper import GameBoard
from panel import BombPanel

# Game settings
num_row = 9
num_col = 9
num_bomb = 10
gb = GameBoard(num_row, num_col, num_bomb)

# Gui settings
button_size = 40
margin_size = 5
tile_size = button_size + margin_size * 2
window_width = tile_size * num_col
window_height = tile_size * num_row

# Generate GUI
root = tk.Tk()
frame = tk.Frame(root)
frame.grid(column=num_col, row=num_row, sticky=tk.NSEW)
frame.master.title("mine_sweeper--")
# frame.master.geometry(f"{window_width}x{window_height}")


def refresh(button_mat: list[list[tk.Button]]):
    for row, button_row in enumerate(button_mat, start=1):
        for col, button in enumerate(button_row, start=1):
            panel = gb.field[row][col]
            if panel.is_open:
                button["state"] = "disabled"
                button["bg"] = "white"
                button["fg"] = "black"
                button["text"] = str(panel)
                if isinstance(panel, BombPanel):
                    button["bg"] = "#ff0000"
            elif panel.is_flagged:
                button["text"] = "F"
            else:
                button["text"] = " "


# click event
def left_click(self, x, y, button_mat):
    def func(self):
        ret = gb.open(y, x)
        if ret:
            print("alive")
            gb.cascade_open()
            refresh(button_mat)
        else:
            gb.bomb_open()
            refresh(button_mat)
            messagebox.showinfo("", "Game Over!")
            sys.exit()
        if gb.is_finished():
            messagebox.showinfo("", "You Win!")
            sys.exit()

    return func


# click event
def right_click(self, x, y, button_mat):
    def func(self):
        gb.flag(y, x)
        refresh(button_mat)

    return func


button_mat = []
for row in range(num_row):
    button_row = []
    for col in range(num_col):
        x = col + 1
        y = row + 1
        button = tk.Button(frame, text=" ", width=5, height=2)
        button.bind("<Button-1>", left_click(frame, x, y, button_mat))
        button.bind("<Button-2>", right_click(frame, x, y, button_mat))
        button.bind("<Button-3>", right_click(frame, x, y, button_mat))
        button.grid(column=col, row=row)
        button_row.append(button)
    button_mat.append(button_row)

root.mainloop()
