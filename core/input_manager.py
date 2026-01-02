import pygame
import sys
import random


class InputManager:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        player = self.game.get_current_player()

        if player.is_ai:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(player)

            if event.type == pygame.KEYDOWN and self.game.game_phase == 'MAIN':
                self._handle_keyboard(event, player)

    def _handle_mouse_click(self, player):
        mx, my = pygame.mouse.get_pos()

        if self.game.game_phase == 'SETUP':
            hovered_vertex = None
            hovered_edge = None

            for tile in self.game.board.tiles:
                if self.game.setup_subphase == 'SETTLEMENT':
                    v = tile.get_nearest_vertex(mx, my)
                    if v: hovered_vertex = v
                elif self.game.setup_subphase == 'ROAD':
                    e = tile.get_nearest_edge(mx, my)
                    if e: hovered_edge = e

            if self.game.setup_subphase == 'SETTLEMENT' and hovered_vertex:
                if self.game.board.place_settlement(hovered_vertex, player, initial_phase=True):
                    self.game.rules_manager.advance_setup_step()
            elif self.game.setup_subphase == 'ROAD' and hovered_edge:
                if self.game.board.place_road(hovered_edge, player):
                    self.game.rules_manager.advance_setup_step()

        elif self.game.game_phase == 'MAIN':
            hovered_vertex = None
            hovered_edge = None
            selected_hex = None
            for tile in self.game.board.tiles:
                if tile.contains_point(mx, my): selected_hex = tile
                v = tile.get_nearest_vertex(mx, my);
                if v: hovered_vertex = v
                e = tile.get_nearest_edge(mx, my);
                if e: hovered_edge = e

            if self.game.interaction_mode == 'move_robber' and selected_hex:
                self.game.board.move_robber(selected_hex)
                self.game.interaction_mode = 'view'
                self.game.set_message("Robber moved!", 1500)

            elif self.game.interaction_mode == 'build_settlement' and hovered_vertex:
                if player.can_afford('settlement'):
                    if self.game.board.place_settlement(hovered_vertex, player):
                        player.deduct_resources('settlement')

            elif self.game.interaction_mode == 'build_road' and hovered_edge:
                if player.can_afford('road'):
                    if self.game.board.place_road(hovered_edge, player):
                        player.deduct_resources('road')
                        self.game.rules_manager.check_achievements()

            elif self.game.interaction_mode == 'build_city' and hovered_vertex:
                if player.can_afford('city'):
                    if self.game.board.upgrade_to_city(hovered_vertex, player):
                        player.deduct_resources('city')

    def _handle_keyboard(self, event, player):
        if self.game.interaction_mode in ['monopoly', 'year_of_plenty', 'trade']:
            if event.key == pygame.K_ESCAPE:
                self.game.interaction_mode = 'view'
                self.game.trade_offer = None
            elif event.key in [pygame.K_w, pygame.K_b, pygame.K_s, pygame.K_g, pygame.K_o]:
                self._handle_special_keys(event.key, player)
            return

        key_map = {
            pygame.K_s: self.game.storage_manager.save_game,
            pygame.K_l: self.game.storage_manager.load_game,
            pygame.K_1: lambda: setattr(self.game, 'interaction_mode', 'build_settlement'),
            pygame.K_2: lambda: setattr(self.game, 'interaction_mode', 'build_road'),
            pygame.K_3: lambda: setattr(self.game, 'interaction_mode', 'build_city'),
            pygame.K_k: lambda: self.game.rules_manager.play_dev_card('knight'),
            pygame.K_m: lambda: self.game.rules_manager.play_dev_card('monopoly'),
            pygame.K_y: lambda: self.game.rules_manager.play_dev_card('year_of_plenty'),
            pygame.K_u: lambda: self.game.rules_manager.play_dev_card('road_building'),
        }

        if event.key in key_map:
            key_map[event.key]()

        elif event.key == pygame.K_4:
            if player.can_afford('dev_card'):
                c = self.game.board.draw_dev_card()
                if c:
                    player.deduct_resources('dev_card')
                    player.dev_cards[c] += 1
                    self.game.set_message(f"Bought: {c.upper()}", 2000)

        elif event.key == pygame.K_t:
            can_trade = any(c >= 4 for c in
                            player.resources.values())
            min_ratio = min(player.trade_ratios.values())
            can_trade = any(c >= min_ratio for c in player.resources.values())

            if can_trade:
                self.game.interaction_mode = 'trade'
                self.game.trade_offer = None
            else:
                self.game.set_message("Not enough resources to trade!", 2000)

        elif event.key == pygame.K_r:
            if not self.game.dice_rolled_this_turn:
                d = random.randint(1, 6) + random.randint(1, 6)
                self.game.last_dice_roll = d
                self.game.dice_rolled_this_turn = True
                self.game.set_message(f"{player.name} Rolled: {d}", 1500)

                if d == 7:
                    self.game.interaction_mode = 'move_robber'
                    self.game.set_message("ROBBER! Click a hex.", 3000)
                else:
                    self.game.board.distribute_resources(d)

        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.game.dice_rolled_this_turn:
                self.game.current_player_idx = (self.game.current_player_idx + 1) % len(self.game.players)
                self.game.dice_rolled_this_turn = False
                self.game.last_dice_roll = 0

    def _handle_special_keys(self, key, player):
        res_map = {pygame.K_w: 'wood', pygame.K_b: 'brick', pygame.K_s: 'sheep', pygame.K_g: 'wheat', pygame.K_o: 'ore'}
        sel = res_map[key]

        if self.game.interaction_mode == 'monopoly':
            player.dev_cards['monopoly'] -= 1
            stolen = self.game.rules_manager.execute_monopoly(sel)
            self.game.set_message(f"Monopoly! Stole {stolen} {sel.upper()}", 2500)
            self.game.interaction_mode = 'view'

        elif self.game.interaction_mode == 'year_of_plenty':
            self.game.yop_selected_resources.append(sel)
            if len(self.game.yop_selected_resources) == 2:
                player.dev_cards['year_of_plenty'] -= 1
                for r in self.game.yop_selected_resources:
                    player.add_resource(r, 1)
                self.game.set_message(f"YoP: Added Resources", 2500)
                self.game.interaction_mode = 'view'

        elif self.game.interaction_mode == 'trade':
            if not self.game.trade_offer:
                cost = player.trade_ratios.get(sel, 4)
                if cost > player.general_port_ratio: cost = player.general_port_ratio

                if player.resources[sel] >= cost:
                    self.game.trade_offer = sel
                else:
                    self.game.set_message(f"Need {cost} {sel.upper()}!", 1000)
            else:
                player.trade_with_bank(self.game.trade_offer, sel)
                self.game.set_message(f"Traded!", 1500)
                self.game.trade_offer = None
                self.game.interaction_mode = 'view'