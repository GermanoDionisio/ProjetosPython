import pygame
import sys
import math
import random

pygame.init()

# Configurações
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FPS - Estilo COD")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)

# Objetos
class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH//2, HEIGHT//2)
        self.speed = 4
        self.health = 100
        self.ammo = 30
        self.shoot_delay = 250
        self.last_shot = 0

    def move(self, keys):
        dir = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            dir.y = -1
        if keys[pygame.K_s]:
            dir.y = 1
        if keys[pygame.K_a]:
            dir.x = -1
        if keys[pygame.K_d]:
            dir.x = 1
        if dir.length() != 0:
            dir = dir.normalize() * self.speed
            self.pos += dir
        # limite tela
        self.pos.x = max(0, min(WIDTH, self.pos.x))
        self.pos.y = max(0, min(HEIGHT, self.pos.y))

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.ammo > 0 and now - self.last_shot > self.shoot_delay:
            self.ammo -= 1
            self.last_shot = now
            return True
        return False
    
    def draw(self, surface):
        pygame.draw.rect(surface, DARK_GREEN, (self.pos.x - 10, self.pos.y - 20, 20, 40))
        # Barra de vida e munição
        pygame.draw.rect(surface, RED, (10, 10, 200, 20))
        pygame.draw.rect(surface, GREEN, (10, 10, 2 * self.health, 20))
        # munição
        font = pygame.font.SysFont("Arial", 20)
        ammo_text = font.render(f"Ammo: {self.ammo}", True, WHITE)
        surface.blit(ammo_text, (10, 40))
        health_text = font.render(f"Health: {self.health}", True, WHITE)
        surface.blit(health_text, (10, 70))


class Bullet:
    def __init__(self, pos, dir):
        self.pos = pygame.Vector2(pos)
        self.dir = dir.normalize()
        self.speed = 10
        self.alive = True

    def update(self):
        self.pos += self.dir * self.speed
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), 3)

class Enemy:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))
        self.size = 40
        self.speed = 1.2
        self.health = 50

    def move_toward(self, target):
        direction = target - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.pos.x - self.size//2, self.pos.y - self.size//2, self.size, self.size))
        # barra de vida
        pygame.draw.rect(surface, DARK_GREEN, (self.pos.x - 20, self.pos.y - self.size//2 - 10, 40, 5))
        pygame.draw.rect(surface, GREEN, (self.pos.x - 20, self.pos.y - self.size//2 - 10, 2*self.health/2, 5))

def main():
    player = Player()
    enemies = [Enemy() for _ in range(8)]
    bullets = []
    spawn_time = pygame.time.get_ticks()

    while True:
        dt = clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.ammo > 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dir = pygame.Vector2(mouse_x - player.pos.x, mouse_y - player.pos.y)
                    if player.shoot():
                        bullets.append(Bullet(player.pos, dir))
                        # Play shooting sound here

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw(screen)

        # Atualiza e move inimigos
        for enemy in enemies[:]:
            enemy.move_toward(player.pos)
            # collision ou ataque
            if (enemy.pos - player.pos).length() < 30:
                player.health -= 0.2
            # atira nos inimigos
            for b in bullets[:]:
                if (b.pos - enemy.pos).length() < enemy.size/2:
                    enemy.health -= 20
                    bullets.remove(b)
                    # som de tiros
            if enemy.health <= 0:
                enemies.remove(enemy)

        # imprime os inimigos
        for enemy in enemies:
            enemy.draw(screen)

        # bala
        for b in bullets[:]:
            b.update()
            b.draw(screen)
            if not b.alive:
                bullets.remove(b)

        # দেখাব și câteva efecte minute dacă aveți timp :) 

        # Informação adicional
        if player.health <= 0:
            draw_text(screen, "Você morreu! Reinicie...", font, (WIDTH//2, HEIGHT//2), RED, True)

        pygame.display.flip()

if __name__ == "__main__":
    main()
