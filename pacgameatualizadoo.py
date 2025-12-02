import pygame
import sys
import random

pygame.init()

# Dimensões e configurações
WIDTH, HEIGHT = 560, 620
ROWS, COLS = 31, 28
TILE_SIZE = WIDTH // COLS

# Cores arcade vibrantes
BLACK = (10, 10, 10)
BLUE = (0, 0, 255)
YELLOW = (255, 240, 60)
RED = (255, 60, 60)
WHITE = (255, 255, 255)
PURPLE = (180, 30, 200)
GREEN = (60, 255, 70)
DARK_GRAY = (30, 30, 30)

# Tela e fontes arcade
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN Rotas Próprias - Arcade")

arcade_font = pygame.font.SysFont('Courier New', 50, bold=True)
arcade_font_medium = pygame.font.SysFont('Courier New', 36, bold=True)
arcade_font_small = pygame.font.SysFont('Courier New', 20, bold=True)
font = pygame.font.SysFont('arial', 24)

clock = pygame.time.Clock()

labirinto = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,0,1,1,2,2,2,2,2,2,2,2,0,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1,1,1,2,1],
    [1,2,1,2,2,1,2,1,2,2,0,1,2,1,1,2,1,2,2,2,1,1,2,1,2,1,2,1],
    [1,2,1,2,2,1,2,1,2,1,2,1,2,1,1,2,1,2,1,2,2,0,2,1,2,1,2,1],
    [1,2,1,2,2,1,2,1,2,1,2,1,2,1,1,2,1,2,1,1,2,1,2,1,2,1,2,1],
    [1,2,1,1,2,1,2,1,2,2,2,2,2,1,1,2,1,2,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,1,2,1,2,1,1,1,1,1,2,1,1,2,1,1,2,1,2,0,2,1,2,1,2,1],
    [1,1,2,1,2,1,2,1,2,2,2,2,2,1,1,2,1,2,2,1,2,1,2,1,2,0,2,1],
    [1,2,2,1,2,1,2,1,2,1,2,0,2,1,1,2,1,2,1,1,2,1,2,1,2,1,2,1],
    [1,2,2,1,2,1,0,1,2,1,2,1,2,1,1,2,1,2,1,2,2,1,2,1,2,1,2,1],
    [1,2,2,1,2,1,2,1,2,2,2,1,2,1,1,2,1,2,2,2,2,1,2,1,2,1,2,1],
    [1,2,2,1,2,1,2,1,1,1,2,1,2,1,1,2,1,1,1,1,1,1,2,1,2,1,2,1],
    [1,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2,1,2,1],
    [1,2,2,1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,2,2,2,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1,2,2,2,1,0,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1],
    [1,2,2,2,2,1,2,2,2,2,2,2,2,1,1,2,2,2,2,1,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,1,1,2,2,0,2,2,2,2,2,2,2,0,2,1],
    [1,1,1,1,1,1,1,1,1,1,2,1,0,0,0,0,1,2,1,1,1,1,1,1,1,1,1,1],
]

while len(labirinto) < ROWS:
    labirinto.append([1] * COLS)

