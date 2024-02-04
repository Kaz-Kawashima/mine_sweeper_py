import random

from panel import BlankPanel, BombPanel, BorderPanel, Panel


class GameBoard:
    def __init__(self, size_x: int, size_y: int, all_bomb_num: int):
        self.mined: bool = False
        self.size_x: int = size_x
        self.size_y: int = size_y
        self.field_size_x: int = size_x + 2
        self.field_size_y: int = size_y + 2
        self.field: list[list[Panel]]
        self.all_bomb_num: int = all_bomb_num

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
            field[y][self.field_size_y - 1] = BorderPanel()
        for x in range(self.field_size_x):
            field[0][x] = BorderPanel()
            field[self.field_size_y - 1][x] = BorderPanel()
        self.field = field
        # Set Bomb
        self.set_bomb_all(all_bomb_num)
        self.calc_bomb_num_all()

    def new_game(self):
        self.set_bomb_all(self.all_bomb_num)
        self.calc_bomb_num_all()
        # close all panel
        for col in range(1, self.size_y + 1):
            for row in range(1, self.size_x + 1):
                self.field[col][row].is_open = False

    def set_bomb(self):
        finished = False
        while not finished:
            x = random.randint(1, self.size_x)
            y = random.randint(1, self.size_y)
            if not isinstance(self.field[y][x], BombPanel):
                self.field[y][x] = BombPanel()
                finished = True

    def set_bomb_all(self, all_bomb_num: int):
        if all_bomb_num >= self.size_x * self.size_y:
            raise Exception
        for _ in range(all_bomb_num):
            self.set_bomb()
        self.mined = True

    def calc_bomb_num(self, y: int, x: int):
        bomb_num = 0
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                if isinstance(self.field[yy][xx], BombPanel):
                    bomb_num += 1
        self.field[y][x].bomb_num = bomb_num

    def calc_bomb_num_all(self):
        for y in range(1, self.size_y + 1):
            for x in range(1, self.size_x + 1):
                panel = self.field[y][x]
                if not isinstance(panel, BombPanel):
                    self.calc_bomb_num(y, x)

    def __str__(self):
        board_text: str = ""
        for panel_row in self.field:
            for current_panel in panel_row:
                board_text += str(current_panel)
                board_text += " "
            board_text += "\n"
        return board_text

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

    def open(self, y: int, x: int) -> bool:
        """
        Open panel

        param:
            y
            x
        return:
            The game is alive or not
        """
        panel = self.field[y][x]
        if panel.is_flagged:
            return True
        else:
            panel.is_open = True
            if isinstance(panel, BombPanel):
                return False
            else:
                return True

    def flag(self, y: int, x: int):
        self.field[y][x].flag()

    def open_around(self, y: int, x: int) -> int:
        """
        open panels at around specific panel

        return:
            number of newly opened panels
        """
        open_num = 0
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                panel = self.field[yy][xx]
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
            for y in range(1, self.size_y + 1):
                for x in range(1, self.size_x + 1):
                    panel = self.field[y][x]
                    if panel.is_open and panel.bomb_num == 0:
                        new_open += self.open_around(y, x)

    def bomb_open(self):
        """
        Open all bombs for game over status
        """
        for panel_row in self.field:
            for panel in panel_row:
                if not panel.is_open and isinstance(panel, BombPanel):
                    panel.open()

    def is_finished(self) -> bool:
        """
        check whether this game is finished or not
        """
        for panel_row in self.field:
            for panel in panel_row:
                if not panel.is_open and not isinstance(panel, BombPanel):
                    return False
        return True

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
