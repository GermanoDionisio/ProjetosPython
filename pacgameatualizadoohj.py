import pygame
import sys
import random

pygame.init()

# Dimensões e configurações
WIDTH, HEIGHT = 560, 620  # Largura e altura da janela em pixels. Garante espaço visual suficiente para desenhar o labirinto clássico completo e permite ajuste fácil para outras resoluções.
ROWS, COLS = 31, 28  # Define o número de linhas e colunas do grid do labirinto. Essencial para o posicionamento lógico de paredes, pontos e personagens, preservando a fidelidade do labirinto original.
TILE_SIZE = WIDTH // COLS  # Calcula o tamanho exato de cada célula (tile) do grid, mantendo os elementos proporcionalmente distribuídos pela tela e facilitando a movimentação alinhada ao grid.

# Cores arcade vibrantes
BLACK = (10, 10, 10)     # Cor de fundo da tela, importante para destacar os outros elementos e dar contraste ao visual do jogo.
BLUE = (0, 0, 255)       # Usada para desenhar as paredes do labirinto, reforçando o estilo do arcade clássico.
YELLOW = (255, 240, 60)  # Cor chamativa do Pac-Man, garantindo destaque máximo sobre o fundo escuro.
RED = (255, 60, 60)      # Fantasmas comuns e mensagens de alerta usam vermelho para trazer sensação de perigo e captar atenção.
WHITE = (255, 255, 255)  # Utilizada em pontos, moedas (pellets) e textos informativos, com alto contraste para fácil visualização.
PURPLE = (180, 30, 200)  # Indica o estado especial dos fantasmas (modo poder), mudando o feedback visual rapidamente quando ativado.
GREEN = (60, 255, 70)    # Cor positiva, destacando mensagens como vitórias ou conquistas para aumentar o impacto positivo na experiência.
DARK_GRAY = (30, 30, 30) # Detalhes de fundo e menus para agregar profundidade visual sem poluir o gameplay.

# Tela e fontes arcade
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a superfície onde todo o jogo é desenhado, respeitando as configurações de resolução escolhidas.
pygame.display.set_caption("PAC-MAN Rotas Próprias - Arcade")  # Nome do projeto exibido na barra superior da janela, trazendo identificação e atmosfera arcade.

arcade_font = pygame.font.SysFont('Courier New', 50, bold=True)         # Títulos grandes e menus principais, alinhando o visual às máquinas de arcade antigas.
arcade_font_medium = pygame.font.SysFont('Courier New', 36, bold=True)  # Menus intermediários e destaques de mensagens importantes.
arcade_font_small = pygame.font.SysFont('Courier New', 20, bold=True)   # Textos de instrução ou informação secundária de fácil leitura.
font = pygame.font.SysFont('arial', 24)                                # Textos gerais do placar, dicas e informações menos destacadas.

clock = pygame.time.Clock()  # Controlador da taxa de atualização de frames do jogo. Garante animações suaves, movimentação precisa e jogo responsivo.

# Matriz do labirinto original (1=parede, 2=caminho com moeda, 0=caminho livre)
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

# Garante que o labirinto tenha o número correto de linhas
while len(labirinto) < ROWS:
    labirinto.append([1] * COLS)


