import config


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.resources = {
            'wood': 0, 'brick': 0, 'sheep': 0, 'wheat': 0, 'ore': 0
        }

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

        self.victory_points = 0

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
        if self.resources.get(give_res, 0) >= 4:
            self.resources[give_res] -= 4
            self.resources[get_res] += 1
            return True
        return False

    def update_victory_points(self):
        points = 0
        points += len(self.settlements) * 1
        points += len(self.cities) * 2
        points += self.dev_cards['vp'] * 1

        self.victory_points = points
        return self.victory_points