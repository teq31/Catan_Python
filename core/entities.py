import math
import config

class HexTile:
    def __init__(self, q, r, resource_type, number_token=None):
        self.q = q
        self.r = r
        self.resource_type = resource_type
        self.number_token = number_token
        self.is_highlighted = False
        self.pixel_x, self.pixel_y = self._calculate_pixel_center()
        self.has_robber = False

    def _calculate_pixel_center(self):
        size = config.HEX_RADIUS
        center_offset_x = config.SCREEN_WIDTH // 2
        center_offset_y = config.SCREEN_HEIGHT // 2

        x = size * math.sqrt(3) * (self.q + self.r / 2)
        y = size * (3 / 2) * self.r
        return (x + center_offset_x, y + center_offset_y)

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            px = self.pixel_x + config.HEX_RADIUS * math.cos(angle_rad)
            py = self.pixel_y + config.HEX_RADIUS * math.sin(angle_rad)
            vertices.append((px, py))
        return vertices

    def contains_point(self, x, y):
        dist = math.sqrt((x - self.pixel_x) ** 2 + (y - self.pixel_y) ** 2)
        return dist < (config.HEX_RADIUS * 0.85)

    def get_nearest_vertex(self, x, y):

        vertices = self.get_vertices()
        best_dist = float('inf')
        best_point = None

        for v in vertices:
            dist = math.sqrt((x - v[0]) ** 2 + (y - v[1]) ** 2)
            if dist < best_dist:
                best_dist = dist
                best_point = v

        if best_dist < 20:
            return best_point
        return None

    def get_nearest_edge(self, x, y):

        vertices = self.get_vertices()
        best_dist = float('inf')
        best_edge = None

        for i in range(6):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % 6]

            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2

            dist = math.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)

            if dist < best_dist:
                best_dist = dist
                best_edge = (p1, p2)

        if best_dist < 20:
            return best_edge
        return None