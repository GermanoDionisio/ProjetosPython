import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Quest - Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 30)
large_font = pygame.font.SysFont("Consolas", 60)

# Cores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 100)
RED = (255, 60, 60)
BLACK = (10, 10, 20)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 30)

def draw_text(surface, text, font, pos, color=WHITE, center=False):
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=pos)
        surface.blit(label, rect)
    else:
        surface.blit(label, pos)

# Classes de entidade
class Particle:
    def __init__(self, pos, vel, radius, color, lifespan):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.radius = radius
        self.color = color
        self.lifespan = lifespan
        self.age = 0
    
    def update(self):
        self.pos += self.vel
        self.age += 1
    
    def draw(self, surface):
        alpha = max(255 * (1 - self.age / self.lifespan), 0)
        if alpha <= 0:
            return
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, int(alpha)), (self.radius, self.radius), self.radius)
        surface.blit(s, (self.pos.x - self.radius, self.pos.y - self.radius))
    
    def is_alive(self):
        return self.age < self.lifespan

class Ship:
    def __init__(self):
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, CYAN, [(25, 0), (0, 60), (50, 60)])
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 80))
        self.speed = 7
        self.vel = pygame.Vector2(0, 0)
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
    
    def move(self, keys):
        self.vel.x = 0
        self.vel.y = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed
        if keys[pygame.K_UP]:
            self.vel.y = -self.speed
        if keys[pygame.K_DOWN]:
            self.vel.y = self.speed
        
        self.rect.move_ip(self.vel.x, self.vel.y)
        self.rect.clamp_ip(screen.get_rect())

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
    
    def draw(self, surface):
        if self.invincible and self.invincible_timer % 6 < 3:
            # Flicker effect
            return
        surface.blit(self.image, self.rect.topleft)
    
    def hit(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 120

class Enemy:
    def __init__(self):
        self.size = random.randint(30, 60)
        self.pos = pygame.Vector2(random.randint(self.size, WIDTH - self.size), -self.size)
        self.speed = random.uniform(2, 4)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), self.size//3)
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.pos.y += self.speed
        if self.pos.y - self.size > HEIGHT:
            self.reset()
        self.rect.center = self.pos
    
    def reset(self):
        self.size = random.randint(30, 60)
        self.pos = pygame.Vector2(random.randint(self.size, WIDTH - self.size), -self.size)
        self.speed = random.uniform(2, 4)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), self.size//3)
        self.rect = self.image.get_rect(center=self.pos)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class PowerUp:
    def __init__(self):
        self.radius = 20
        self.pos = pygame.Vector2(random.randint(self.radius, WIDTH-self.radius),
                                  random.randint(self.radius, HEIGHT//2))
        self.rect = pygame.Rect(self.pos.x-self.radius, self.pos.y-self.radius, 
                                self.radius*2, self.radius*2)
        self.color = ORANGE
        self.active = True
    
    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
    
    def deactivate(self):
        self.active = False

class Game:
    def __init__(self):
        self.ship = Ship()
        self.enemies = [Enemy() for _ in range(8)]
        self.particles = []
        self.powerup = PowerUp()
        self.score = 0
        self.level = 1
        self.state = "MENU"
        self.flash_timer = 0
    
    def reset_level(self):
        self.enemies = [Enemy() for _ in range(5 + self.level)]
        self.powerup = PowerUp()
        self.ship.rect.center = (WIDTH//2, HEIGHT - 80)
        self.ship.lives = 3
        self.ship.invincible = False
        self.score = 0
        self.flash_timer = 0

    def run(self):
        running = True
        while running:
            clock.tick(60)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and self.state == "MENU":
                    self.state = "PLAY"

            screen.fill(BLACK)

            if self.state == "MENU":
                draw_text(screen, "SPACE QUEST", large_font, (WIDTH//2, HEIGHT//2 - 100), CYAN, True)
                draw_text(screen, "Pressione qualquer tecla para iniciar", font, (WIDTH//2, HEIGHT//2), WHITE, True)
            elif self.state == "PLAY":
                self.play(keys)
            elif self.state == "GAMEOVER":
                draw_text(screen, "GAME OVER", large_font, (WIDTH//2, HEIGHT//2), RED, True)
                draw_text(screen, "Pressione R para reiniciar", font, (WIDTH//2, HEIGHT//2 + 60), WHITE, True)
                if keys[pygame.K_r]:
                    self.reset_level()
                    self.state = "PLAY"
            
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def play(self, keys):
        self.ship.move(keys)
        self.handle_enemies()
        self.handle_powerup()
        self.update_particles()
        self.draw_entities()

        draw_text(screen, f"Score: {self.score}", font, (10, 10))
        draw_text(screen, f"Vidas: {self.ship.lives}", font, (10, 45))
        draw_text(screen, f"Nível: {self.level}", font, (WIDTH - 150, 10))
        
        if self.ship.lives <= 0:
            self.state = "GAMEOVER"
        
        if self.score > 0 and self.score % 10 == 0 and self.level != (self.score // 10):
            self.level_up()

    def handle_enemies(self):
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.colliderect(self.ship.rect):
                if not self.ship.invincible:
                    self.ship.hit()
                    self.create_particles(self.ship.rect.center, RED)
                    self.flash_timer = 10
            if enemy.rect.bottom > HEIGHT + enemy.size:
                self.enemies.remove(enemy)
                self.enemies.append(Enemy())

    def handle_powerup(self):
        if self.powerup.active:
            self.powerup.draw(screen)
            if self.ship.rect.colliderect(self.powerup.rect):
                self.powerup.deactivate()
                self.score += 5
                self.ship.invincible = True
                self.ship.invincible_timer = 300

    def create_particles(self, pos, color):
        for _ in range(20):
            vel = pygame.Vector2(random.uniform(-3,3), random.uniform(-3,3))
            radius = random.randint(2,5)
            lifespan = random.randint(20, 40)
            self.particles.append(Particle(pos, vel, radius, color, lifespan))

    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
            else:
                particle.draw(screen)

    def draw_entities(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1
            screen.fill(RED)

        self.ship.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.powerup.draw(screen)

    def level_up(self):
        self.level = self.score // 10
        for enemy in self.enemies:
            enemy.speed += 0.5
        self.create_particles(self.ship.rect.center, GREEN)

if __name__ == "__main__":
    game = Game()
    game.run()
