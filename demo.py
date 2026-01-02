import pygame
import sys
import random
import config

from core.board import Board
from core.player import Player
from core.ai import AIController
from core.input_manager import InputManager
from core.rules_manager import RulesManager
from gui.renderer import BoardRenderer


class DemoGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Catan - DEMO / DEBUG MODE (4 Players)")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board()
        self.board.generate_random_board()

        p1 = Player("Human (Red)", (255, 50, 50), is_ai=False)
        p2 = Player("AI (Blue)", (50, 50, 255), is_ai=True)
        p3 = Player("AI (Green)", (50, 200, 50), is_ai=True)
        p4 = Player("AI (Orange)", (255, 165, 0), is_ai=True)
        self.players = [p1, p2, p3, p4]

        self.renderer = BoardRenderer(self.screen)
        self.ai_brain = AIController(self)
        self.input_manager = InputManager(self)
        self.rules_manager = RulesManager(self)

        self.game_phase = 'MAIN'
        self.current_player_idx = 0
        self.winner = None

        self.interaction_mode = 'view'
        self.trade_offer = None
        self.last_dice_roll = 0
        self.dice_rolled_this_turn = False
        self.yop_selected_resources = []

        self.setup_order = []
        self.setup_step_idx = 0
        self.setup_subphase = 'DONE'

        self.message = "DEMO MODE ACTIVE - GOD MODE ON"
        self.message_timer = 0

        self.apply_debug_start()

    def apply_debug_start(self):
        print("--- APPLYING GOD MODE SETTINGS ---")

        human = self.players[0]
        for r in human.resources: human.resources[r] = 50
        human.dev_cards['knight'] = 5
        human.dev_cards['monopoly'] = 5
        human.dev_cards['year_of_plenty'] = 5
        human.dev_cards['road_building'] = 5

        for i in range(1, 4):
            ai = self.players[i]
            for r in ai.resources: ai.resources[r] = 20

        for player in self.players:
            for _ in range(2):
                spots = self.board.get_all_possible_settlement_spots(player, initial_phase=True)
                if spots:
                    target = random.choice(spots)
                    self.board.place_settlement(target, player, initial_phase=True)

                    road_spots = self.board.get_all_possible_road_spots(player)
                    if road_spots:
                        r_target = random.choice(road_spots)
                        self.board.place_road(r_target, player)

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def set_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration
        self.draw()

    def check_achievements(self):
        self.rules_manager.check_achievements()

    def play_dev_card(self, card_type):
        self.rules_manager.play_dev_card(card_type)

    def _execute_monopoly(self, res_type):
        return self.rules_manager.execute_monopoly(res_type)

    def save_game(self):
        self.set_message("Save Disabled in Demo", 1000)

    def load_game(self):
        pass

    def advance_setup_step(self):
        pass

    def update(self):
        if self.winner: return
        for p in self.players:
            if p.update_victory_points() >= 10: self.winner = p.name

        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""

        curr = self.get_current_player()

        if curr.is_ai and not self.winner:
            self.ai_brain.run_main_turn(curr)
            return

        mx, my = pygame.mouse.get_pos()
        self.hovered_vertex = None;
        self.hovered_edge = None;
        self.selected_hex = None
        for tile in self.board.tiles:
            if tile.contains_point(mx, my):
                tile.is_highlighted = True;
                self.selected_hex = tile
                if self.interaction_mode not in ['move_robber', 'trade', 'monopoly', 'year_of_plenty']:
                    if self.interaction_mode in ['build_settlement', 'build_city', 'view']:
                        v = tile.get_nearest_vertex(mx, my)
                        self.hovered_vertex = v if v else None
                    if self.interaction_mode in ['build_road', 'view']:
                        e = tile.get_nearest_edge(mx, my)
                        self.hovered_edge = e if e else None
            else:
                tile.is_highlighted = False

    def handle_events(self):
        self.input_manager.handle_input()

    def draw(self):
        if self.winner: self.renderer.draw_winner(self.winner); pygame.display.flip(); return
        self.screen.fill(config.BG_COLOR)

        self.renderer.draw_board(self.board, self.hovered_vertex, self.hovered_edge)
        self.renderer.draw_ui(self.get_current_player(), self.interaction_mode, self.last_dice_roll)

        if self.message:
            font = pygame.font.SysFont('Arial', 28, bold=True)
            txt = font.render(self.message, True, (255, 255, 0))
            bg_rect = txt.get_rect(center=(config.SCREEN_WIDTH // 2, 60)).inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect);
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, width=2)
            self.screen.blit(txt, txt.get_rect(center=(config.SCREEN_WIDTH // 2, 60)))

        if self.interaction_mode == 'move_robber':
            font = pygame.font.SysFont('Arial', 36, bold=True)
            txt = font.render("MOVE THE ROBBER!", True, (255, 0, 0))
            self.screen.blit(txt, (config.SCREEN_WIDTH // 2 - 150, 120))

        if self.game_phase == 'MAIN':
            if self.interaction_mode == 'trade':
                self.renderer.draw_trade_menu(self.trade_offer, self.get_current_player())
            elif self.interaction_mode == 'monopoly':
                self.renderer.draw_monopoly_menu()
            elif self.interaction_mode == 'year_of_plenty':
                self.renderer.draw_yop_menu(len(self.yop_selected_resources))

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
    game = DemoGame()
    game.run()