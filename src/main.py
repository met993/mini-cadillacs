import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from enemy import EnemyManager
from level import Level

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Cadillacs Demo")
    clock = pygame.time.Clock()

    level = Level()
    player = Player(level)
    enemy_manager = EnemyManager(level, player)

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新
        player.update(dt)
        enemy_manager.update(dt)

        # 碰撞检测（攻击命中敌人等）
        enemy_manager.check_collisions()

        # 渲染
        screen.fill((40, 40, 60))
        level.draw(screen)
        enemy_manager.draw(screen)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
