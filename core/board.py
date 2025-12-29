import math
import random
from core.entities import HexTile


class Board:
    def __init__(self):
        self.tiles = []
        self.radius = 2

        self.built_settlements = {}
        self.built_cities = {}
        self.built_roads = {}

        self.dev_card_deck = []

    def generate_random_board(self):
        coords = self._get_hex_grid_coords()
        resources = self._get_shuffled_resources()
        numbers = self._get_shuffled_numbers()
        self.tiles = []
        for q, r in coords:
            res_type = resources.pop()
            if res_type == 'desert':
                num_token = None
                new_tile = HexTile(q, r, res_type, num_token)
                new_tile.has_robber = True
            else:
                num_token = numbers.pop()
                new_tile = HexTile(q, r, res_type, num_token)

            self.tiles.append(new_tile)

        self._initialize_dev_deck()
        print(f"Map generated. Deck size: {len(self.dev_card_deck)}")

    def _initialize_dev_deck(self):
        self.dev_card_deck = []
        self.dev_card_deck += ['knight'] * 14
        self.dev_card_deck += ['vp'] * 5
        self.dev_card_deck += ['road_building'] * 2
        self.dev_card_deck += ['year_of_plenty'] * 2
        self.dev_card_deck += ['monopoly'] * 2
        random.shuffle(self.dev_card_deck)

    def draw_dev_card(self):
        if len(self.dev_card_deck) > 0:
            return self.dev_card_deck.pop()
        return None

    def _get_hex_grid_coords(self):
        coords = []
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                if -self.radius <= q + r <= self.radius:
                    coords.append((q, r))
        return coords

    def _get_shuffled_resources(self):
        deck = ['wood'] * 4 + ['sheep'] * 4 + ['wheat'] * 4 + ['brick'] * 3 + ['ore'] * 3 + ['desert'] * 1
        random.shuffle(deck)
        return deck

    def _get_shuffled_numbers(self):
        tokens = [2, 12] + [3, 4, 5, 6, 8, 9, 10, 11] * 2
        random.shuffle(tokens)
        return tokens

    def move_robber(self, target_hex):
        for tile in self.tiles:
            tile.has_robber = False
        target_hex.has_robber = True

    def distribute_resources(self, roll_number):
        target_tiles = [t for t in self.tiles if t.number_token == roll_number]
        for tile in target_tiles:
            if tile.has_robber:
                print(f"BLOCKED! Robber is on {tile.resource_type}")
                continue

            res_type = tile.resource_type
            vertices = tile.get_vertices()

            for vx, vy in vertices:
                for loc, owner in self.built_settlements.items():
                    if math.sqrt((vx - loc[0]) ** 2 + (vy - loc[1]) ** 2) < 5:
                        owner.add_resource(res_type, 1)

                for loc, owner in self.built_cities.items():
                    if math.sqrt((vx - loc[0]) ** 2 + (vy - loc[1]) ** 2) < 5:
                        owner.add_resource(res_type, 2)

    def place_settlement(self, node_coords, player, initial_phase=False):
        if node_coords in self.built_settlements or node_coords in self.built_cities: return False
        for existing_node in list(self.built_settlements.keys()) + list(self.built_cities.keys()):
            if math.sqrt(
                (node_coords[0] - existing_node[0]) ** 2 + (node_coords[1] - existing_node[1]) ** 2) < 50: return False

        self.built_settlements[node_coords] = player
        player.settlements.append(node_coords)
        return True

    def place_road(self, edge_coords, player):
        p1, p2 = edge_coords
        if (p1, p2) in self.built_roads or (p2, p1) in self.built_roads: return False
        self.built_roads[edge_coords] = player
        player.roads.append(edge_coords)
        return True

    def upgrade_to_city(self, node_coords, player):
        if self.built_settlements.get(node_coords) == player:
            del self.built_settlements[node_coords]
            self.built_cities[node_coords] = player
            player.cities.append(node_coords)
            return True
        return False