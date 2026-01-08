import pygame
import sys
import config

from core.board import Board
from core.player import Player
from core.ai import AIController
from core.input_manager import InputManager
from core.rules_manager import RulesManager
from core.storage_manager import StorageManager
from gui.renderer import BoardRenderer


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Catan - 4 Players Mode")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board()
        self.board.generate_random_board()

        p1 = Player("Human (Red)", (255, 50, 50), is_ai=False)
        p2 = Player("AI 1 (Blue)", (50, 50, 255), is_ai=True)
        p3 = Player("AI 2 (Green)", (34, 139, 34), is_ai=True)
        p4 = Player("AI 3 (Orange)", (255, 140, 0), is_ai=True)

        self.players = [p1, p2, p3, p4]

        self.renderer = BoardRenderer(self.screen)
        self.ai_brain = AIController(self)
        self.input_manager = InputManager(self)
        self.rules_manager = RulesManager(self)
        self.storage_manager = StorageManager(self)

        self.game_phase = 'SETUP'

        num_players = len(self.players)
        self.setup_order = list(range(num_players)) + list(range(num_players - 1, -1, -1))

        self.setup_step_idx = 0
        self.setup_subphase = 'SETTLEMENT'

        self.current_player_idx = self.setup_order[0]
        self.winner = None

        self.interaction_mode = 'view'
        self.trade_offer = None

        self.p2p_offer = {'give': {}, 'get': {}}
        self.p2p_active_side = 'give'
        self.p2p_target_idx = 0

        self.last_dice_roll = 0
        self.dice_rolled_this_turn = False
        self.yop_selected_resources = []
        self.message = "SETUP PHASE: Place Settlement"
        self.message_timer = 0

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def set_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration
        self.draw()

    def reinit_controllers(self):
        self.ai_brain = AIController(self)
        self.input_manager = InputManager(self)
        self.rules_manager = RulesManager(self)

    def update(self):
        if self.winner: return
        for p in self.players:
            if p.update_victory_points() >= 10: self.winner = p.name

        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            if self.game_phase == 'SETUP':
                self.message = f"SETUP: {self.get_current_player().name} place {self.setup_subphase}"
            else:
                self.message = ""

        curr = self.get_current_player()

        if curr.is_ai and not self.winner:
            if self.game_phase == 'SETUP':
                self.ai_brain.run_setup_turn(curr)
            else:
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
                if self.game_phase == 'SETUP':
                    if self.setup_subphase == 'SETTLEMENT': v = tile.get_nearest_vertex(mx,
                                                                                        my); self.hovered_vertex = v if v else None
                    if self.setup_subphase == 'ROAD': e = tile.get_nearest_edge(mx,
                                                                                my); self.hovered_edge = e if e else None
                elif self.interaction_mode not in ['move_robber', 'trade', 'monopoly', 'year_of_plenty', 'p2p_trade',
                                                   'p2p_confirm']:
                    if self.interaction_mode in ['build_settlement', 'build_city', 'view']: v = tile.get_nearest_vertex(
                        mx, my); self.hovered_vertex = v if v else None
                    if self.interaction_mode in ['build_road', 'view']: e = tile.get_nearest_edge(mx,
                                                                                                  my); self.hovered_edge = e if e else None
            else:
                tile.is_highlighted = False

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
            elif self.interaction_mode == 'p2p_trade':
                self.renderer.draw_p2p_menu(self)
            elif self.interaction_mode == 'p2p_confirm':
                self.renderer.draw_p2p_confirm(self)
            elif self.interaction_mode == 'monopoly':
                self.renderer.draw_monopoly_menu()
            elif self.interaction_mode == 'year_of_plenty':
                self.renderer.draw_yop_menu(len(self.yop_selected_resources))

        pygame.display.flip()

    def handle_events(self):
        self.input_manager.handle_input()

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