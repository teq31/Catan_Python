import random


class RulesManager:
    def __init__(self, game):
        self.game = game

    def check_achievements(self):
        largest_holder = None
        max_knights = 2
        for p in self.game.players:
            if p.has_largest_army: largest_holder = p
            if p.knights_played > max_knights: max_knights = p.knights_played

        for p in self.game.players:
            if p.knights_played == max_knights and max_knights >= 3:
                if largest_holder != p:
                    if largest_holder: largest_holder.has_largest_army = False
                    p.has_largest_army = True
                    self.game.set_message(f"{p.name} takes LARGEST ARMY!", 2000)
                break

        longest_holder = None
        max_road = 4
        for p in self.game.players:
            if p.has_longest_road: longest_holder = p

        for p in self.game.players:
            length = self.game.board.calculate_longest_road(p)
            p.road_length = length
            if length > max_road: max_road = length

        for p in self.game.players:
            if p.road_length == max_road and max_road >= 5:
                if longest_holder != p:
                    if longest_holder: longest_holder.has_longest_road = False
                    p.has_longest_road = True
                    self.game.set_message(f"{p.name} takes LONGEST ROAD ({max_road})!", 2000)

    def play_dev_card(self, card_type):
        player = self.game.get_current_player()
        if player.dev_cards[card_type] <= 0:
            self.game.set_message(f"No {card_type} card!", 1000)
            return

        if player.is_ai:
            player.dev_cards[card_type] -= 1
            if card_type == 'knight':
                player.knights_played += 1
                valid_tiles = [t for t in self.game.board.tiles if not t.has_robber]
                if valid_tiles:
                    target = random.choice(valid_tiles)
                    self.game.board.move_robber(target)
                    self.execute_robber_theft(target)
                self.check_achievements()
            elif card_type == 'year_of_plenty':
                player.add_resource('wood', 1);
                player.add_resource('wheat', 1)
                self.game.set_message("AI used Year of Plenty", 1500)
            elif card_type == 'monopoly':
                self.execute_monopoly('sheep')
                self.game.set_message("AI used Monopoly on Sheep!", 1500)
            elif card_type == 'road_building':
                player.add_resource('wood', 2);
                player.add_resource('brick', 2)
                self.game.set_message("AI used Road Building", 1500)
            return

        if card_type == 'knight':
            player.dev_cards[card_type] -= 1
            player.knights_played += 1
            self.game.interaction_mode = 'move_robber'
            self.game.set_message("Knight played! Move Robber.", 2000)
            self.check_achievements()

        elif card_type == 'monopoly':
            self.game.interaction_mode = 'monopoly'
            self.game.set_message("Choose resource to STEAL!", 2000)

        elif card_type == 'year_of_plenty':
            self.game.yop_selected_resources = []
            self.game.interaction_mode = 'year_of_plenty'
            self.game.set_message("Choose 2 resources!", 2000)

        elif card_type == 'road_building':
            player.dev_cards[card_type] -= 1
            player.add_resource('wood', 2)
            player.add_resource('brick', 2)
            self.game.set_message("Road Building: +2 Wood, +2 Brick", 2000)

    def execute_monopoly(self, resource_type):
        player = self.game.get_current_player()
        total_stolen = 0
        for other in self.game.players:
            if other != player:
                amt = other.resources[resource_type]
                other.resources[resource_type] = 0
                total_stolen += amt
        player.resources[resource_type] += total_stolen
        return total_stolen

    def execute_robber_theft(self, tile):
        current_player = self.game.get_current_player()
        potential_victims = self.game.board.get_players_on_tile(tile)

        if current_player in potential_victims:
            potential_victims.remove(current_player)

        valid_victims = [p for p in potential_victims if sum(p.resources.values()) > 0]

        if not valid_victims:
            self.game.set_message("Robber moved. No one to steal from!", 2000)
            return

        victim = random.choice(valid_victims)
        victim_hand = []
        for res, count in victim.resources.items():
            victim_hand.extend([res] * count)

        stolen_res = random.choice(victim_hand)
        victim.resources[stolen_res] -= 1
        current_player.resources[stolen_res] += 1

        msg = f"Stole 1 {stolen_res.upper()} from {victim.name}!"
        self.game.set_message(msg, 3000)

    def execute_p2p_trade(self, p1, p2, give_dict, get_dict):
        for res, amt in give_dict.items():
            p1.resources[res] -= amt
            p2.resources[res] += amt

        for res, amt in get_dict.items():
            p2.resources[res] -= amt
            p1.resources[res] += amt

        self.game.set_message(f"Trade successful with {p2.name}!", 2500)

    def advance_setup_step(self):
        player = self.game.get_current_player()

        if self.game.setup_subphase == 'SETTLEMENT':
            self.game.setup_subphase = 'ROAD'
            self.game.set_message(f"{player.name}: Place Road")
        else:
            half_way = len(self.game.setup_order) // 2
            if self.game.setup_step_idx >= half_way:
                last_settlement = player.settlements[-1]
                resources = self.game.board.get_resources_from_node(last_settlement)
                for r in resources: player.add_resource(r, 1)

            self.game.setup_step_idx += 1
            if self.game.setup_step_idx >= len(self.game.setup_order):
                self.game.game_phase = 'MAIN'
                self.game.current_player_idx = 0
                self.game.set_message("MAIN GAME START! Press R to Roll.")
            else:
                self.game.current_player_idx = self.game.setup_order[self.game.setup_step_idx]
                self.game.setup_subphase = 'SETTLEMENT'
                self.game.set_message(f"{self.game.players[self.game.current_player_idx].name}: Place Settlement")