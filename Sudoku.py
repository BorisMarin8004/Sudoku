import numpy as np
import random as rd
from Color import Color


class Sudoku:
    BOARD_SIDE_VALUE = 9
    MAX_BOARD_VALUES_SIZE = 30

    def __init__(self, board_values_to_remove: int = MAX_BOARD_VALUES_SIZE, save_solution: bool = True, generate_board: bool = True):
        if board_values_to_remove > Sudoku.MAX_BOARD_VALUES_SIZE:
            print("{color_start}ERROR: board_values_size exceeds maximum value {max_val}!!!{color_end}".format(
                color_start=Color.ERROR,
                max_val=Sudoku.MAX_BOARD_VALUES_SIZE,
                color_end=Color.ENDC
            ))
            exit(1)
        self.board_values_to_remove = board_values_to_remove
        self.save_solution = save_solution
        self.saved_board_solution = None
        self.board = None
        if generate_board:
            self.generate_board()

    @staticmethod
    def __get_random_row() -> np.array:
        return np.array(rd.sample(range(1, Sudoku.BOARD_SIDE_VALUE + 1), Sudoku.BOARD_SIDE_VALUE))

    @staticmethod
    def __get_random_coordinate() -> tuple:
        return rd.randint(0, Sudoku.BOARD_SIDE_VALUE - 1), rd.randint(0, Sudoku.BOARD_SIDE_VALUE - 1)

    @staticmethod
    def __get_next_coordinate(curr_coordinates: tuple) -> tuple or None:
        next_x = curr_coordinates[1] + 1
        next_y = curr_coordinates[0]
        if next_x >= Sudoku.BOARD_SIDE_VALUE:
            next_x = 0
            next_y += 1
            if next_y >= Sudoku.BOARD_SIDE_VALUE:
                print("{color_start}INFO: Reached the end of board{color_end}".format(
                    color_start=Color.OKCYAN,
                    color_end=Color.ENDC
                ))
                return None
        return next_y, next_x

    def __get_board_state(self) -> bool:
        def get_unique_state(arr_outer: np.array) -> bool:
            counts_outer = np.array(list(map(lambda arr_inner: np.unique(arr_inner[arr_inner != 0], return_counts=True), arr_outer)), dtype=object)[:, 1]
            return all(list(map(lambda counts_inner: np.all(counts_inner <= 1), counts_outer)))

        def get_rows_state() -> bool:
            return get_unique_state(self.board)

        def get_columns_state() -> bool:
            return get_unique_state(self.board.transpose())

        def get_squares_state() -> bool:
            squares = self.board.reshape((3, 3, 3, 3)).swapaxes(1, 2).reshape(-1, 3, 3)
            return get_unique_state(squares)

        return all((get_rows_state(), get_columns_state(), get_squares_state()))

    def __solve_board_backtrace(self, coordinates: tuple = (0, 0)) -> bool:
        if coordinates is None:
            print("{color_start}INFO: Sudoku board solved{color_end}".format(
                color_start=Color.OKGREEN,
                color_end=Color.ENDC
            ))
            return True
        variants = Sudoku.__get_random_row()
        for variant in variants:
            next_coordinates = Sudoku.__get_next_coordinate(coordinates)
            if self.board[coordinates] == 0:
                self.board[coordinates] = variant
                if self.__get_board_state():
                    if not self.__solve_board_backtrace(next_coordinates):
                        self.board[coordinates] = 0
                    else:
                        return True
                else:
                    self.board[coordinates] = 0
            else:
                return self.__solve_board_backtrace(next_coordinates)
        return False

    def __remove_random(self) -> None:
        while self.board_values_to_remove > 0:
            coordinates = Sudoku.__get_random_coordinate()
            if self.board[coordinates] != 0:
                self.board[coordinates] = 0
                self.board_values_to_remove -= 1

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return self.__str__()

    def generate_board(self) -> None:
        self.board = np.zeros(shape=(Sudoku.BOARD_SIDE_VALUE, Sudoku.BOARD_SIDE_VALUE), dtype=int)
        self.solve_board()
        if self.save_solution:
            self.saved_board_solution = self.board
        self.__remove_random()

    def solve_board(self) -> None:
        self.__solve_board_backtrace()


if __name__ == "__main__":
    sudoku = Sudoku(20)
    print(sudoku)
    sudoku.solve_board()
    print(sudoku)
