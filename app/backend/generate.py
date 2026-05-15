import random
import copy


def generate_sudoku(empty_cells: int = 40) -> list[list[int]]:
    board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(board, x: int, y: int, value: int) -> bool:
        # row
        if value in board[y]:
            return False

        # column
        for row in board:
            if row[x] == value:
                return False

        # 3x3
        start_x = (x // 3) * 3
        start_y = (y // 3) * 3

        for dy in range(3):
            for dx in range(3):
                if board[start_y + dy][start_x + dx] == value:
                    return False

        return True

    def fill(board) -> bool:
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)

                    for value in numbers:
                        if is_valid(board, x, y, value):
                            board[y][x] = value

                            if fill(board):
                                return True

                            board[y][x] = 0

                    return False

        return True

    def count_solutions(board, limit=2):
        solutions = 0

        def solve():
            nonlocal solutions

            if solutions >= limit:
                return

            for y in range(9):
                for x in range(9):
                    if board[y][x] == 0:
                        for value in range(1, 10):
                            if is_valid(board, x, y, value):
                                board[y][x] = value

                                solve()

                                board[y][x] = 0

                        return

            solutions += 1

        solve()
        return solutions

    # generate full board
    fill(board)

    # remove cells while preserving uniqueness
    cells = [(x, y) for y in range(9) for x in range(9)]
    random.shuffle(cells)

    removed = 0

    for x, y in cells:
        if removed >= empty_cells:
            break

        backup = board[y][x]
        board[y][x] = 0

        test_board = copy.deepcopy(board)

        if count_solutions(test_board) != 1:
            board[y][x] = backup
        else:
            removed += 1

    return board