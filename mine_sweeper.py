import random
from enum import Enum

from panel import BlankPanel, BombPanel, BorderPanel, Panel


class Status(Enum):
    UNINITIALIZED = 1
    PLAYING = 2
    WIN = 3
    LOSE = 4


class GameBoard:
    def __init__(self, size_y: int, size_x: int, num_bomb: int):
        self.size_x: int = size_x
        self.size_y: int = size_y
        self.field_size_x: int = size_x + 2
        self.field_size_y: int = size_y + 2
        self.field: list[list[Panel]]
        self.num_bomb: int = num_bomb
        self.cursor_row: int = 1
        self.cursor_col: int = 1
        self.status: Status = Status.UNINITIALIZED

        self.init_field()

    def init_field(self):
        # Fill Panel
        field = []
        for _ in range(self.field_size_y):
            panel_row = []
            for _ in range(self.field_size_x):
                panel_row.append(BlankPanel())
            field.append(panel_row)
        # Fill Boarder
        for y in range(self.field_size_y):
            field[y][0] = BorderPanel()
            field[y][self.field_size_x - 1] = BorderPanel()
        for x in range(self.field_size_x):
            field[0][x] = BorderPanel()
            field[self.field_size_y - 1][x] = BorderPanel()
        self.field = field

    def get_status(self) -> Status:
        if self.status == Status.UNINITIALIZED:
            return self.status
        self.status = Status.WIN
        for panel_row in self.field:
            for p in panel_row:
                if p.is_open and p.is_instance_of(BombPanel):
                    self.status = Status.LOSE
                    return Status.LOSE
                if not p.is_open and p.is_instance_of(BlankPanel):
                    self.status = Status.PLAYING
        return self.status

    def new_game(self):
        # reset all panel
        for row in range(1, self.size_y + 1):
            for col in range(1, self.size_x + 1):
                self.field[row][col] = BlankPanel()
        self.status = Status.UNINITIALIZED

    def set_bomb(self, cursor_row: int = None, cursor_col: int = None):
        # Check bomb num is valid.
        if self.num_bomb >= self.size_x * self.size_y:
            raise ValueError
        if cursor_row is None:
            cursor_row = self.cursor_row
        if cursor_col is None:
            cursor_col = self.cursor_col

        # Set Mines
        bomb_counter = 0
        while bomb_counter < self.num_bomb:
            x = random.randint(1, self.size_x)
            y = random.randint(1, self.size_y)
            if x == cursor_col and y == cursor_row:
                continue
            if not self.field[y][x].is_instance_of(BombPanel):
                self.field[y][x] = BombPanel()
                bomb_counter += 1
        self.calc_bomb_values()
        self.status = Status.PLAYING

    def calc_panel_bomb_value(self, y: int, x: int):
        bomb_num = 0
        for row in range(y - 1, y + 2):
            for col in range(x - 1, x + 2):
                if self.field[row][col].is_instance_of(BombPanel):
                    bomb_num += 1
        self.field[y][x].bomb_num = bomb_num

    def calc_bomb_values(self):
        for row in range(1, self.size_y + 1):
            for col in range(1, self.size_x + 1):
                panel = self.field[row][col]
                if not panel.is_instance_of(BombPanel):
                    self.calc_panel_bomb_value(row, col)

    def __str__(self):
        board_text: str = ""
        for panel_row in self.field:
            for current_panel in panel_row:
                board_text += str(current_panel)
                board_text += " "
            board_text += "\n"
        return board_text

    def up(self):
        self.cursor_row -= 1
        if self.cursor_row < 1:
            self.cursor_row = 1

    def down(self):
        self.cursor_row += 1
        if self.cursor_row > self.size_y:
            self.cursor_row = self.size_y

    def right(self):
        self.cursor_col += 1
        if self.cursor_col > self.size_x:
            self.cursor_col = self.size_x

    def left(self):
        self.cursor_col -= 1
        if self.cursor_col < 1:
            self.cursor_col = 1

    def user_input(self) -> (int, int):
        """
        Get game input from console

        return:
            inputY
            inputX
        """
        while True:
            try:
                inputY = int(input("input y\n"))
            except ValueError:
                continue
            if inputY >= 1 and inputY <= self.size_y:
                break
        while True:
            try:
                inputX = int(input("input x\n"))
            except ValueError:
                continue
            if inputX >= 1 and inputX <= self.size_x:
                break
        return inputY, inputX

    def open(self, row: int = None, col: int = None) -> bool:
        """
        Open panel

        param:
            y
            x
        return:
            The game is alive or not
        """
        if row is None:
            row = self.cursor_row
        if col is None:
            col = self.cursor_col

        # Set Bombs if not initialized
        if self.status == Status.UNINITIALIZED:
            self.set_bomb(row, col)

        # Open Panel
        safe_open = False
        panel = self.field[row][col]
        if panel.is_flagged:
            safe_open = True
        else:
            panel.is_open = True
            if panel.is_instance_of(BombPanel):
                safe_open = False
                self.bomb_open()
            else:
                if panel.bomb_num == 0:
                    self.cascade_open()
                safe_open = True
        self.get_status()
        return safe_open

    def flag(self, row: int = None, col: int = None):
        if row is None:
            row = self.cursor_row
        if col is None:
            col = self.cursor_col
        self.field[row][col].flag()

    def open_around(self, y: int, x: int) -> int:
        """
        open panels at around specific panel

        return:
            number of newly opened panels
        """
        open_num = 0
        for row in range(y - 1, y + 2):
            for col in range(x - 1, x + 2):
                panel = self.field[row][col]
                if not panel.is_open:
                    panel.open()
                    open_num += 1
        return open_num

    def cascade_open(self):
        """
        automatic open around "0" panel
        """
        new_open = 1
        while new_open > 0:
            new_open = 0
            for row in range(1, self.size_y + 1):
                for col in range(1, self.size_x + 1):
                    panel = self.field[row][col]
                    if panel.is_open and panel.bomb_num == 0:
                        new_open += self.open_around(row, col)

    def bomb_open(self):
        """
        Open all bombs for game over status
        """
        for panel_row in self.field:
            for panel in panel_row:
                if not panel.is_open and panel.is_instance_of(BombPanel):
                    panel.open()

    def is_finished(self) -> bool:
        """
        check whether this game is finished or not
        """
        for panel_row in self.field:
            for panel in panel_row:
                if not panel.is_open and not panel.is_instance_of(BombPanel):
                    return False
        return True

    def count_flags(self) -> int:
        """
        count flagged panels
        """
        counter = 0
        for panel_row in self.field:
            for panel in panel_row:
                if panel.is_flagged:
                    counter += 1
        return counter

    def cli_game(self):
        """
        CLI game
        """
        finished = False
        while not finished:
            print(self)
            y, x = self.user_input()
            ret = self.open(y, x)
            if ret:
                self.cascade_open()
            else:
                self.bomb_open()
                print(self)
                print("Game Over!")
                return
            finished = self.is_finished()
        self.bomb_open()
        print(self)
        print("You Win!")


if __name__ == "__main__":
    gb = GameBoard(9, 9, 10)
    gb.cli_game()
