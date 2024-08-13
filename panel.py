from abc import ABC


class Panel(ABC):
    def __init__(self):
        self.is_open: bool = False
        self.is_flagged: bool = False

    def open(self):
        """
        Open panel
        """
        if not self.is_flagged:
            self.is_open = True

    def flag(self):
        """
        Toggle flag status
        """
        if self.is_flagged:
            self.is_flagged = False
        else:
            self.is_flagged = True

    def is_instance_of(self, TypeObject) -> bool:
        return isinstance(self, TypeObject)


class BombPanel(Panel):
    def __init__(self):
        self.is_open: bool = False
        self.is_flagged = False

    def __str__(self):
        if self.is_open:
            return "B"
        if self.is_flagged:
            return "F"
        else:
            return "x"


class BlankPanel(Panel):
    def __init__(self):
        self.is_open: bool = False
        self.is_flagged: bool = False
        self.bomb_num: int = 0

    def __str__(self):
        if self.is_open:
            if self.bomb_num > 0:
                return f"{self.bomb_num}"
            else:
                return " "
        if self.is_flagged:
            return "F"
        else:
            return "x"


class BorderPanel(Panel):
    def __init__(self):
        self.is_open: bool = True
        self.is_flagged: bool = False

    def __str__(self):
        return "="