class PacmanGame:
    """
    Classe principal que gerencia toda a lógica do jogo Pac-Man.
    Controla estado do Pac-Man, fantasmas, moedas, pontuação e condições de vitória/derrota.
    """
    
    def __init__(self):
        """
        Inicializa todas as variáveis e estados do jogo ao criar uma partida nova.
        Define posições iniciais, direções, pontuação, pellets e configurações do modo poder.
        """
        self.pacman_pos = [13, 23]  # Posição inicial do Pac-Man no grid [coluna, linha]
        self.pacman_dir = (0, 0)  # Direção atual do Pac-Man (dx, dy). Inicia parado.
        self.ghosts = [[13, 11], [14, 11], [13, 12], [14, 12]]  # Posições iniciais dos 4 fantasmas
        self.ghost_dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Direções iniciais de cada fantasma
        self.pellets = set()  # Conjunto de coordenadas (x, y) onde há moedas/pontos para coletar
        
        # Popula o conjunto de pellets baseado no labirinto
        for y in range(ROWS):
            for x in range(COLS):
                if labirinto[y][x] == 0 or labirinto[y][x] == 2:  # Células caminháveis
                    if random.random() > 0.05:  # 95% de chance de ter moeda
                        self.pellets.add((x, y))
        
        self.score = 0  # Pontuação atual do jogador
        self.game_over = False  # Flag de derrota
        self.vitoria = False  # Flag de vitória
        self.modo_poder = False  # Indica se o modo poder está ativo
        self.poder_timer = 0  # Timestamp de quando o modo poder foi ativado
        self.moedas_coletadas = 0  # Contador de moedas coletadas desde o início/último poder
        self.poder_duracao = 30  # Duração em segundos do modo poder
        self.moedas_necessarias = 30  # Moedas necessárias para ativar o modo poder
        self.moved = False  # Flag que indica se o jogador deu comando de movimento

    def move_pacman(self):
        """
        Move o Pac-Man na direção atual e gerencia coleta de moedas.
        Verifica colisão com paredes, atualiza pontuação e ativa modo poder quando necessário.
        """
        if not self.moved:  # Só move se houver comando do jogador
            return
        
        # Calcula nova posição baseada na direção atual
        nx = self.pacman_pos[0] + self.pacman_dir[0]
        ny = self.pacman_pos[1] + self.pacman_dir[1]
        
        # Verifica se a nova posição é válida (dentro dos limites e não é parede)
        if 0 <= nx < COLS and 0 <= ny < ROWS and labirinto[ny][nx] != 1:
            self.pacman_pos = [nx, ny]  # Atualiza posição
            
            # Verifica se há moeda na nova posição
            if (nx, ny) in self.pellets:
                self.pellets.remove((nx, ny))  # Remove moeda coletada
                self.score += 10  # Aumenta pontuação
                self.moedas_coletadas += 1  # Incrementa contador
                
                # Ativa modo poder se coletou moedas suficientes
                if self.moedas_coletadas >= self.moedas_necessarias:
                    self.modo_poder = True
                    self.poder_timer = pygame.time.get_ticks()  # Marca o tempo de ativação
        
        self.moved = False  # Reseta flag de movimento

    def move_ghosts(self):
        """
        Move os fantasmas automaticamente pelo labirinto.
        Cada fantasma segue sua direção atual e muda ao colidir com parede (rotação de 90°).
        """
        for i in range(len(self.ghosts)):
            gx, gy = self.ghosts[i]  # Posição atual do fantasma
            dx, dy = self.ghost_dirs[i]  # Direção atual do fantasma
            nx, ny = gx + dx, gy + dy  # Calcula próxima posição
            
            # Verifica se pode mover para a próxima posição
            if 0 <= nx < COLS and 0 <= ny < ROWS and labirinto[ny][nx] != 1:
                self.ghosts[i] = [nx, ny]  # Move o fantasma
            else:
                # Colisão com parede: gira 90° (troca e inverte coordenadas)
                current_dir = self.ghost_dirs[i]
                new_dir = (current_dir[1], -current_dir[0])
                self.ghost_dirs[i] = new_dir

    def check_game_over_and_victory(self):
        """
        Verifica colisões entre Pac-Man e fantasmas, e condições de vitória.
        No modo poder, fantasmas são eliminados. Caso contrário, é game over.
        Vitória ocorre quando todos os fantasmas são eliminados.
        """
        for ghost in self.ghosts[:]:  # Itera sobre cópia da lista para permitir remoção
            if ghost == self.pacman_pos:  # Detecta colisão
                if self.modo_poder:
                    self.ghosts.remove(ghost)  # Elimina fantasma
                    self.score += 100  # Bônus por eliminar fantasma
                else:
                    self.game_over = True  # Derrota
        
        # Verifica vitória
        if len(self.ghosts) == 0:
            self.vitoria = True

    def update_poder(self):  
        """
        Atualiza o estado do modo poder.
        Desativa o modo após 30 segundos e reseta contador de moedas.
        """
        if self.modo_poder:
            tempo_passado = (pygame.time.get_ticks() - self.poder_timer) / 1000  # Converte ms para segundos
            if tempo_passado > 30:  # Duração fixa de 30 segundos
                self.modo_poder = False
                self.moedas_coletadas = 0  # Reseta contador

    def draw(self):
        """
        Renderiza todo o estado visual do jogo na tela.
        Desenha labirinto, pellets, Pac-Man, fantasmas, placar e mensagens de fim de jogo.
        """
        screen.fill(BLACK)  # Limpa tela com fundo preto
        
        # Desenha paredes do labirinto
        for y in range(ROWS):
            for x in range(COLS):
                if labirinto[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Desenha pellets/moedas
        for pellet in self.pellets:
            px = pellet[0] * TILE_SIZE + TILE_SIZE // 2
            py = pellet[1] * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, WHITE, (px, py), 4)
        
        # Desenha Pac-Man
        px = self.pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2
        py = self.pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (px, py), TILE_SIZE // 2 - 2)
        
        # Desenha fantasmas (cor muda conforme modo poder)
        ghost_color = PURPLE if self.modo_poder else RED
        for gx, gy in self.ghosts:
            pygame.draw.circle(screen, ghost_color, 
                             (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2),
                             TILE_SIZE // 2 - 2)
        
        # Desenha placar
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 30))
        
        # Mensagens de fim de jogo
        if self.game_over:
            go_text = font.render("GAME OVER", True, RED)
            screen.blit(go_text, (WIDTH // 2 - 80, HEIGHT // 2))
        elif self.vitoria:
            vitoria_text = font.render("VITÓRIA!", True, GREEN)
            screen.blit(vitoria_text, (WIDTH // 2 - 80, HEIGHT // 2))


def draw_text(surface, text, font_used, color, pos, outline_color=None):
    """
    Renderiza texto centralizado com contorno opcional (efeito arcade).
    Usado para títulos, menus e mensagens importantes, aumentando legibilidade e impacto visual.
    """
    if outline_color:
        base = font_used.render(text, True, color)
        # Desenha contorno em 8 direções
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,-1),(1,1),(-1,1)]:
            outline = font_used.render(text, True, outline_color)
            rect = outline.get_rect(center=(pos[0]+dx, pos[1]+dy))
            surface.blit(outline, rect)
        # Desenha texto principal por cima
        rect = base.get_rect(center=pos)
        surface.blit(base, rect)
    else:
        base = font_used.render(text, True, color)
        rect = base.get_rect(center=pos)
        surface.blit(base, rect)


def draw_arcade_background(surface):
    """
    Desenha fundo quadriculado estilo arcade para menus.
    Cria atmosfera retrô sem distrair do conteúdo principal.
    """
    surface.fill(BLACK)
    spacing = 20  # Espaçamento entre linhas do grid
    # Linhas verticais
    for x in range(0, WIDTH, spacing):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, HEIGHT))
    # Linhas horizontais
    for y in range(0, HEIGHT, spacing):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (WIDTH, y))


