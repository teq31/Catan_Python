import pygame
import sys
import random
import config
from core.board import Board
from core.player import Player
from gui.renderer import BoardRenderer


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Catan - Final Version")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board()
        self.board.generate_random_board()

        # Start with enough resources to build initial settlement/road AND buy a card
        start_res = {'wood': 5, 'brick': 5, 'sheep': 5, 'wheat': 5, 'ore': 5}

        p1 = Player("Red", (255, 50, 50))
        p1.resources = start_res.copy()

        p2 = Player("Blue", (50, 50, 255))
        p2.resources = start_res.copy()

        self.players = [p1, p2]
        self.current_player_idx = 0
        self.winner = None

        self.renderer = BoardRenderer(self.screen)

        self.hovered_vertex = None
        self.hovered_edge = None
        self.selected_hex = None

        self.interaction_mode = 'view'
        self.trade_offer = None

        self.last_dice_roll = 0
        self.dice_rolled_this_turn = False

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def handle_events(self):
        player = self.get_current_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if self.interaction_mode == 'move_robber':
                    print("WARNING: You must move the ROBBER! Click on a hex.")

                elif self.interaction_mode == 'trade':
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_t:
                        self.interaction_mode = 'view'
                        self.trade_offer = None
                        print("Trade cancelled.")

                    elif event.key in [pygame.K_w, pygame.K_b, pygame.K_s, pygame.K_g, pygame.K_o]:
                        selected_res = ""
                        if event.key == pygame.K_w:
                            selected_res = 'wood'
                        elif event.key == pygame.K_b:
                            selected_res = 'brick'
                        elif event.key == pygame.K_s:
                            selected_res = 'sheep'
                        elif event.key == pygame.K_g:
                            selected_res = 'wheat'
                        elif event.key == pygame.K_o:
                            selected_res = 'ore'

                        if self.trade_offer is None:
                            if player.resources[selected_res] >= 4:
                                self.trade_offer = selected_res
                                print(f"You chose to give 4 {selected_res}. Choose what to receive.")
                            else:
                                print(f"You don't have enough {selected_res} (You need 4)!")
                        else:
                            if player.trade_with_bank(self.trade_offer, selected_res):
                                print(f"Successful trade: -4 {self.trade_offer} | +1 {selected_res}")
                            self.trade_offer = None
                            self.interaction_mode = 'view'

                else:
                    if event.key == pygame.K_1:
                        self.interaction_mode = 'build_settlement'
                        print("Mode: Build Settlement")
                    elif event.key == pygame.K_2:
                        self.interaction_mode = 'build_road'
                        print("Mode: Build Road")
                    elif event.key == pygame.K_3:
                        self.interaction_mode = 'build_city'
                        print("Mode: Build City")

                    # --- BUY DEV CARD (Key 4) ---
                    elif event.key == pygame.K_4:
                        if player.can_afford('dev_card'):
                            card = self.board.draw_dev_card()
                            if card:
                                player.deduct_resources('dev_card')
                                player.dev_cards[card] += 1
                                print(f"BOUGHT DEV CARD: {card.upper()}")
                                # Daca e VP, se updateaza automat punctele
                            else:
                                print("Deck is empty!")
                        else:
                            print("Not enough resources for Dev Card (Sheep + Wheat + Ore)")

                    # --- PLAY KNIGHT (Key K) ---
                    elif event.key == pygame.K_k:
                        if player.dev_cards['knight'] > 0:
                            player.dev_cards['knight'] -= 1
                            self.interaction_mode = 'move_robber'
                            print("PLAYED KNIGHT CARD! Move the robber.")
                        else:
                            print("You don't have a Knight card!")

                    elif event.key == pygame.K_ESCAPE:
                        self.interaction_mode = 'view'

                    elif event.key == pygame.K_t:
                        self.interaction_mode = 'trade'
                        self.trade_offer = None
                        print("\n--- TRADE MODE ---")

                    elif event.key == pygame.K_r:
                        d1 = random.randint(1, 6)
                        d2 = random.randint(1, 6)
                        self.last_dice_roll = d1 + d2
                        self.dice_rolled_this_turn = True
                        print(f"\n>>> Dice: {self.last_dice_roll} <<<")

                        if self.last_dice_roll == 7:
                            print("!!! Robber (7) !!! Move the robber.")
                            self.interaction_mode = 'move_robber'
                        else:
                            self.board.distribute_resources(self.last_dice_roll)

                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.dice_rolled_this_turn:
                            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
                            self.dice_rolled_this_turn = False
                            self.last_dice_roll = 0
                            print(f"\n--- Turn: {self.players[self.current_player_idx].name} ---")
                        else:
                            print("Roll the dice at least once!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if self.interaction_mode == 'move_robber' and self.selected_hex:
                        self.board.move_robber(self.selected_hex)
                        print("The robber has been moved.")
                        self.interaction_mode = 'view'

                    elif self.interaction_mode == 'build_settlement' and self.hovered_vertex:
                        if player.can_afford('settlement'):
                            if self.board.place_settlement(self.hovered_vertex, player):
                                player.deduct_resources('settlement')
                                print("Settlement built!")

                    elif self.interaction_mode == 'build_road' and self.hovered_edge:
                        if player.can_afford('road'):
                            if self.board.place_road(self.hovered_edge, player):
                                player.deduct_resources('road')
                                print("Road built!")

                    elif self.interaction_mode == 'build_city' and self.hovered_vertex:
                        if player.can_afford('city'):
                            if self.board.upgrade_to_city(self.hovered_vertex, player):
                                player.deduct_resources('city')
                                print("City upgraded!")

    def update(self):
        if self.winner: return

        for p in self.players:
            if p.update_victory_points() >= 10:
                self.winner = p.name
                print(f"WINNER: {p.name}")

        mx, my = pygame.mouse.get_pos()
        self.hovered_vertex = None
        self.hovered_edge = None
        self.selected_hex = None

        for tile in self.board.tiles:
            if tile.contains_point(mx, my):
                tile.is_highlighted = True
                self.selected_hex = tile

                if self.interaction_mode != 'move_robber':
                    if self.interaction_mode in ['build_settlement', 'build_city', 'view']:
                        v = tile.get_nearest_vertex(mx, my)
                        if v: self.hovered_vertex = v; return

                    if self.interaction_mode in ['build_road', 'view']:
                        e = tile.get_nearest_edge(mx, my)
                        if e: self.hovered_edge = e; return
            else:
                tile.is_highlighted = False

    def draw(self):
        if self.winner:
            self.renderer.draw_winner(self.winner)
            pygame.display.flip()
            return

        self.screen.fill(config.BG_COLOR)
        self.renderer.draw_board(self.board, self.hovered_vertex, self.hovered_edge)
        current_player = self.get_current_player()
        self.renderer.draw_ui(current_player, self.interaction_mode, self.last_dice_roll)

        if self.interaction_mode == 'move_robber':
            font = pygame.font.SysFont('Arial', 30, bold=True)
            txt = font.render("Move the robber!", True, (255, 0, 0))
            self.screen.blit(txt, (config.SCREEN_WIDTH // 2 - 200, 120))

        if self.interaction_mode == 'trade':
            center_x = config.SCREEN_WIDTH // 2
            center_y = config.SCREEN_HEIGHT // 2

            bg_rect = pygame.Rect(center_x - 300, center_y - 100, 600, 200)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, width=3)

            font_big = pygame.font.SysFont('Arial', 32, bold=True)
            font_small = pygame.font.SysFont('Arial', 24)

            title = font_big.render("BANK TRADE (4:1)", True, (255, 215, 0))
            self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 80))

            if self.trade_offer is None:
                instr1 = font_small.render("STEP 1: Choose resource to GIVE (Must have 4+):", True, (255, 255, 255))
            else:
                instr1 = font_small.render(f"STEP 2: Giving 4 {self.trade_offer.upper()}. Choose what to GET:", True,
                                           (100, 255, 100))

            self.screen.blit(instr1, (center_x - instr1.get_width() // 2, center_y - 30))

            instr2 = font_small.render("[W]ood  [B]rick  [S]heep  [G]rain  [O]re", True, (200, 200, 200))
            self.screen.blit(instr2, (center_x - instr2.get_width() // 2, center_y + 10))

            cancel = font_small.render("Press [ESC] to Cancel", True, (255, 100, 100))
            self.screen.blit(cancel, (center_x - cancel.get_width() // 2, center_y + 60))

        pygame.display.flip()

    def run(self):
        print("Start! R=Dice, T=Trade, 4=Buy Card, K=Knight")
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