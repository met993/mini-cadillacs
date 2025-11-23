import pygame
import random
from settings import WIDTH, HEIGHT, ENEMY_SPEED, ENEMY_SPAWN_INTERVAL

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, player):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect()

        self.level = level
        self.player = player

        lane_top = HEIGHT * 0.5
        lane_bottom = HEIGHT * 0.9
        self.rect.midbottom = (
            random.choice([WIDTH + 50, -50]),      # 左右两边刷
            random.randint(int(lane_top), int(lane_bottom))
        )
        self.speed = ENEMY_SPEED
        self.hp = 3

    def update(self, dt):
        # 简单 AI：朝玩家慢慢走
        if self.player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.player.rect.centery > self.rect.centery:
            self.rect.y += self.speed * 0.6
        else:
            self.rect.y -= self.speed * 0.6

    def take_hit(self, dmg=1):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class EnemyManager:
    def __init__(self, level, player):
        self.level = level
        self.player = player
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0

    def spawn_enemy(self):
        enemy = Enemy(self.level, self.player)
        self.enemies.add(enemy)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ENEMY_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_enemy()

        self.enemies.update(dt)

    def check_collisions(self):
        hitbox = self.player.get_attack_hitbox()
        if not hitbox:
            return
        for enemy in self.enemies:
            if enemy.rect.colliderect(hitbox):
                enemy.take_hit()

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)
