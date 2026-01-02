import config


class Player:
    def __init__(self, name, color, is_ai=False):
        self.name = name
        self.color = color
        self.is_ai = is_ai

        self.resources = {
            'wood': 0, 'brick': 0, 'sheep': 0, 'wheat': 0, 'ore': 0
        }

        self.trade_ratios = {
            'wood': 4, 'brick': 4, 'sheep': 4, 'wheat': 4, 'ore': 4
        }
        self.general_port_ratio = 4

        self.settlements = []
        self.cities = []
        self.roads = []

        self.dev_cards = {
            'knight': 0,
            'vp': 0,
            'road_building': 0,
            'year_of_plenty': 0,
            'monopoly': 0
        }

        self.knights_played = 0
        self.has_largest_army = False
        self.has_longest_road = False
        self.road_length = 0

        self.victory_points = 0

    def update_trade_ratios(self, port_type):
        if port_type == '3:1':
            if self.general_port_ratio > 3:
                self.general_port_ratio = 3

            for res in self.trade_ratios:
                if self.trade_ratios[res] == 4:
                    self.trade_ratios[res] = 3
        else:
            if port_type in self.trade_ratios:
                self.trade_ratios[port_type] = 2

    def can_afford(self, building_type):
        costs = {
            'road': {'wood': 1, 'brick': 1},
            'settlement': {'wood': 1, 'brick': 1, 'wheat': 1, 'sheep': 1},
            'city': {'wheat': 2, 'ore': 3},
            'dev_card': {'sheep': 1, 'wheat': 1, 'ore': 1}
        }
        cost = costs.get(building_type)
        if not cost: return False

        for res, amount in cost.items():
            if self.resources[res] < amount:
                return False
        return True

    def deduct_resources(self, building_type):
        costs = {
            'road': {'wood': 1, 'brick': 1},
            'settlement': {'wood': 1, 'brick': 1, 'wheat': 1, 'sheep': 1},
            'city': {'wheat': 2, 'ore': 3},
            'dev_card': {'sheep': 1, 'wheat': 1, 'ore': 1}
        }
        cost = costs.get(building_type)
        if cost:
            for res, amount in cost.items():
                self.resources[res] -= amount

    def add_resource(self, resource, amount):
        if resource in self.resources:
            self.resources[resource] += amount

    def trade_with_bank(self, give_res, get_res):
        cost = self.trade_ratios.get(give_res, 4)

        if cost > self.general_port_ratio:
            cost = self.general_port_ratio

        if self.resources.get(give_res, 0) >= cost:
            self.resources[give_res] -= cost
            self.resources[get_res] += 1
            return True
        return False

    def update_victory_points(self):
        points = 0
        points += len(self.settlements) * 1
        points += len(self.cities) * 2
        points += self.dev_cards['vp'] * 1

        if self.has_largest_army: points += 2
        if self.has_longest_road: points += 2

        self.victory_points = points
        return self.victory_points