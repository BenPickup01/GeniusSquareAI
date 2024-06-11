# Create a PyGame window which displays a grid of squares with dimensions 6x6
import pygame

# Define Colour Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)

# Colour converter dictionary
colour_dict = {
    'white': WHITE,
    'black': BLACK,
    'red': RED,
    'blue': BLUE,
    'green': GREEN,
    'yellow': YELLOW,
    'orange': ORANGE,
    'purple': PURPLE,
    'teal': TEAL,
    "brown": (165, 42, 42),
    "grey": (128, 128, 128)
}


class visulizeGeniusSquare:
    def __init__(self):
        pygame.init()

        self.gameDisplay = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Genius Square")
        pygame.display.update()
        self.gameDisplay.fill(BLACK)

    def draw_grid(self, colours=None):

        if colours is None:
            for row in range(6):
                for col in range(6):
                    rect = pygame.Rect(col * (100 + 1), row * (100 + 1), 100, 100)
                    pygame.draw.rect(self.gameDisplay, WHITE, rect, 1)
            return None
        else:
            for row in range(6):
                for col in range(6):
                    # Fill the rectangle with the colour

                    colour = colour_dict[colours[row][col]]
                    rect = pygame.Rect(col * (100 + 1), row * (100 + 1), 100, 100)
                    # Draw white border
                    pygame.draw.rect(self.gameDisplay, WHITE, rect, 1)
                    # Draw filled in shape
                    pygame.draw.rect(self.gameDisplay, colour, rect)

            return None

    def update(self):
        pygame.display.update()
