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
                self.game.rules_manager.execute_robber_theft(selected_hex)

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

        if self.game.interaction_mode == 'p2p_trade':
            if event.key == pygame.K_ESCAPE:
                self.game.interaction_mode = 'view'
                self._reset_p2p()

            elif event.key == pygame.K_TAB:
                if self.game.p2p_active_side == 'give':
                    self.game.p2p_active_side = 'get'
                else:
                    self.game.p2p_active_side = 'give'

            elif event.key == pygame.K_SPACE:
                start_idx = self.game.p2p_target_idx
                while True:
                    self.game.p2p_target_idx = (self.game.p2p_target_idx + 1) % len(self.game.players)
                    if self.game.p2p_target_idx != self.game.current_player_idx:
                        break
                    if self.game.p2p_target_idx == start_idx: break

            elif event.key in [pygame.K_w, pygame.K_b, pygame.K_s, pygame.K_g, pygame.K_o]:
                self._handle_p2p_selection(event.key)

            elif event.key == pygame.K_RETURN:
                target_player = self.game.players[self.game.p2p_target_idx]
                give = self.game.p2p_offer['give']
                get = self.game.p2p_offer['get']

                valid_offer = True
                for res, amt in give.items():
                    if player.resources.get(res, 0) < amt: valid_offer = False

                if not valid_offer:
                    self.game.set_message("You don't have these resources!", 2000)
                elif not give and not get:
                    self.game.set_message("Empty offer!", 1000)
                else:
                    if target_player.is_ai:
                        accepted, msg = self.game.ai_brain.evaluate_trade_offer_specific(target_player, give, get)
                        if accepted:
                            self.game.rules_manager.execute_p2p_trade(player, target_player, give, get)
                            self.game.interaction_mode = 'view'
                            self._reset_p2p()
                        else:
                            self.game.set_message(f"{target_player.name} refused.", 2000)
                    else:
                        target_valid = True
                        for res, amt in get.items():
                            if target_player.resources.get(res, 0) < amt: target_valid = False

                        if not target_valid:
                            self.game.set_message(f"{target_player.name} can't afford this!", 2000)
                        else:
                            self.game.interaction_mode = 'p2p_confirm'
            return

        if self.game.interaction_mode == 'p2p_confirm':
            target_player = self.game.players[self.game.p2p_target_idx]
            if event.key == pygame.K_y:
                self.game.rules_manager.execute_p2p_trade(player, target_player, self.game.p2p_offer['give'],
                                                          self.game.p2p_offer['get'])
                self.game.interaction_mode = 'view'
                self._reset_p2p()
            elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                self.game.interaction_mode = 'p2p_trade'
                self.game.set_message(f"{target_player.name} declined.", 2000)
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
            # MODIFICARE: Permitem deschiderea meniului indiferent de resurse
            # Validarea se face cand selectezi resursa in _handle_special_keys
            self.game.interaction_mode = 'trade'
            self.game.trade_offer = None

        elif event.key == pygame.K_p:
            self.game.interaction_mode = 'p2p_trade'
            self._reset_p2p()
            self.game.p2p_target_idx = (self.game.current_player_idx + 1) % len(self.game.players)

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

    def _handle_p2p_selection(self, key):
        res_map = {pygame.K_w: 'wood', pygame.K_b: 'brick', pygame.K_s: 'sheep', pygame.K_g: 'wheat', pygame.K_o: 'ore'}
        res = res_map[key]
        side = self.game.p2p_active_side
        current_dict = self.game.p2p_offer[side]
        current_dict[res] = current_dict.get(res, 0) + 1

    def _reset_p2p(self):
        self.game.p2p_offer = {'give': {}, 'get': {}}
        self.game.p2p_active_side = 'give'