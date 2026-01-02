import random
import pygame


class AIController:
    def __init__(self, game_instance):
        self.game = game_instance
        self.board = game_instance.board

    def wait(self, ms):
        pygame.time.delay(ms)
        self.game.draw()

    def run_setup_turn(self, player):
        self.game.set_message(f"AI ({player.name}) is thinking...", duration=500)
        self.wait(500)

        if self.game.setup_subphase == 'SETTLEMENT':
            valid_spots = self.board.get_all_possible_settlement_spots(player, initial_phase=True)
            if valid_spots:
                target = random.choice(valid_spots)
                if self.board.place_settlement(target, player, initial_phase=True):
                    self.game.set_message("AI placed a Settlement!", duration=1000)
                    self.wait(1000)
                    self.game.rules_manager.advance_setup_step()
            else:
                print("AI ERROR: No settlement spots found!")
                self.game.rules_manager.advance_setup_step()

        elif self.game.setup_subphase == 'ROAD':
            valid_spots = self.board.get_all_possible_road_spots(player)
            if valid_spots:
                target = random.choice(valid_spots)
                if self.board.place_road(target, player):
                    self.game.set_message("AI placed a Road!", duration=1000)
                    self.wait(1000)
                    self.game.rules_manager.advance_setup_step()
            else:
                print("AI WARNING: No valid road spots found (Math error?). Skipping road.")
                self.game.set_message("AI skips road (Map Error)", 1000)
                self.wait(1000)
                self.game.rules_manager.advance_setup_step()

    def run_main_turn(self, player):

        if player.dev_cards['knight'] > 0 and random.random() < 0.3:
            self.game.rules_manager.play_dev_card('knight')

        if not self.game.dice_rolled_this_turn:
            self.game.set_message(f"{player.name} is rolling dice...", duration=1000)
            self.wait(1000)

            d = random.randint(1, 6) + random.randint(1, 6)
            self.game.last_dice_roll = d
            self.game.dice_rolled_this_turn = True

            self.game.set_message(f"{player.name} Rolled: {d}", duration=1500)
            self.wait(1500)

            if d == 7:
                self.handle_robber_logic(player)
            else:
                self.board.distribute_resources(d)
                self.wait(500)

        self.handle_building_logic(player)

        self.game.set_message(f"{player.name} ends turn.", duration=1000)
        self.wait(1000)

        self.game.current_player_idx = (self.game.current_player_idx + 1) % len(self.game.players)
        self.game.dice_rolled_this_turn = False
        self.game.last_dice_roll = 0

    def handle_robber_logic(self, player):
        self.game.set_message(f"{player.name} moves the ROBBER!", duration=2000)
        self.wait(1000)

        valid_tiles = [t for t in self.board.tiles if not t.has_robber]
        if valid_tiles:
            target = random.choice(valid_tiles)
            self.board.move_robber(target)
            self.game.set_message(f"AI blocked {target.resource_type.upper()}!", duration=2000)
            self.wait(2000)

    def handle_building_logic(self, player):
        if player.can_afford('city'):
            for s in player.settlements:
                if self.board.upgrade_to_city(s, player):
                    player.deduct_resources('city')
                    self.game.set_message("AI built a CITY!", duration=1500)
                    self.wait(1500)
                    return

        if player.can_afford('settlement'):
            spots = self.board.get_all_possible_settlement_spots(player)
            if spots:
                if self.board.place_settlement(random.choice(spots), player):
                    player.deduct_resources('settlement')
                    self.game.set_message("AI built a SETTLEMENT!", duration=1500)
                    self.wait(1500)
                    return

        if player.can_afford('road'):
            spots = self.board.get_all_possible_road_spots(player)
            if spots:
                if self.board.place_road(random.choice(spots), player):
                    player.deduct_resources('road')
                    self.game.set_message("AI built a ROAD!", duration=1500)
                    self.wait(1500)
                    self.game.rules_manager.check_achievements()