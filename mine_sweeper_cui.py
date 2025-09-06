import curses as cs

from mine_sweeper import GameBoard, Status

white = 1
red = 2
red_r = 3


class TUI:
    def __init__(self, stdscr, num_row: int, num_col: int, num_bomb: int):
        self.num_row = num_row
        self.num_col = num_col
        self.gb = GameBoard(num_row, num_col, num_bomb)
        self.scr = stdscr
        cs.noecho()
        cs.cbreak()
        cs.start_color()
        cs.init_pair(white, cs.COLOR_WHITE, cs.COLOR_BLACK)
        cs.init_pair(red, cs.COLOR_RED, cs.COLOR_BLACK)
        cs.init_pair(red_r, cs.COLOR_BLACK, cs.COLOR_RED)
        self.scr.keypad(True)

    def cui_game(self):
        # gb = self.gb
        finished = False
        while not finished:
            while (
                self.gb.status == Status.PLAYING
                or self.gb.status == Status.UNINITIALIZED
            ):
                self.print_game()
                cs.curs_set(0)
                c = self.scr.getkey()
                match c:
                    case "q" | "Q":
                        break
                    case "KEY_DOWN":
                        self.gb.down()
                    case "KEY_UP":
                        self.gb.up()
                    case "KEY_LEFT":
                        self.gb.left()
                    case "KEY_RIGHT":
                        self.gb.right()
                    case "o" | "O":
                        self.gb.open()
                    case "f" | "F":
                        self.gb.flag()
                    case _:
                        pass
            self.print_game()
            while True:
                c = self.scr.getkey()
                match c:
                    case "c" | "C":
                        finished = False
                        self.gb.new_game()
                        break
                    case "q" | "Q":
                        finished = True
                        break
                    case _:
                        pass

    def print_game(self):
        self.scr.refresh()
        gb = self.gb
        for row, panel_row in enumerate(gb.field):
            for col, p in enumerate(panel_row):
                if row == gb.cursor_row and col == gb.cursor_col:
                    if gb.status == Status.LOSE:
                        c = "B"
                        font = cs.color_pair(red_r)
                    else:
                        c = "@"
                        font = cs.color_pair(red)
                else:
                    c = str(p)
                    if c == "B":
                        font = cs.color_pair(red)
                    else:
                        font = cs.color_pair(white)
                self.scr.addstr(row, col * 2, c, font)
        match (gb.status):
            case Status.PLAYING | Status.UNINITIALIZED:
                message = f"input <- ^v -> / O open / F flag {gb.count_flags()}"
                font = cs.color_pair(white)
            case Status.WIN:
                message = "You Win!  Continue(C) or Quit(Q)"
                font = cs.color_pair(white)
            case Status.LOSE:
                font = cs.color_pair(red)
                message = "Game Over!  Continue(C) or Quit(Q)"
        self.scr.addstr(self.num_row + 3, 0, message, font)


def main(stdscr):
    t = TUI(stdscr, 9, 9, 10)
    t.cui_game()


cs.wrapper(main)
