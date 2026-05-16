def check_win(board: list[list[int]]) -> bool:
    win = True
    for row in board:
        for col in row:
            if col == 0:
                win = False
                break
    return win