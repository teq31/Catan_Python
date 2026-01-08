import pygame
import math
import os
import config


class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.ui_font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.port_font = pygame.font.SysFont('Arial', 16, bold=True)

        self.resource_images = {}
        self._load_images()

    def _load_images(self):
        target_width = int(math.sqrt(3) * config.HEX_RADIUS) + 2
        target_height = int(2 * config.HEX_RADIUS) + 2

        if hasattr(config, 'RESOURCE_IMAGES'):
            for res_type, file_path in config.RESOURCE_IMAGES.items():
                if os.path.exists(file_path):
                    try:
                        img = pygame.image.load(file_path).convert_alpha()
                        img = pygame.transform.smoothscale(img, (target_width, target_height))
                        self.resource_images[res_type] = img
                    except Exception:
                        pass

    def draw_board(self, board, hovered_vertex=None, hovered_edge=None):
        self.screen.fill((60, 100, 200))

        for tile in board.tiles:
            if not tile.is_highlighted: self.draw_hex_tile(tile)
        for tile in board.tiles:
            if tile.is_highlighted: self.draw_hex_tile(tile)

        self.draw_ports(board)

        for edge, player in board.built_roads.items():
            pygame.draw.line(self.screen, (0, 0, 0), edge[0], edge[1], width=10)
            pygame.draw.line(self.screen, player.color, edge[0], edge[1], width=6)

        for node, player in board.built_settlements.items():
            pygame.draw.circle(self.screen, (0, 0, 0), (int(node[0]), int(node[1])), 16)
            pygame.draw.circle(self.screen, player.color, (int(node[0]), int(node[1])), 13)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(node[0]), int(node[1])), 5)

        for node, player in board.built_cities.items():
            x, y = int(node[0]), int(node[1])
            pygame.draw.rect(self.screen, (0, 0, 0), (x - 14, y - 14, 28, 28))
            pygame.draw.rect(self.screen, player.color, (x - 11, y - 11, 22, 22))
            pygame.draw.rect(self.screen, (255, 255, 255), (x - 6, y - 6, 5, 5))
            pygame.draw.rect(self.screen, (255, 255, 255), (x + 1, y - 6, 5, 5))

        if hovered_edge: self.draw_hovered_edge(hovered_edge)
        if hovered_vertex: self.draw_hovered_vertex(hovered_vertex)

    def draw_hex_tile(self, tile):
        points = tile.get_vertices()

        if tile.resource_type in self.resource_images:
            img = self.resource_images[tile.resource_type]
            rect = img.get_rect(center=(tile.pixel_x, tile.pixel_y))
            self.screen.blit(img, rect)
        else:
            color = config.RESOURCE_COLORS.get(tile.resource_type, (100, 100, 100))
            pygame.draw.polygon(self.screen, color, points)

        pygame.draw.polygon(self.screen, (50, 50, 50), points, 2)

        if tile.is_highlighted:
            pygame.draw.polygon(self.screen, (255, 255, 255), points, 4)

        if tile.has_robber:
            cx, cy = int(tile.pixel_x), int(tile.pixel_y)
            pygame.draw.circle(self.screen, (30, 30, 30), (cx, cy), 20)
            pygame.draw.circle(self.screen, (200, 50, 50), (cx, cy), 20, 3)
            self.screen.blit(self.font.render("!", True, (255, 255, 255)), (cx - 4, cy - 12))
        elif tile.number_token is not None:
            self.draw_number_token(tile.pixel_x, tile.pixel_y, tile.number_token)

    def draw_ports(self, board):
        for port in board.ports:
            p1, p2 = port['edge']
            res_type = port['type']

            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2

            pygame.draw.line(self.screen, (101, 67, 33), p1, (mid_x, mid_y), width=6)
            pygame.draw.line(self.screen, (101, 67, 33), p2, (mid_x, mid_y), width=6)

            bg_color = (240, 240, 240) if res_type == '3:1' else (255, 255, 255)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(mid_x), int(mid_y)), 20)
            pygame.draw.circle(self.screen, bg_color, (int(mid_x), int(mid_y)), 18)

            if res_type != '3:1':
                res_col = config.RESOURCE_COLORS.get(res_type, (150, 150, 150))
                pygame.draw.circle(self.screen, res_col, (int(mid_x), int(mid_y)), 14)
            else:
                pygame.draw.circle(self.screen, (180, 180, 180), (int(mid_x), int(mid_y)), 14)

            label = "?" if res_type == '3:1' else "2:1"
            txt_col = (0, 0, 0)
            if res_type in ['brick', 'ore', 'wood'] and res_type != '3:1':
                txt_col = (255, 255, 255)

            txt_surf = self.port_font.render(label, True, txt_col)
            txt_rect = txt_surf.get_rect(center=(int(mid_x), int(mid_y)))
            self.screen.blit(txt_surf, txt_rect)

            if res_type == '3:1':
                ratio_surf = self.port_font.render("3:1", True, (255, 255, 255))
                bg_ratio = ratio_surf.get_rect(center=(int(mid_x), int(mid_y) + 22)).inflate(4, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_ratio, 0, 4)
                self.screen.blit(ratio_surf, ratio_surf.get_rect(center=(int(mid_x), int(mid_y) + 22)))

    def draw_ui(self, player, mode, dice_roll=0):
        START_X = 20
        START_Y = 50
        PANEL_WIDTH = 280
        PANEL_HEIGHT = 650

        s_shadow = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT))
        s_shadow.set_alpha(100)
        s_shadow.fill((0, 0, 0))
        self.screen.blit(s_shadow, (START_X + 5, START_Y + 5))

        pygame.draw.rect(self.screen, (245, 245, 245), (START_X, START_Y, PANEL_WIDTH, PANEL_HEIGHT), 0, 10)
        pygame.draw.rect(self.screen, (50, 50, 50), (START_X, START_Y, PANEL_WIDTH, PANEL_HEIGHT), 2, 10)

        pygame.draw.rect(self.screen, player.color, (START_X + 2, START_Y + 2, PANEL_WIDTH - 4, 40), 0, 10)

        cursor_y = START_Y + 10
        name_txt = self.font.render(f"{player.name}", True, (255, 255, 255) if sum(player.color) < 400 else (0, 0, 0))
        self.screen.blit(name_txt, (START_X + 15, cursor_y))
        cursor_y += 45

        self.screen.blit(self.ui_font.render(f"Points: {player.victory_points} / 10", True, (0, 0, 100)),
                         (START_X + 15, cursor_y));
        cursor_y += 25

        if dice_roll > 0:
            col = (200, 0, 0) if dice_roll == 7 else (0, 100, 0)
            self.screen.blit(self.font.render(f"Roll: {dice_roll}", True, col), (START_X + 15, cursor_y))
        else:
            self.screen.blit(self.font.render(">> ROLL DICE (R) <<", True, (220, 50, 0)), (START_X + 15, cursor_y))
        cursor_y += 30

        self.screen.blit(self.ui_font.render(f"Mode: {mode.upper()}", True, (80, 80, 80)), (START_X + 15, cursor_y));
        cursor_y += 25
        pygame.draw.line(self.screen, (200, 200, 200), (START_X + 10, cursor_y), (START_X + PANEL_WIDTH - 10, cursor_y),
                         2);
        cursor_y += 10

        for res, amt in player.resources.items():
            col = config.RESOURCE_COLORS.get(res, (0, 0, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), (START_X + 15, cursor_y + 4, 16, 16), 1)
            pygame.draw.rect(self.screen, col, (START_X + 16, cursor_y + 5, 14, 14))
            self.screen.blit(self.ui_font.render(f"{res.capitalize()}: {amt}", True, (0, 0, 0)),
                             (START_X + 40, cursor_y));
            cursor_y += 22

        pygame.draw.line(self.screen, (200, 200, 200), (START_X + 10, cursor_y + 5),
                         (START_X + PANEL_WIDTH - 10, cursor_y + 5), 2);
        cursor_y += 15

        self.screen.blit(self.font.render("Dev Cards:", True, (50, 50, 50)), (START_X + 15, cursor_y));
        cursor_y += 25

        cards = [
            (f"Knights: {player.dev_cards['knight']} (K)", (100, 0, 100)),
            (f"Monopoly: {player.dev_cards['monopoly']} (M)",
             (200, 140, 0) if player.dev_cards['monopoly'] else (150, 150, 150)),
            (f"YoP: {player.dev_cards['year_of_plenty']} (Y)",
             (0, 150, 150) if player.dev_cards['year_of_plenty'] else (150, 150, 150)),
            (f"Road Build: {player.dev_cards['road_building']} (U)",
             (139, 69, 19) if player.dev_cards['road_building'] else (150, 150, 150)),
            (f"VP Cards: {player.dev_cards['vp']}", (0, 120, 0))
        ]

        for txt, col in cards:
            self.screen.blit(self.ui_font.render(txt, True, col), (START_X + 15, cursor_y));
            cursor_y += 20

        cursor_y += 10

        if player.has_longest_road:
            pygame.draw.rect(self.screen, (255, 215, 0), (START_X + 10, cursor_y, 240, 24), 0, 5)
            self.screen.blit(self.ui_font.render("LONGEST ROAD (+2)", True, (0, 0, 0)), (START_X + 50, cursor_y + 2));
            cursor_y += 30
        if player.has_largest_army:
            pygame.draw.rect(self.screen, (200, 50, 50), (START_X + 10, cursor_y, 240, 24), 0, 5)
            self.screen.blit(self.ui_font.render("LARGEST ARMY (+2)", True, (255, 255, 255)),
                             (START_X + 50, cursor_y + 2))

        footer_y = START_Y + PANEL_HEIGHT - 50
        self.screen.blit(self.ui_font.render("[T] Bank Trade   [P] Player Trade", True, (100, 100, 100)),
                         (START_X + 15, footer_y))
        self.screen.blit(self.ui_font.render("[S] Save Game    [L] Load Game", True, (100, 100, 100)),
                         (START_X + 15, footer_y + 25))

    def draw_trade_menu(self, trade_offer, player):
        self._draw_modern_box("BANK / PORT TRADE",
                              "STEP 1: Choose resource to GIVE" if not trade_offer else f"STEP 2: Giving {trade_offer.upper()}",
                              "Choose what to GET" if trade_offer else "",
                              player=player, trade_mode=True)

    def draw_monopoly_menu(self):
        self._draw_modern_box("MONOPOLY CARD", "Choose a resource to STEAL!",
                              "All resources of this type will be yours.")

    def draw_yop_menu(self, count_selected):
        self._draw_modern_box("YEAR OF PLENTY", f"Choose 2 resources FREE.", f"Selected: {count_selected} / 2")

    def draw_p2p_menu(self, game):
        offer = game.p2p_offer
        active_side = game.p2p_active_side
        target_name = game.players[game.p2p_target_idx].name

        W, H = 600, 400;
        CX, CY = config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(200);
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        rect = pygame.Rect(CX - W // 2, CY - H // 2, W, H)
        pygame.draw.rect(self.screen, (30, 35, 45), rect, 0, 15)
        pygame.draw.rect(self.screen, (255, 215, 0), rect, 3, 15)

        title = self.title_font.render("PLAYER TRADE PROPOSAL", True, (255, 215, 0))
        self.screen.blit(title, title.get_rect(center=(CX, CY - 160)))

        target_txt = self.font.render(f"TRADING WITH: {target_name}", True, (50, 200, 255))
        self.screen.blit(target_txt, target_txt.get_rect(center=(CX, CY - 130)))

        instr = self.ui_font.render("[TAB] Switch Side  |  [SPACE] Change Partner  |  [ENTER] Propose", True,
                                    (200, 200, 200))
        self.screen.blit(instr, instr.get_rect(center=(CX, CY + 170)))

        col_give = (100, 255, 100) if active_side == 'give' else (100, 100, 100)
        pygame.draw.rect(self.screen, col_give, (CX - 250, CY - 100, 220, 220), 2)
        lbl_give = self.font.render("YOU GIVE", True, col_give)
        self.screen.blit(lbl_give, (CX - 200, CY - 130))

        y_off = 0
        for res, amt in offer['give'].items():
            txt = self.font.render(f"{amt} x {res.upper()}", True, (255, 255, 255))
            self.screen.blit(txt, (CX - 230, CY - 80 + y_off));
            y_off += 30

        col_get = (100, 255, 100) if active_side == 'get' else (100, 100, 100)
        pygame.draw.rect(self.screen, col_get, (CX + 30, CY - 100, 220, 220), 2)
        lbl_get = self.font.render("YOU WANT", True, col_get)
        self.screen.blit(lbl_get, (CX + 80, CY - 130))

        y_off = 0
        for res, amt in offer['get'].items():
            txt = self.font.render(f"{amt} x {res.upper()}", True, (255, 255, 255))
            self.screen.blit(txt, (CX + 50, CY - 80 + y_off));
            y_off += 30

    def draw_p2p_confirm(self, game):
        target_player = game.players[game.p2p_target_idx]
        current_player = game.get_current_player()

        W, H = 500, 250;
        CX, CY = config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(220);
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, (50, 0, 0), (CX - W // 2, CY - H // 2, W, H), 0, 20)
        pygame.draw.rect(self.screen, (255, 0, 0), (CX - W // 2, CY - H // 2, W, H), 4, 20)

        msg1 = self.title_font.render(f"{target_player.name.upper()}!", True, (255, 255, 255))
        self.screen.blit(msg1, msg1.get_rect(center=(CX, CY - 60)))

        msg2 = self.font.render(f"{current_player.name} offers a trade.", True, (200, 200, 200))
        self.screen.blit(msg2, msg2.get_rect(center=(CX, CY - 20)))

        msg3 = self.title_font.render("Do you ACCEPT?", True, (255, 215, 0))
        self.screen.blit(msg3, msg3.get_rect(center=(CX, CY + 30)))

        keys = self.font.render("[Y] YES      [N] NO", True, (255, 255, 255))
        self.screen.blit(keys, keys.get_rect(center=(CX, CY + 80)))

    def draw_number_token(self, x, y, number):
        pygame.draw.circle(self.screen, (240, 230, 200), (int(x), int(y)), 18)
        pygame.draw.circle(self.screen, (0, 0, 0), (int(x), int(y)), 18, 1)

        col = (200, 0, 0) if number in [6, 8] else (0, 0, 0)
        f = self.font if number in [6, 8] else self.ui_font

        txt = f.render(str(number), True, col)
        self.screen.blit(txt, txt.get_rect(center=(int(x), int(y))))

    def draw_hovered_vertex(self, vertex):
        s = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 150), (15, 15), 10)
        pygame.draw.circle(s, (255, 255, 255, 255), (15, 15), 10, 2)
        self.screen.blit(s, (vertex[0] - 15, vertex[1] - 15))

    def draw_hovered_edge(self, edge):
        pygame.draw.line(self.screen, (255, 255, 255), edge[0], edge[1], width=6)

    def draw_winner(self, winner_name):
        s = pygame.Surface(self.screen.get_size());
        s.set_alpha(220);
        s.fill((0, 0, 0));
        self.screen.blit(s, (0, 0))
        t = self.title_font.render(f"{winner_name} WINS!", True, (255, 215, 0))
        self.screen.blit(t, t.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))

    def _draw_modern_box(self, title, subtitle, sub2="", player=None, trade_mode=False):
        W, H = 520, 320;
        CX, CY = config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180);
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        shadow_rect = pygame.Rect(CX - W // 2 + 8, CY - H // 2 + 8, W, H)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, 0, 15)

        rect = pygame.Rect(CX - W // 2, CY - H // 2, W, H)
        pygame.draw.rect(self.screen, (40, 45, 55), rect, 0, 15)
        pygame.draw.rect(self.screen, (255, 215, 0), rect, 2, 15)

        t_surf = self.title_font.render(title, True, (255, 215, 0))
        self.screen.blit(t_surf, t_surf.get_rect(center=(CX, CY - 120)))

        st_surf = self.font.render(subtitle, True, (220, 220, 220))
        self.screen.blit(st_surf, st_surf.get_rect(center=(CX, CY - 70)))

        if sub2:
            st2_surf = self.ui_font.render(sub2, True, (150, 255, 150))
            self.screen.blit(st2_surf, st2_surf.get_rect(center=(CX, CY - 40)))

        keys = ["W", "B", "S", "G", "O"]
        names = ["Wood", "Brick", "Sheep", "Grain", "Ore"]
        res_keys = ['wood', 'brick', 'sheep', 'wheat', 'ore']
        colors = [config.RESOURCE_COLORS['wood'], config.RESOURCE_COLORS['brick'], config.RESOURCE_COLORS['sheep'],
                  config.RESOURCE_COLORS['wheat'], config.RESOURCE_COLORS['ore']]

        start_x = CX - 220
        y_pos = CY + 30

        for i, key in enumerate(keys):
            bx = start_x + i * 90
            pygame.draw.rect(self.screen, colors[i], (bx, y_pos, 50, 50), 0, 8)
            pygame.draw.rect(self.screen, (255, 255, 255), (bx, y_pos, 50, 50), 2, 8)

            k_s = self.font.render(key, True, (0, 0, 0))
            self.screen.blit(k_s, (bx + 16, y_pos + 11))
            k_txt = self.font.render(key, True, (255, 255, 255))
            self.screen.blit(k_txt, (bx + 15, y_pos + 10))

            n_txt = self.ui_font.render(names[i], True, (200, 200, 200))
            self.screen.blit(n_txt, (bx + 5, y_pos + 55))

            if trade_mode and player:
                res_type = res_keys[i]
                cost = player.trade_ratios.get(res_type, 4)
                if cost > player.general_port_ratio: cost = player.general_port_ratio

                has_enough = player.resources[res_type] >= cost
                c_col = (100, 255, 100) if has_enough else (255, 100, 100)
                cost_txt = self.ui_font.render(f"Cost: {cost}", True, c_col)
                self.screen.blit(cost_txt, (bx + 2, y_pos + 75))

        esc = self.ui_font.render("Press [ESC] to Cancel", True, (255, 100, 100))
        self.screen.blit(esc, esc.get_rect(center=(CX, CY + 130)))