def main():
    """
    Loop principal do jogo.
    Gerencia estados (menu, jogo, vitória, derrota), eventos do usuário,
    atualizações de lógica e renderização de todos os elementos.
    """
    clock = pygame.time.Clock()
    tela = 'menu'  # Estado inicial da aplicação
    menu_opcao = 0  # Opção selecionada no menu (0=Jogar, 1=Config, 2=Sair)
    game = None  # Instância do jogo (None quando não está jogando)
    ghost_move_tick = 0  # Contador para controlar velocidade dos fantasmas

    running = True

    while running:
        try:
            clock.tick(30)  # Limita a 30 FPS

            # Define fundo conforme a tela atual
            if tela in ('menu', 'configuracoes'):
                draw_arcade_background(screen)
            else:
                screen.fill(BLACK)

            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False

            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
                
                elif event.type == pygame.KEYDOWN:
                    # Navegação no menu
                    if tela == 'menu':
                        if event.key == pygame.K_DOWN:
                            menu_opcao = (menu_opcao + 1) % 3
                        elif event.key == pygame.K_UP:
                            menu_opcao = (menu_opcao - 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if menu_opcao == 0:
                                game = PacmanGame()  # Inicia novo jogo
                                tela = 'jogo'
                            elif menu_opcao == 1:
                                tela = 'configuracoes'
                            elif menu_opcao == 2:
                                running = False
                    
                    # Sair de configurações
                    elif tela == 'configuracoes':
                        if event.key == pygame.K_ESCAPE:
                            tela = 'menu'
                    
                    # Controles durante o jogo
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
                    
                    # Opções pós-jogo
                    elif tela in ('vitoria', 'derrota'):
                        if event.key == pygame.K_RETURN:
                            game = PacmanGame()
                            tela = 'jogo'
                        elif event.key == pygame.K_DOWN:
                            tela = 'menu'

            # Renderização do menu principal
            if tela == 'menu':
                draw_text(screen, 'PAC-MAN', arcade_font, YELLOW, (WIDTH // 2, 120), outline_color=RED)
                options = ['JOGAR', 'CONFIGURAÇÕES', 'SAIR']
                rects = []
                
                for i, option in enumerate(options):
                    pos = (WIDTH // 2, 260 + i * 60)
                    color = YELLOW if i == menu_opcao else WHITE
                    draw_text(screen, option, arcade_font_medium, color, pos, 
                            outline_color=BLACK if i == menu_opcao else None)
                    text_surface = pygame.font.SysFont('arial', 24).render(option, True, color)
                    rect = text_surface.get_rect(center=pos)
                    rects.append(rect)
                
                # Suporte a clique do mouse
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
                
                draw_text(screen, 'Use ↑/↓ para navegar e ENTER para selecionar', 
                         font, WHITE, (WIDTH // 2, HEIGHT - 40))
            
            # Tela de configurações
            elif tela == 'configuracoes':
                draw_arcade_background(screen)
                draw_text(screen, 'CONFIGURAÇÕES', arcade_font_medium, WHITE, 
                         (WIDTH // 2, 100), outline_color=BLACK)
                draw_text(screen, 'Aqui podem ficar suas configurações futuras', 
                         arcade_font_small, WHITE, (WIDTH // 2, 200))
                draw_text(screen, 'Pressione ESC para voltar', font, WHITE, 
                         (WIDTH // 2, HEIGHT - 50))
            
            # Loop de jogo
            elif tela == 'jogo' and game:
                if not game.game_over and not game.vitoria:
                    ghost_move_tick += 1
                    game.move_pacman()
                    
                    # Fantasmas se movem mais devagar (a cada 3 frames)
                    if ghost_move_tick % 3 == 0:
                        game.move_ghosts()
                    
                    game.check_game_over_and_victory()
                    game.update_poder()
                    game.draw()
                elif game.game_over:
                    tela = 'derrota'
                elif game.vitoria:
                    tela = 'vitoria'
            
            # Tela de vitória
            elif tela == 'vitoria':
                draw_text(screen, 'PARABÉNS! VOCÊ GANHOU!', arcade_font_medium, GREEN, 
                         (WIDTH // 2, HEIGHT // 2 - 40), outline_color=BLACK)
                draw_text(screen, 'Pressione ENTER para jogar novamente', 
                         arcade_font_small, GREEN, (WIDTH // 2, HEIGHT // 2 + 20))
                draw_text(screen, 'Pressione ↓ para voltar ao menu principal', 
                         arcade_font_small, GREEN, (WIDTH // 2, HEIGHT // 2 + 60))
            
            # Tela de derrota
            elif tela == 'derrota':
                draw_text(screen, 'GAME OVER! VOCÊ PERDEU!', arcade_font_medium, RED, 
                         (WIDTH // 2, HEIGHT // 2 - 40), outline_color=BLACK)
                draw_text(screen, 'Pressione ENTER para jogar novamente', 
                         arcade_font_small, RED, (WIDTH // 2, HEIGHT // 2 + 20))
                draw_text(screen, 'Pressione ↓ para voltar ao menu principal', 
                         arcade_font_small, RED, (WIDTH // 2, HEIGHT // 2 + 60))
            
            pygame.display.flip()  # Atualiza a tela
        
        except Exception as e:
            print("Erro detectado no loop principal:", e)
    
    pygame.quit()
    sys.exit()


# Ponto de entrada do programa
# Executa a função main() apenas se este arquivo for executado diretamente (não importado como módulo)
if __name__ == "__main__":
    main()