class PacmanGame:
    "Inicializa todas as variáveis e estados do jogo ao criar uma partida nova."
    def __init__(self):
        self.pacman_pos = [13, 23]
        self.pacman_dir = (0, 0)
        self.ghosts = [[13, 11], [14, 11], [13, 12], [14, 12]]
        self.ghost_dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.pellets = set()
        for y in range(ROWS):
            for x in range(COLS):
                if labirinto[y][x] == 0 or labirinto[y][x] == 2:
                    if random.random() > 0.05:
                        self.pellets.add((x, y))
        self.score = 0
        self.game_over = False
        self.vitoria = False
        self.modo_poder = False
        self.poder_timer = 0
        self.moedas_coletadas = 0
        self.poder_duracao = 30
        self.moedas_necessarias = 30
        self.moved = False

    "Move Pac-Man e coleta moedas, ativando modo especial quando necessário."
    def move_pacman(self):
        if not self.moved:
            return
        nx = self.pacman_pos[0] + self.pacman_dir[0]
        ny = self.pacman_pos[1] + self.pacman_dir[1]
        if 0 <= nx < COLS and 0 <= ny < ROWS and labirinto[ny][nx] != 1:
            self.pacman_pos = [nx, ny]
            if (nx, ny) in self.pellets:
                self.pellets.remove((nx, ny))
                self.score += 10
                self.moedas_coletadas += 1
                if self.moedas_coletadas >= self.moedas_necessarias:
                    self.modo_poder = True
                    self.poder_timer = pygame.time.get_ticks()
        self.moved = False

    "Faz fantasmas se moverem automaticamente e trocarem de direção ao bater em parede."
    def move_ghosts(self):
        for i in range(len(self.ghosts)):
            gx, gy = self.ghosts[i]
            dx, dy = self.ghost_dirs[i]
            nx, ny = gx + dx, gy + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and labirinto[ny][nx] != 1:
                self.ghosts[i] = [nx, ny]
            else:
                current_dir = self.ghost_dirs[i]
                new_dir = (current_dir[1], -current_dir[0])
                self.ghost_dirs[i] = new_dir

    "Verifica colisão entre Pac-Man e fantasmas e define fim de partida ou vitória."
    def check_game_over_and_victory(self):
        for ghost in self.ghosts[:]:
            if ghost == self.pacman_pos:
                if self.modo_poder:
                    self.ghosts.remove(ghost)
                    self.score += 100
                else:
                    self.game_over = True
        if len(self.ghosts) == 0:
            self.vitoria = True

    "Atualiza duração do modo especial e desativa após tempo limite."
    def update_poder(self):
        if self.modo_poder:
            tempo_passado = (pygame.time.get_ticks() - self.poder_timer) / 1000
            if tempo_passado > 30:
                self.modo_poder = False
                self.moedas_coletadas = 0

    "Desenha o estado atual do jogo para o jogador."
    def draw(self):
        screen.fill(BLACK)
        for y in range(ROWS):
            for x in range(COLS):
                if labirinto[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for pellet in self.pellets:
            px = pellet[0] * TILE_SIZE + TILE_SIZE // 2
            py = pellet[1] * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (px, py), 4)
        px = self.pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2
        py = self.pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (px, py), TILE_SIZE // 2 - 2)
        ghost_color = PURPLE if self.modo_poder else RED
        for gx, gy in self.ghosts:
            pygame.draw.circle(screen, ghost_color, (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 30))
        if self.game_over:
            go_text = font.render("GAME OVER", True, RED)
            screen.blit(go_text, (WIDTH // 2 - 80, HEIGHT // 2))
        elif self.vitoria:
            vitoria_text = font.render("VITÓRIA!", True, GREEN)
            screen.blit(vitoria_text, (WIDTH // 2 - 80, HEIGHT // 2))

"Renderiza textos centralizados e com contorno se pedido."
def draw_text(surface, text, font_used, color, pos, outline_color=None):
    if outline_color:
        base = font_used.render(text, True, color)
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,-1),(1,1),(-1,1)]:
            outline = font_used.render(text, True, outline_color)
            rect = outline.get_rect(center=(pos[0]+dx, pos[1]+dy))
            surface.blit(outline, rect)
        rect = base.get_rect(center=pos)
        surface.blit(base, rect)
    else:
        base = font_used.render(text, True, color)
        rect = base.get_rect(center=pos)
        surface.blit(base, rect)

"Desenha fundo quadriculado nos menus do jogo."
def draw_arcade_background(surface):
    surface.fill(BLACK)
    spacing = 20
    for x in range(0, WIDTH, spacing):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, spacing):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (WIDTH, y))

