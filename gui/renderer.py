import pygame
import config


class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

    def draw_hovered_vertex(self, vertex):
        vx, vy = vertex
        pygame.draw.circle(self.screen, (255, 50, 50), (int(vx), int(vy)), 12)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(vx), int(vy)), 12, width=2)

    def draw_hovered_edge(self, edge):
        p1, p2 = edge
        pygame.draw.line(self.screen, (0, 0, 255), p1, p2, width=8)
        pygame.draw.line(self.screen, (255, 255, 255), p1, p2, width=2)

    def draw_board(self, board, hovered_vertex=None, hovered_edge=None):
        for tile in board.tiles:
            if not tile.is_highlighted:
                self.draw_hex_tile(tile)

        for tile in board.tiles:
            if tile.is_highlighted:
                self.draw_hex_tile(tile)

        if hovered_edge:
            self.draw_hovered_edge(hovered_edge)

        if hovered_vertex:
            self.draw_hovered_vertex(hovered_vertex)

    def draw_hex_tile(self, tile):
        points = tile.get_vertices()
        color = config.RESOURCE_COLORS[tile.resource_type]

        pygame.draw.polygon(self.screen, color, points)

        if tile.is_highlighted:
            pygame.draw.polygon(self.screen, (0, 0, 0), points, width=8)

            highlight_color = (0, 255, 255)  # Cyan
            pygame.draw.polygon(self.screen, highlight_color, points, width=4)

            for point in points:
                cx, cy = int(point[0]), int(point[1])
                pygame.draw.circle(self.screen, (255,255,255), (cx, cy), 8)
                pygame.draw.circle(self.screen, (0,0,0), (cx, cy), 8, width=2)
        else:
            pygame.draw.polygon(self.screen, config.COLOR_LINE, points, width=3)

        if tile.number_token is not None:
            self.draw_number_token(tile.pixel_x, tile.pixel_y, tile.number_token)

    def draw_number_token(self, x, y, number):
        pygame.draw.circle(self.screen, config.COLOR_TOKEN, (int(x), int(y)), 18)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), 18, width=1)

        text_color = (255, 0, 0) if number in [6, 8] else config.COLOR_TEXT

        text_surface = self.font.render(str(number), True, text_color)

        text_rect = text_surface.get_rect(center=(int(x), int(y)))
        self.screen.blit(text_surface, text_rect)