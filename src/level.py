import pygame
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self):
        # 先用纯色+几条线模拟街道
        self.bg_color = (30, 30, 40)

    def draw(self, surface):
        surface.fill(self.bg_color)

        # 画“马路”
        lane_top = HEIGHT * 0.5
        lane_bottom = HEIGHT * 0.9
        pygame.draw.rect(surface, (60, 60, 80),
                         (0, lane_top, WIDTH, lane_bottom - lane_top))

        # 画远景地平线
        pygame.draw.line(surface, (90, 90, 120),
                         (0, lane_top), (WIDTH, lane_top), 2)
