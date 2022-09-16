import numpy as np
import random as rd
from enum import Enum
from Color import Color


class Sudoku:
    BOARD_SIDE_VALUE = 9
    SQUARE_SIZE = 3
    NUM_OF_SQUARES_IN_ROW = BOARD_SIDE_VALUE // SQUARE_SIZE
    MAX_BOARD_VALUES_SIZE = BOARD_SIDE_VALUE ** 2

    def __init__(
            self,
            board_values_to_remove: int = MAX_BOARD_VALUES_SIZE,
            save_solution: bool = True,
            generate_board: bool = True
    ):
        if board_values_to_remove > Sudoku.MAX_BOARD_VALUES_SIZE:
            print("{color_start}ERROR: board_values_size exceeds maximum value {max_val}!!!{color_end}".format(
                color_start=Color.ERROR,
                max_val=Sudoku.MAX_BOARD_VALUES_SIZE,
                color_end=Color.ENDC
            ))
            exit(1)
        self.square_ranges = [
            range(i * Sudoku.SQUARE_SIZE, (i + 1) * Sudoku.SQUARE_SIZE)
            for i in range(Sudoku.NUM_OF_SQUARES_IN_ROW)
        ]
        self.board_values_to_remove = board_values_to_remove
        self.save_solution = save_solution
        self.saved_board_solution = None
        self.board = None
        if generate_board:
            self.generate_board()

    @staticmethod
    def __get_row() -> np.array:
        return np.arange(1, Sudoku.BOARD_SIDE_VALUE + 1)

    @staticmethod
    def __get_random_row() -> np.array:
        return np.array(rd.sample(set(Sudoku.__get_row()), Sudoku.BOARD_SIDE_VALUE))

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

    def get_rows(self) -> np.array:
        return self.board

    def get_columns(self) -> np.array:
        return self.board.transpose()

    def get_squares(self) -> np.array:
        return self.board.reshape((
            Sudoku.NUM_OF_SQUARES_IN_ROW,
            Sudoku.NUM_OF_SQUARES_IN_ROW,
            Sudoku.SQUARE_SIZE,
            Sudoku.SQUARE_SIZE
        )).swapaxes(1, 2).reshape(-1, Sudoku.SQUARE_SIZE, Sudoku.SQUARE_SIZE)

    def __get_square_from_coordinates(self, coordinates: tuple) -> int:
        y, x = coordinates
        return \
            next(i for i, s_range in enumerate(self.square_ranges) if y in s_range) \
            + \
            next(i for i, s_range in enumerate(self.square_ranges) if x in s_range)

    def __get_context_variants(self, coordinates: tuple) -> np.array:
        y, x = coordinates
        return Sudoku.__get_row()[np.isin(Sudoku.__get_row(), np.unique(np.concatenate([
            self.get_rows()[y],
            self.get_columns()[x],
            self.get_squares()[self.__get_square_from_coordinates(coordinates)].flatten()
        ])), invert=True)]

    def __get_board_state(self) -> bool:
        def get_unique_state(arr_outer: np.array) -> bool:
            counts_outer = np.array(
                list(
                    map(
                        lambda arr_inner: np.unique(arr_inner[arr_inner != 0], return_counts=True),
                        arr_outer
                    )
                ),
                dtype=object
            )[:, 1]
            return all(list(map(lambda counts_inner: np.all(counts_inner <= 1), counts_outer)))

        return all(map(get_unique_state, (self.get_rows(), self.get_columns(), self.get_squares())))

    def __solve_board_backtrace(self, coordinates: tuple = (0, 0)) -> bool:
        if coordinates is None:
            print("{color_start}INFO: Sudoku board solved{color_end}".format(
                color_start=Color.OKGREEN,
                color_end=Color.ENDC
            ))
            return True
        variants = self.__get_random_row()
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
    sudoku = Sudoku(0, generate_board=False)
    sudoku.board = np.array(
        [[8, 0, 0, 1, 0, 0, 0, 7, 0],
         [0, 2, 0, 0, 4, 0, 8, 0, 0],
         [0, 6, 0, 7, 0, 0, 0, 0, 0],
         [0, 0, 0, 4, 7, 0, 9, 0, 8],
         [2, 4, 0, 0, 8, 0, 0, 0, 0],
         [0, 3, 8, 0, 0, 0, 0, 0, 5],
         [0, 8, 0, 6, 0, 4, 1, 0, 0],
         [9, 0, 0, 0, 0, 7, 2, 0, 4],
         [0, 0, 5, 8, 1, 0, 0, 0, 6]]
    )

    # print(sudoku.test((0, 0)))
    #
    # sudoku = Sudoku(20)
    print(sudoku)
    sudoku.solve_board()
    print(sudoku)
