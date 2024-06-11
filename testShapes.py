

# A file to test shapes and to see why they are bugging


import numpy as np

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

def testing_shapes(tetroid, rotation, invert):
    # Rotate the tetroid
    for _ in range(rotation):
        tetroid = np.rot90(tetroid).tolist()

    # Invert the tetroid
    if invert:
        tetroid = np.fliplr(tetroid).tolist()

    return tetroid

print(testing_shapes(tetroids[3], 3, True))

