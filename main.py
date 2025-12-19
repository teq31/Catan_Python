import pygame
import sys
import config
from core.board import Board
from gui.renderer import BoardRenderer


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board()
        self.board.generate_random_board()

        self.renderer = BoardRenderer(self.screen)

        self.hovered_vertex = None
        self.hovered_edge = None
        self.selected_hex = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.hovered_vertex:
                        print(f"You clicked a vertex at {self.hovered_vertex}")
                    elif self.hovered_edge:
                        print(f"You clicked an edge between {self.hovered_edge[0]} and {self.hovered_edge[1]}")
                    elif self.selected_hex:
                        print(f"You clicked the polygon : {self.selected_hex.resource_type}")

    def update(self):
        mx, my = pygame.mouse.get_pos()

        self.hovered_vertex = None
        self.hovered_edge = None
        self.selected_hex = None

        found_interaction = False

        for tile in self.board.tiles:
            if tile.contains_point(mx, my):
                tile.is_highlighted = True
                self.selected_hex = tile

                nearest_v = tile.get_nearest_vertex(mx, my)
                if nearest_v:
                    self.hovered_vertex = nearest_v
                    found_interaction = True

                if not found_interaction:
                    nearest_e = tile.get_nearest_edge(mx, my)
                    if nearest_e:
                        self.hovered_edge = nearest_e

            else:
                tile.is_highlighted = False

    def draw(self):
        self.screen.fill(config.BG_COLOR)
        self.renderer.draw_board(self.board, self.hovered_vertex, self.hovered_edge)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()