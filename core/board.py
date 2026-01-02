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
        self.ports = []

    def generate_random_board(self):
        coords = self._get_hex_grid_coords()
        resources = self._get_shuffled_resources()
        numbers = self._get_shuffled_numbers()
        self.tiles = []

        for q, r in coords:
            res_type = resources.pop()
            if res_type == 'desert':
                new_tile = HexTile(q, r, res_type, None)
                new_tile.has_robber = True
            else:
                new_tile = HexTile(q, r, res_type, numbers.pop())
            self.tiles.append(new_tile)

        self._generate_ports()
        self._initialize_dev_deck()

    def _generate_ports(self):
        self.ports = []
        port_types = ['wood', 'brick', 'sheep', 'wheat', 'ore'] + ['3:1'] * 4
        random.shuffle(port_types)

        outer_tiles = []
        tile_map = {(t.q, t.r): t for t in self.tiles}
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for t in self.tiles:
            neighbors = 0
            for dq, dr in directions:
                if (t.q + dq, t.r + dr) in tile_map: neighbors += 1
            if neighbors < 6:
                outer_tiles.append(t)

        possible_edges = []
        for t in outer_tiles:
            edges = t.get_edges()
            for e in edges:
                is_shared = False
                for other in self.tiles:
                    if other == t: continue
                    other_edges = other.get_edges()
                    e_int = tuple(sorted([(int(p[0]), int(p[1])) for p in e]))
                    for oe in other_edges:
                        oe_int = tuple(sorted([(int(p[0]), int(p[1])) for p in oe]))
                        if e_int == oe_int:
                            is_shared = True;
                            break
                if not is_shared:
                    possible_edges.append(e)

        random.shuffle(possible_edges)
        count = min(len(port_types), len(possible_edges))
        step = 2 if len(possible_edges) >= count * 2 else 1

        idx_edge = 0
        for i in range(count):
            if idx_edge >= len(possible_edges): break
            ptype = port_types[i]
            edge = possible_edges[idx_edge]
            self.ports.append({'edge': edge, 'type': ptype})
            idx_edge += step

    def _initialize_dev_deck(self):
        self.dev_card_deck = ['knight'] * 14 + ['vp'] * 5 + ['road_building'] * 2 + ['year_of_plenty'] * 2 + [
            'monopoly'] * 2
        random.shuffle(self.dev_card_deck)

    def draw_dev_card(self):
        return self.dev_card_deck.pop() if self.dev_card_deck else None

    def _get_hex_grid_coords(self):
        coords = []
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                if -self.radius <= q + r <= self.radius: coords.append((q, r))
        return coords

    def _get_shuffled_resources(self):
        deck = ['wood'] * 4 + ['sheep'] * 4 + ['wheat'] * 4 + ['brick'] * 3 + ['ore'] * 3 + ['desert'] * 1
        random.shuffle(deck);
        return deck

    def _get_shuffled_numbers(self):
        tokens = [2, 12] + [3, 4, 5, 6, 8, 9, 10, 11] * 2
        random.shuffle(tokens);
        return tokens

    def move_robber(self, target_hex):
        for tile in self.tiles: tile.has_robber = False
        target_hex.has_robber = True

    def distribute_resources(self, roll_number):
        target_tiles = [t for t in self.tiles if t.number_token == roll_number]
        for tile in target_tiles:
            if tile.has_robber: continue
            for vx, vy in tile.get_vertices():
                for loc, owner in self.built_settlements.items():
                    if math.sqrt((vx - loc[0]) ** 2 + (vy - loc[1]) ** 2) < 5: owner.add_resource(tile.resource_type, 1)
                for loc, owner in self.built_cities.items():
                    if math.sqrt((vx - loc[0]) ** 2 + (vy - loc[1]) ** 2) < 5: owner.add_resource(tile.resource_type, 2)

    def _is_near(self, p1, p2, threshold=5):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < threshold

    def place_settlement(self, node_coords, player, initial_phase=False):
        for existing in list(self.built_settlements.keys()) + list(self.built_cities.keys()):
            if self._is_near(node_coords, existing, 5): return False  # Ocupat
            if self._is_near(node_coords, existing, 50): return False  # Prea aproape (regula distanta)

        if not initial_phase:
            connected = False
            for edge, owner in self.built_roads.items():
                if owner == player:
                    if self._is_near(edge[0], node_coords) or self._is_near(edge[1], node_coords):
                        connected = True;
                        break
            if not connected: return False

        self.built_settlements[node_coords] = player
        player.settlements.append(node_coords)

        for port in self.ports:
            p1, p2 = port['edge']
            if self._is_near(node_coords, p1) or self._is_near(node_coords, p2):
                player.update_trade_ratios(port['type'])

        return True

    def place_road(self, edge_coords, player):
        p1, p2 = edge_coords

        for existing, owner in self.built_roads.items():
            e1, e2 = existing
            match1 = (self._is_near(p1, e1) and self._is_near(p2, e2))
            match2 = (self._is_near(p1, e2) and self._is_near(p2, e1))
            if match1 or match2: return False

        connected = False

        for loc, owner in self.built_settlements.items():
            if owner == player and (self._is_near(p1, loc) or self._is_near(p2, loc)): connected = True; break
        if not connected:
            for loc, owner in self.built_cities.items():
                if owner == player and (self._is_near(p1, loc) or self._is_near(p2, loc)): connected = True; break

        if not connected:
            for existing, owner in self.built_roads.items():
                if owner == player:
                    e1, e2 = existing
                    if self._is_near(p1, e1) or self._is_near(p1, e2) or self._is_near(p2, e1) or self._is_near(p2, e2):
                        connected = True;
                        break

        if not connected: return False

        self.built_roads[edge_coords] = player
        player.roads.append(edge_coords)
        return True

    def upgrade_to_city(self, node_coords, player):
        target_node = None
        for loc, owner in self.built_settlements.items():
            if owner == player and self._is_near(node_coords, loc):
                target_node = loc
                break

        if target_node:
            del self.built_settlements[target_node]
            self.built_cities[target_node] = player
            player.cities.append(target_node)
            return True
        return False

    def get_all_possible_settlement_spots(self, player, initial_phase=False):
        valid = []
        for tile in self.tiles:
            for v in tile.get_vertices():
                if self.place_settlement(v, player, initial_phase):
                    if v in self.built_settlements: del self.built_settlements[v]
                    if v in player.settlements: player.settlements.remove(v)
                    valid.append(v)
        return valid

    def get_all_possible_road_spots(self, player):
        valid = []
        for tile in self.tiles:
            for e in tile.get_edges():
                if self.place_road(e, player):
                    # Revert
                    if e in self.built_roads: del self.built_roads[e]
                    if e in player.roads: player.roads.remove(e)
                    valid.append(e)
        return valid

    def get_resources_from_node(self, node):
        res = []
        for tile in self.tiles:
            if tile.resource_type == 'desert': continue
            for v in tile.get_vertices():
                if self._is_near(v, node): res.append(tile.resource_type)
        return res

    def calculate_longest_road(self, player):
        roads = [e for e, o in self.built_roads.items() if o == player]
        if not roads: return 0

        def to_key(p):
            return (int(p[0]), int(p[1]))

        adj = {}
        for p1, p2 in roads:
            k1, k2 = to_key(p1), to_key(p2)
            adj.setdefault(k1, []).append(k2)
            adj.setdefault(k2, []).append(k1)

        max_len = 0

        def dfs(curr, visited, length):
            nonlocal max_len
            max_len = max(max_len, length)
            for neigh in adj.get(curr, []):
                edge = tuple(sorted((curr, neigh)))
                if edge not in visited:
                    visited.add(edge)
                    dfs(neigh, visited, length + 1)
                    visited.remove(edge)

        for start_node in adj:
            dfs(start_node, set(), 0)

        return max_len