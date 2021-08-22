import pygame
import sys


class View:
    def __init__(self, height: int = 1000, width: int = 1500):
        pygame.init()
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Sudoku")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill((255, 255, 255))
            pygame.draw.rect(surface=self.screen, color=(0, 0, 0), rect=pygame.Rect(0, 0, 200, 200))
            # pygame.display.flip()
            self.screen.update()


if __name__ == "__main__":
    view = View()
