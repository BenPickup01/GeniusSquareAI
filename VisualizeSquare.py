# Create a dash app with a simple layout
import dash
import numpy as np
from dash import html, callback, Output, Input, State, MATCH, ALL

app = dash.Dash(__name__)

app.layout = html.Div([
    # Create a store to hold the grid values
    html.Div(id="store1", style={"display": "none"}),
    html.Div(id="store2", style={"display": "none"}),
    # In the center of the page make a 5 by 5 grid of light grey squares all with an id corresponding to the row
    # and column
    html.Div([
        html.Div([
            html.Button(f"{row}{col}",
                        style={"textAlign": "center", "padding": "10px",
                               "background-color": "lightgrey", "border": "1px solid black",
                               "width": "50px", "height": "50px"},
                        id={"type": "square", 'index': f"{row}, {col}"})
            for col in ['1', '2', '3', '4', '5', '6']
        ], style={"display": "flex", "flexDirection": "row"})
        for row in ['A', 'B', 'C', 'D', 'E', 'F']
    ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center"})

    # Make a button to get the grid values
    , html.Button("Get Grid", id="get-grid")
    # Make a div to show the grid values
    , html.Div(id="grid-values")
    , html.Button("Place Tetroid", id="place-tetroid")
])


# Function to take in the grid and return it as a list of 1s and 0s, 1 for any colour square and 0 for any light grey
def get_grid(grid):
    grid = [1 if i != "lightgrey" else 0 for i in grid]
    # use np to reshape into a 5 by 5 grid
    return np.array(grid).reshape(6, 6).tolist()


def place_tetroid(grid, position, rotation, tetroid_number):
    tetroids = [
        # I
        [[1, 1, 1, 1]],
        # O
        [[1, 1], [1, 1]],
        # T
        [[0, 1, 0], [1, 1, 1]],
        # S
        [[0, 1, 1], [1, 1, 0]],
        # Z
        [[1, 1, 0], [0, 1, 1]],
        # J
        [[1, 0, 0], [1, 1, 1]],
        # L
        [[0, 0, 1], [1, 1, 1]],
        # 1 piece
        [[1]]
    ]

    tetroid = tetroids[tetroid_number]

    # Rotate the tetroid
    for _ in range(rotation):
        tetroid = np.rot90(tetroid).tolist()

    # Place the tetroid on the grid
    for row in range(len(tetroid)):
        for col in range(len(tetroid[0])):
            grid[row + position[0]][col + position[1]] = tetroid[row][col]

    return grid


if __name__ == '__main__':
    app.run_server(debug=True)
