import pygame
from settings import WIDTH, HEIGHT, PLAYER_SPEED, PLAYER_ATTACK_COOLDOWN

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        # 暂时用方块代替角色
        self.image = pygame.Surface((40, 80))
        self.image.fill((0, 200, 50))
        self.rect = self.image.get_rect()
        # 起始放在左下方
        self.rect.midbottom = (WIDTH * 0.2, HEIGHT * 0.8)

        self.level = level
        self.speed = PLAYER_SPEED
        self.attack_cooldown = 0
        self.is_attacking = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed

        # 简单的“走道”限制：只允许在中间一条带内上下
        lane_top = HEIGHT * 0.5
        lane_bottom = HEIGHT * 0.9

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > lane_bottom:
            self.rect.bottom = lane_bottom
        if self.rect.top < lane_top:
            self.rect.top = lane_top

    def update_attack(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:  # 攻击键
            if self.attack_cooldown <= 0:
                self.is_attacking = True
                self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        else:
            self.is_attacking = False

    def get_attack_hitbox(self):
        if not self.is_attacking:
            return None
        # 在角色前方生成一个矩形当作拳头/脚
        if self.rect.centerx < WIDTH / 2:
            # 面向右
            return pygame.Rect(self.rect.right,
                               self.rect.top,
                               40,
                               self.rect.height)
        else:
            # 简单：假设在右边就面向左
            return pygame.Rect(self.rect.left - 40,
                               self.rect.top,
                               40,
                               self.rect.height)

    def update(self, dt):
        self.handle_input()
        self.update_attack(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # 调试：画出攻击框
        hitbox = self.get_attack_hitbox()
        if hitbox:
            pygame.draw.rect(surface, (255, 255, 0), hitbox, 2)
