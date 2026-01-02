import math
import config


class HexTile:
    def __init__(self, q, r, resource_type, number_token):
        self.q = q
        self.r = r
        self.resource_type = resource_type
        self.number_token = number_token

        self.pixel_x, self.pixel_y = self._hex_to_pixel(q, r)

        self.is_highlighted = False
        self.has_robber = False

    def _hex_to_pixel(self, q, r):
        size = config.HEX_RADIUS

        center_x = config.SCREEN_WIDTH // 2 + 130
        center_y = config.SCREEN_HEIGHT // 2

        x = center_x + size * math.sqrt(3) * (q + r / 2)
        y = center_y + size * 3 / 2 * r

        return x, y

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            vx = self.pixel_x + config.HEX_RADIUS * math.cos(angle_rad)
            vy = self.pixel_y + config.HEX_RADIUS * math.sin(angle_rad)
            vertices.append((vx, vy))
        return vertices

    def get_edges(self):
        verts = self.get_vertices()
        edges = []
        for i in range(len(verts)):
            p1 = verts[i]
            p2 = verts[(i + 1) % 6]
            edges.append((p1, p2))
        return edges

    def contains_point(self, x, y):
        dist = math.sqrt((x - self.pixel_x) ** 2 + (y - self.pixel_y) ** 2)
        return dist < config.HEX_RADIUS * 0.9

    def get_nearest_vertex(self, x, y):
        best_v = None
        min_dist = float('inf')
        for v in self.get_vertices():
            dist = math.sqrt((x - v[0]) ** 2 + (y - v[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_v = v
        if min_dist < 15: return best_v
        return None

    def get_nearest_edge(self, x, y):
        best_e = None
        min_dist = float('inf')
        for p1, p2 in self.get_edges():
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            dist = math.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_e = (p1, p2)
        if min_dist < 15: return best_e
        return None