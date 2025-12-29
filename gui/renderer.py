import pygame
import config


class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.ui_font = pygame.font.SysFont('Arial', 18)

    def draw_board(self, board, hovered_vertex=None, hovered_edge=None):

        for tile in board.tiles:
            if not tile.is_highlighted:
                self.draw_hex_tile(tile)
        for tile in board.tiles:
            if tile.is_highlighted:
                self.draw_hex_tile(tile)

        for edge, player in board.built_roads.items():
            p1, p2 = edge
            pygame.draw.line(self.screen, player.color, p1, p2, width=8)

        for node, player in board.built_settlements.items():
            x, y = int(node[0]), int(node[1])
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 14)
            pygame.draw.circle(self.screen, player.color, (x, y), 12)

        for node, player in board.built_cities.items():
            x, y = int(node[0]), int(node[1])
            pygame.draw.rect(self.screen, (0, 0, 0), (x - 12, y - 12, 24, 24))
            pygame.draw.rect(self.screen, player.color, (x - 10, y - 10, 20, 20))

        if hovered_edge: self.draw_hovered_edge(hovered_edge)
        if hovered_vertex: self.draw_hovered_vertex(hovered_vertex)

    def draw_ui(self, player, mode, dice_roll=0):
        START_X = 20
        START_Y = 60
        PANEL_WIDTH = 240  # Putin mai lat pentru carti
        PANEL_HEIGHT = 260  # Putin mai inalt

        panel_rect = pygame.Rect(START_X, START_Y, PANEL_WIDTH, PANEL_HEIGHT)
        s = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT))
        s.set_alpha(200)
        s.fill((255, 255, 255))
        self.screen.blit(s, (START_X, START_Y))
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect, width=2)

        name_text = self.font.render(f"Turn: {player.name}", True, player.color)
        self.screen.blit(name_text, (START_X + 15, START_Y + 15))

        vp_text = self.ui_font.render(f"Points: {player.victory_points} / 10", True, (0, 0, 0))
        self.screen.blit(vp_text, (START_X + 15, START_Y + 35))

        if dice_roll > 0:
            dice_text = f"Dice: {dice_roll}"
            dice_color = (255, 0, 0) if dice_roll == 7 else (0, 0, 0)
            dice_surf = self.ui_font.render(dice_text, True, dice_color)
            self.screen.blit(dice_surf, (START_X + 150, START_Y + 18))
        else:
            warn_surf = self.ui_font.render("PRESS 'R'", True, (200, 0, 0))
            self.screen.blit(warn_surf, (START_X + 150, START_Y + 18))

        mode_text = f"Mode: {mode.upper()}"
        if mode == 'view': mode_text += " (1-4)"
        mode_surf = self.ui_font.render(mode_text, True, (50, 50, 50))
        self.screen.blit(mode_surf, (START_X + 15, START_Y + 55))

        line_y = START_Y + 80
        pygame.draw.line(self.screen, (0, 0, 0), (START_X + 15, line_y), (START_X + PANEL_WIDTH - 15, line_y), 1)

        current_y = line_y + 10
        for res, amount in player.resources.items():
            res_color = config.RESOURCE_COLORS.get(res, (0, 0, 0))
            res_str = f"{res.capitalize()}: {amount}"
            res_surf = self.ui_font.render(res_str, True, (0, 0, 0))

            pygame.draw.rect(self.screen, res_color, (START_X + 15, current_y + 5, 10, 10))
            pygame.draw.rect(self.screen, (0, 0, 0), (START_X + 15, current_y + 5, 10, 10), 1)

            self.screen.blit(res_surf, (START_X + 35, current_y))
            current_y += 20

        # --- SECTIUNE DEV CARDS ---
        pygame.draw.line(self.screen, (0, 0, 0), (START_X + 15, current_y), (START_X + PANEL_WIDTH - 15, current_y), 1)
        current_y += 5

        knight_txt = f"Knights: {player.dev_cards['knight']} (Press K)"
        k_surf = self.ui_font.render(knight_txt, True, (100, 0, 100))
        self.screen.blit(k_surf, (START_X + 15, current_y))

        current_y += 20
        vp_txt = f"VP Cards: {player.dev_cards['vp']}"
        vp_surf = self.ui_font.render(vp_txt, True, (0, 100, 0))
        self.screen.blit(vp_surf, (START_X + 15, current_y))

    def draw_hex_tile(self, tile):
        points = tile.get_vertices()
        color = config.RESOURCE_COLORS[tile.resource_type]
        pygame.draw.polygon(self.screen, color, points)

        if tile.is_highlighted:
            pygame.draw.polygon(self.screen, (0, 0, 0), points, width=8)
            pygame.draw.polygon(self.screen, (0, 255, 255), points, width=4)
            for point in points:
                cx, cy = int(point[0]), int(point[1])
                pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), 6)
                pygame.draw.circle(self.screen, (0, 0, 0), (cx, cy), 6, width=2)
        else:
            pygame.draw.polygon(self.screen, config.COLOR_LINE, points, width=3)

        if tile.has_robber:
            cx, cy = int(tile.pixel_x), int(tile.pixel_y)
            pygame.draw.circle(self.screen, (60, 60, 60), (cx, cy), 22)
            pygame.draw.circle(self.screen, (0, 0, 0), (cx, cy), 22, width=2)
            robber_text = self.font.render("!", True, (255, 50, 50))
            text_rect = robber_text.get_rect(center=(cx, cy))
            self.screen.blit(robber_text, text_rect)

        elif tile.number_token is not None:
            self.draw_number_token(tile.pixel_x, tile.pixel_y, tile.number_token)

    def draw_number_token(self, x, y, number):
        pygame.draw.circle(self.screen, config.COLOR_TOKEN, (int(x), int(y)), 18)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), 18, width=1)

        text_color = (255, 0, 0) if number in [6, 8] else config.COLOR_TEXT

        text_surface = self.font.render(str(number), True, text_color)
        text_rect = text_surface.get_rect(center=(int(x), int(y)))
        self.screen.blit(text_surface, text_rect)

    def draw_hovered_vertex(self, vertex):
        vx, vy = vertex
        s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 180), (20, 20), 12)
        pygame.draw.circle(s, (255, 50, 50, 255), (20, 20), 12, width=2)
        self.screen.blit(s, (vx - 20, vy - 20))

    def draw_hovered_edge(self, edge):
        p1, p2 = edge
        pygame.draw.line(self.screen, (200, 200, 200), p1, p2, width=6)

    def draw_winner(self, winner_name):
        s = pygame.Surface(self.screen.get_size())
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))

        font_huge = pygame.font.SysFont('Arial', 60, bold=True)
        text = font_huge.render(f"{winner_name} WINS!", True, (255, 215, 0))

        rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

        font_small = pygame.font.SysFont('Arial', 30)
        sub = font_small.render("Press [ESC] to Quit", True, (255, 255, 255))
        rect_sub = sub.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(sub, rect_sub)