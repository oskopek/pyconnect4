from typing import Optional, Tuple

import numpy as np
import os


def print_elem(elem: int) -> str:
    if elem == 0:
        return " "
    elif elem == -1:
        return "X"
    elif elem == 1:
        return "O"
    else:
        raise ValueError()


def print_board(board: np.ndarray, player: int) -> str:
    rows = ["", "  " + "===" * (board.shape[1] - 1) + "="]
    for row in board:
        rows.append("  " + "  ".join(map(print_elem, row)))
    rows.append("  " + "===" * (board.shape[1] - 1) + "=")
    rows.append("  " + "  ".join(map(str, range(1, board.shape[1] + 1))))
    rows.append("")
    if player == -1:
        rows.append(f"  Player {print_elem(player)} is playing: ")
    else:
        rows.append(f"  Player {print_elem(player)} is playing... (please wait)")

    return "\n".join(rows)


def clear_screen() -> None:
    os.system("clear")  # on linux / os x


def read_input_col() -> Optional[int]:
    dig = input().strip()
    if "1" <= dig <= "9":
        return int(ord(dig) - ord("1"))
    else:
        return None


def won(board: np.ndarray, place: Tuple[int, int], connect: int = 4) -> int:
    x, y = place
    m, n = board.shape
    player = int(board[x, y])
    longest = 1

    # row
    cur = 0
    for i in range(y + 1, n):
        if board[x, i] != player:
            break
        cur += 1
    for i in range(y, -1, -1):
        if board[x, i] != player:
            break
        cur += 1
    longest = max(longest, cur)

    # col
    cur = 0
    for i in range(x + 1, m):
        if board[i, y] != player:
            break
        cur += 1
    for i in range(x, -1, -1):
        if board[i, y] != player:
            break
        cur += 1
    longest = max(longest, cur)

    # diag
    cur = 0
    i = 0
    while x + i < m and y + i < n:
        if board[x + i, y + i] != player:
            break
        cur += 1
        i += 1
    i = 1
    while x - i >= 0 and y - i >= 0:
        if board[x - i, y - i] != player:
            break
        cur += 1
        i += 1
    longest = max(longest, cur)

    # rev diag
    cur = 0
    i = 0
    while x + i < m and y - i >= 0:
        if board[x + i, y - i] != player:
            break
        cur += 1
        i += 1
    i = 1
    while x - i >= 0 and y + i < n:
        if board[x - i, y + i] != player:
            break
        cur += 1
        i += 1
    longest = max(longest, cur)

    return player if longest >= connect else 0


def next_step(board: np.ndarray, col: int, player: int) -> Tuple[int, int]:
    if board[0, col] != 0:
        return True, player  # repeat turn

    m = board.shape[0]
    for row_idx in range(m):
        if row_idx + 1 == m or board[row_idx + 1, col] != 0:
            board[row_idx, col] = player
            return won(board, (row_idx, col)), -player

    raise ValueError("Invalid state.")


def minimax(board: np.ndarray, player: int, depth: int = 0) -> Tuple[int, int]:
    if depth >= 6:
        return 0, 0

    if not (board == 0).any():
        return 0, 0

    def get_row_idx(col: int) -> int:
        row_idx = 0
        while row_idx + 1 < m:
            if board[row_idx + 1, col] != 0:
                break
            row_idx += 1
        return row_idx

    vals = []
    for col in range(board.shape[1]):
        if board[0, col] != 0:
            continue
        row_idx = get_row_idx(col)

        board[row_idx, col] = player
        if won(board, (row_idx, col)):
            board[row_idx, col] = 0
            return col, player * np.infty
        else:
            _, val = minimax(board, -player, depth=depth + 1)
            vals.append((col, val))
        board[row_idx, col] = 0

    if player > 0:
        return max(vals, key=lambda x: x[1])
    else:
        return min(vals, key=lambda x: x[1])


def main(m: int, n: int) -> None:
    board = np.zeros((m, n))
    game_won = 0
    player = -1

    while not game_won:
        clear_screen()
        print(print_board(board, player), end="")

        col = None
        if player == 1:  # minimax
            col, _ = minimax(board, player)
        else:  # user
            while col is None:
                col = read_input_col()

        game_won, player = next_step(board, col, player)
        if not (board == 0).any():
            game_won = 0
            player = 0
            break

    clear_screen()
    print(print_board(board, player)[:-1], end="")
    print(f"\n\n PLAYER {print_elem(game_won)} WON!")


if __name__ == "__main__":
    m = 6
    n = 7
    main(m, n)
