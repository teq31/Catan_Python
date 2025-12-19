import random
from core.entities import HexTile


class Board:
    def __init__(self):
        self.tiles = []
        self.radius = 2

    def generate_random_board(self):

        coords = self._get_hex_grid_coords()

        resources = self._get_shuffled_resources()

        numbers = self._get_shuffled_numbers()

        self.tiles = []

        for q, r in coords:
            res_type = resources.pop()

            if res_type == 'desert':
                num_token = None
            else:
                num_token = numbers.pop()

            new_tile = HexTile(q, r, res_type, num_token)
            self.tiles.append(new_tile)

        print(f"The map has been generated with {len(self.tiles)} tiles.")

    def _get_hex_grid_coords(self):
        coords = []
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                if -self.radius <= q + r <= self.radius:
                    coords.append((q, r))
        return coords

    def _get_shuffled_resources(self):
        deck = (
                ['wood'] * 4 +
                ['sheep'] * 4 +
                ['wheat'] * 4 +
                ['brick'] * 3 +
                ['ore'] * 3 +
                ['desert'] * 1
        )
        random.shuffle(deck)
        return deck

    def _get_shuffled_numbers(self):
        tokens = [2, 12]
        tokens += [3, 4, 5, 6, 8, 9, 10, 11] * 2

        random.shuffle(tokens)
        return tokens

    def debug_print(self):
        for tile in self.tiles:
            print(tile)