"Controla o loop principal, eventos, telas e atualizações do jogo."
def main():
    clock = pygame.time.Clock()
    tela = 'menu'
    menu_opcao = 0
    game = None
    ghost_move_tick = 0

    running = True

    while running:
        try:
            clock.tick(30)

            if tela in ('menu', 'configuracoes'):
                draw_arcade_background(screen)
            else:
                screen.fill(BLACK)

            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
                elif event.type == pygame.KEYDOWN:
                    if tela == 'menu':
                        if event.key == pygame.K_DOWN:
                            menu_opcao = (menu_opcao + 1) % 3
                        elif event.key == pygame.K_UP:
                            menu_opcao = (menu_opcao - 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if menu_opcao == 0:
                                game = PacmanGame()
                                tela = 'jogo'
                            elif menu_opcao == 1:
                                tela = 'configuracoes'
                            elif menu_opcao == 2:
                                running = False
                    elif tela == 'configuracoes':
                        if event.key == pygame.K_ESCAPE:
                            tela = 'menu'
                    elif tela == 'jogo' and game and not game.game_over and not game.vitoria:
                        if event.key == pygame.K_UP:
                            game.pacman_dir = (0, -1)
                            game.moved = True
                        elif event.key == pygame.K_DOWN:
                            game.pacman_dir = (0, 1)
                            game.moved = True
                        elif event.key == pygame.K_LEFT:
                            game.pacman_dir = (-1, 0)
                            game.moved = True
                        elif event.key == pygame.K_RIGHT:
                            game.pacman_dir = (1, 0)
                            game.moved = True
                    elif tela in ('vitoria', 'derrota'):
                        if event.key == pygame.K_RETURN:
                            game = PacmanGame()
                            tela = 'jogo'
                        elif event.key == pygame.K_DOWN:
                            tela = 'menu'
            if tela == 'menu':
                draw_text(screen, 'PAC-MAN', arcade_font, YELLOW, (WIDTH // 2, 120), outline_color=RED)
                options = ['JOGAR', 'CONFIGURAÇÕES', 'SAIR']
                rects = []
                for i, option in enumerate(options):
                    pos = (WIDTH // 2, 260 + i * 60)
                    color = YELLOW if i == menu_opcao else WHITE
                    draw_text(screen, option, arcade_font_medium, color, pos, outline_color=BLACK if i == menu_opcao else None)
                    text_surface = pygame.font.SysFont('arial', 24).render(option, True, color)
                    rect = text_surface.get_rect(center=pos)
                    rects.append(rect)
                if mouse_clicked:
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(mouse_pos):
                            menu_opcao = i
                            if i == 0:
                                game = PacmanGame()
                                tela = 'jogo'
                            elif i == 1:
                                tela = 'configuracoes'
                            elif i == 2:
                                running = False
                draw_text(screen, 'Use ↑/↓ para navegar e ENTER para selecionar', font, WHITE, (WIDTH // 2, HEIGHT - 40))
            elif tela == 'configuracoes':
                draw_arcade_background(screen)
                draw_text(screen, 'CONFIGURAÇÕES', arcade_font_medium, WHITE, (WIDTH // 2, 100), outline_color=BLACK)
                draw_text(screen, 'Aqui podem ficar suas configurações futuras', arcade_font_small, WHITE, (WIDTH // 2, 200))
                draw_text(screen, 'Pressione ESC para voltar', font, WHITE, (WIDTH // 2, HEIGHT - 50))
            elif tela == 'jogo' and game:
                if not game.game_over and not game.vitoria:
                    ghost_move_tick += 1
                    game.move_pacman()
                    if ghost_move_tick % 3 == 0:
                        game.move_ghosts()
                    game.check_game_over_and_victory()
                    game.update_poder()
                    game.draw()
                elif game.game_over:
                    tela = 'derrota'
                elif game.vitoria:
                    tela = 'vitoria'
            elif tela == 'vitoria':
                draw_text(screen, 'PARABÉNS! VOCÊ GANHOU!', arcade_font_medium, GREEN, (WIDTH // 2, HEIGHT // 2 - 40), outline_color=BLACK)
                draw_text(screen, 'Pressione ENTER para jogar novamente', arcade_font_small, GREEN, (WIDTH // 2, HEIGHT // 2 + 20))
                draw_text(screen, 'Pressione ↓ para voltar ao menu principal', arcade_font_small, GREEN, (WIDTH // 2, HEIGHT // 2 + 60))
            elif tela == 'derrota':
                draw_text(screen, 'GAME OVER! VOCÊ PERDEU!', arcade_font_medium, RED, (WIDTH // 2, HEIGHT // 2 - 40), outline_color=BLACK)
                draw_text(screen, 'Pressione ENTER para jogar novamente', arcade_font_small, RED, (WIDTH // 2, HEIGHT // 2 + 20))
                draw_text(screen, 'Pressione ↓ para voltar ao menu principal', arcade_font_small, RED, (WIDTH // 2, HEIGHT // 2 + 60))
            pygame.display.flip()
        except Exception as e:
            print("Erro detectado no loop principal:", e)
    pygame.quit()
    sys.exit()

"Executa main() só se o arquivo for rodado como principal."
if __name__ == "__main__":
    main()
