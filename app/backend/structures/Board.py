class Board:
    board = []

    @staticmethod
    def check(array: list[list[int]]) -> bool:
        # Проверка размера
        if len(array) != 9:
            return False

        for row in array:
            if len(row) != 9:
                return False

        # Проверка строк
        for row in array:
            nums = [x for x in row if x != 0]
            if len(nums) != len(set(nums)):
                return False

        # Проверка столбцов
        for x in range(9):
            nums = []

            for y in range(9):
                value = array[y][x]

                if value != 0:
                    nums.append(value)

            if len(nums) != len(set(nums)):
                return False

        # Проверка квадратов 3x3
        for square_y in range(0, 9, 3):
            for square_x in range(0, 9, 3):
                nums = []

                for dy in range(3):
                    for dx in range(3):
                        value = array[square_y + dy][square_x + dx]

                        if value != 0:
                            nums.append(value)

                if len(nums) != len(set(nums)):
                    return False

        # Проверка диапазона значений
        for row in array:
            for value in row:
                if not (0 <= value <= 9):
                    return False

        return True

    def __init__(self, array: list[list[int]] = None):
        if array:
            if not Board.check(array):
                raise ValueError()

            self.board = array
        else:
            self.board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(9)
            ]

    def place(self, x: int, y: int, value: int):
        new_board = [row.copy() for row in self.board]

        new_board[y - 1][x - 1] = value

        if not Board.check(new_board) or value not in range(1, 10):
            raise ValueError(f"Invalid move: {value} to ({x}, {y})")

        self.board = new_board


    def __repr__(self):
        display = ""
        for row in self.board:
            display += "  ".join(map(lambda c: str(c) if c != 0 else "□", row)) + "\n"
        return display


