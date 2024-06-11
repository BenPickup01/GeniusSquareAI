import random

import numpy as np
import pygame

from PyGameSimulation import visulizeGeniusSquare


# define a class of a 6 by 6 grid

def roll_dice(seed):
    # 2D array of the dice and their sides
    dice = [[[0, 0], [2, 0], [3, 0], [3, 1], [4, 1], [5, 2]],
            [[0, 1], [1, 1], [2, 1], [0, 2], [1, 0], [1, 2]],
            [[2, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3]],
            [[3, 0], [5, 1], [1, 5], [0, 4]],
            [[0, 3], [1, 4], [2, 5], [2, 4], [3, 5], [5, 5]],
            [[4, 3], [5, 3], [4, 4], [5, 4], [3, 4], [4, 5]],
            [[5, 0], [0, 5]]
            ]

    # Chooses a random value from each dice and adds it to output array
    rolls = []
    for i in dice:
        rolls.append(random.choice(i))


class PlayBoard:
    def __init__(self):
        self.grid = [[0 for _ in range(6)] for _ in range(6)]
        self.colour_grid = [["black" for _ in range(6)] for _ in range(6)]

    def place_tetroid(self, position, rotation, tetroid_number, invert=False):
        tetroids = [
            # I
            [[1, 1, 1, 1]],
            # O
            [
                [1, 1],
                [1, 1]
            ],
            # T
            [
                [0, 1, 0],
                [1, 1, 1]
            ],

            # Z
            [
                [1, 1, 0],
                [0, 1, 1]
            ],
            # J
            [
                [1, 0, 0],
                [1, 1, 1]
            ],

            # Small L
            [
                [1, 0],
                [1, 1]
            ],

            # 3 piece
            [
                [1, 1, 1]
            ],

            # 2 piece
            [
                [1, 1]
            ],

            [
                [1]
            ]
        ]
        tetroid_colour = [
            "grey",
            "green",
            "yellow",
            "red",
            "teal",
            "purple",
            "orange",
            "brown",
            "blue"
        ]

        tetroid = tetroids[tetroid_number]
        colour = tetroid_colour[tetroid_number]

        print("Tetroid: ", tetroid_number)
        print("Colour: ", colour)
        print("Rotation: ", rotation)
        print("Position: ", position)
        print("Invert: ", invert)
        # Rotate the tetroid
        for _ in range(rotation):
            tetroid = np.rot90(tetroid).tolist()

        # invert the tetroid
        if invert:
            tetroid = np.fliplr(tetroid).tolist()

        fail_score = 3
        # Place the tetroid on the grid
        try:
            for row in range(len(tetroid)):
                for col in range(len(tetroid[0])):
                    # Check if there is already a non-zero value in the grid position, if so set the position to -1
                    if self.grid[row + position[0]][col + position[1]] != 0 and tetroid[row][col] == 1:
                        self.grid[row + position[0]][col + position[1]] = -1
                        fail_score += -1
                    else:
                        if tetroid[row][col] == 1:
                            self.grid[row + position[0]][col + position[1]] = 1
                            self.colour_grid[row + position[0]][col + position[1]] = colour
        except IndexError:
            fail_score = -5

        print("Score: ", fail_score)
        return self.grid, fail_score

    def place_blockers(self, seed=None):
        if seed:
            random.seed(seed)

        dice = [[[0, 0], [2, 0], [3, 0], [3, 1], [4, 1], [5, 2]],
                [[0, 1], [1, 1], [2, 1], [0, 2], [1, 0], [1, 2]],
                [[2, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3]],
                [[3, 0], [5, 1], [1, 5], [0, 4]],
                [[0, 3], [1, 4], [2, 5], [2, 4], [3, 5], [5, 5]],
                [[4, 3], [5, 3], [4, 4], [5, 4], [3, 4], [4, 5]],
                [[5, 0], [0, 5]]
                ]

        # Chooses a random value from each dice and adds it to output array
        rolls = []
        for i in dice:
            self.place_block(random.choice(i))

        return self.get_grid()

    def get_grid(self):
        return self.grid

    def show_grid(self):
        for row in self.grid:
            print(row)

        print("\n")

    def place_block(self, position):
        self.grid[position[0]][position[1]] = 1
        self.colour_grid[position[0]][position[1]] = "white"
        return self.grid

    def get_position(self, position):
        return self.grid[position[0]][position[1]]

    def clear_board(self):
        self.grid = [[0 for _ in range(6)] for _ in range(6)]
        self.colour_grid = [["black" for _ in range(6)] for _ in range(6)]
        return self.grid

    def visualize_grid(self):
        return self.colour_grid


def shuffle_grid(board):
    board.clear_board()
    board.place_blockers()
    position = [random.randint(0, 5), random.randint(0, 5)]
    rotation = random.randint(0, 3)
    tetroid_number = random.randint(0, 7)
    invert = random.choice([True, False])
    board.place_tetroid(position, rotation, tetroid_number, invert=invert)
    print(board.show_grid())


if __name__ == "__main__":
    # create an instance of the class
    board = playBoard()
    visualBoard = visulizeGeniusSquare()

    pygame.init()
    visualBoard.draw_grid(board.visualize_grid())

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If the enter key is hit then update the board
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                shuffle_grid(board)
                visualBoard.draw_grid(board.visualize_grid())
                visualBoard.update()
                pygame.display.update()

        visualBoard.update()


