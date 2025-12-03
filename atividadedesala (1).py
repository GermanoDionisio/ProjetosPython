import os
import time


# ---------- INTERFACE ----------


def limpar_tela():
    # Limpa o console conforme o SO:
    # - Windows usa 'cls'
    # - Unix-like (Linux/macOS) usa 'clear'
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho():
    # Imprime um cabeçalho simples para contextualizar o jogo
    print("=" * 35)
    print("   JOGO DA VELHA - IA (MINIMAX)    ")
    print("        VOCÊ COMEÇA (X)            ")
    print("=" * 35)
    print("Você: X    IA: O")
    print()


def imprimir_tabuleiro(tab):
    # Constrói as três linhas visuais a partir da string 'tab' de 9 chars
    linhas = []
    for l in range(3):
        linha = []
        for c in range(3):
            idx = l * 3 + c  # mapeia (linha,coluna) -> índice 0..8
            linha.append(tab[idx])
        # Junta com separadores para exibição amigável
        linhas.append(" " + " | ".join(linha) + " ")

    # Separadores e mapa de posições para o usuário
    sep = "---+---+---"
    mapa = [" 0 | 1 | 2 ", " 3 | 4 | 5 ", " 6 | 7 | 8 "]

    # Exibe lado a lado: estado atual e os índices das casas
    print("TABULEIRO        POSIÇÕES")
    print(linhas[0] + "     " + mapa[0])
    print(sep + "     " + sep)
    print(linhas[1] + "     " + mapa[1])
    print(sep + "     " + sep)
    print(linhas[2] + "     " + mapa[2])
    print()


# ---------- LÓGICA DO JOGO ----------


def inicializar_tabuleiro():
    # Cria um tabuleiro vazio como string de 9 '-' (casa livre)
    return "-" * 9


def jogadas_possiveis(tab):
    # Retorna índices das casas livres (onde há '-')
    return [i for i, v in enumerate(tab) if v == "-"]


def vencedor(tab):
    # Todas as combinações vencedoras (linhas, colunas, diagonais)
    linhas = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    # Se três em linha são iguais e não '-', há vencedor
    for a, b, c in linhas:
        if tab[a] == tab[b] == tab[c] != "-":
            return tab[a]  # 'X' ou 'O'
    # Se não há casas livres, é empate
    if "-" not in tab:
        return "empate"
    # Caso contrário, jogo continua
    return None


def jogar_pos(tab, pos, jogador):
    # Aplica uma jogada imutavelmente:
    # converte para lista, altera a posição e volta para string
    lista = list(tab)
    lista[pos] = jogador
    return "".join(lista)


# ---------- MINIMAX (IA É O) ----------


def minimax(tab, maximizando):
    """
    Agora o maximizador é a IA (O) e o minimimizador é o humano (X).
    Vitória da IA (O): +1
    Vitória do humano (X): -1
    Empate: 0
    """
    # Caso base: se o jogo terminou, retorna utilidade
    g = vencedor(tab)
    if g == "O":
        return 1      # melhor para a IA
    elif g == "X":
        return -1     # pior para a IA
    elif g == "empate":
        return 0      # neutro

    # Lista as ações (casas livres) a explorar
    jogadas = jogadas_possiveis(tab)

    if maximizando:  # vez da IA (O): escolhe o MAIOR score
        melhor = float("-inf")
        for a in jogadas:
            # Simula jogar 'O' na posição a
            novo = jogar_pos(tab, a, "O")
            # Próximo nível é do minimizador (humano)
            score = minimax(novo, False)
            # Mantém o melhor (máximo) score
            melhor = max(melhor, score)
        return melhor
    else:  # vez do humano (X): escolhe o MENOR score
        melhor = float("inf")
        for a in jogadas:
            # Simula jogar 'X' na posição a
            novo = jogar_pos(tab, a, "X")
            # Próximo nível é do maximizador (IA)
            score = minimax(novo, True)
            # Mantém o pior (mínimo) para a IA
            melhor = min(melhor, score)
        return melhor


def melhor_jogada_ia(tab):
    """Escolhe a melhor jogada para a IA (O) usando Minimax."""
    # Varre todas as ações possíveis, avalia com minimax,
    # e escolhe a de maior pontuação
    melhor_score = float("-inf")
    melhor_acao = None
    for a in jogadas_possiveis(tab):
        # Simula colocar 'O' e avalia assumindo que o próximo é o minimizador
        novo = jogar_pos(tab, a, "O")
        score = minimax(novo, False)  # depois do O, vez do X
        if score > melhor_score:
            melhor_score = score
            melhor_acao = a
    return melhor_acao


# ---------- JOGO CONTRA HUMANO ----------


def jogar():
    """
    Você é X e SEMPRE começa.
    IA é O e responde com Minimax.
    """
    # Estado inicial e jogador da vez
    tab = inicializar_tabuleiro()
    vez = "X"  # humano começa

    while True:
        # Atualiza a interface a cada turno
        limpar_tela()
        cabecalho()
        imprimir_tabuleiro(tab)

        # Verifica término (vitória/empate) antes da próxima ação
        g = vencedor(tab)
        if g == "X":
            print("Resultado: Você venceu! (jogou melhor que a IA ou ela errou).")
            break
        elif g == "O":
            print("Resultado: A IA venceu.")
            break
        elif g == "empate":
            print("Resultado: Empate.")
            break

        if vez == "X":
            # Turno do humano: lê e valida entrada
            livres = jogadas_possiveis(tab)
            print("Sua vez (X). Casas livres:", livres)
            entrada = input("Digite uma posição (0–8): ")
            try:
                pos = int(entrada)
            except ValueError:
                print("Entrada inválida. Use número de 0 a 8.")
                time.sleep(1)
                continue
            if pos not in livres:
                print("Posição inválida ou ocupada. Tente de novo.")
                time.sleep(1)
                continue
            # Aplica jogada e passa a vez para a IA
            tab = jogar_pos(tab, pos, "X")
            vez = "O"
        else:
            # Turno da IA: pensa e executa melhor jogada
            print("Vez da IA (O)...")
            time.sleep(0.7)
            acao = melhor_jogada_ia(tab)
            tab = jogar_pos(tab, acao, "O")
            vez = "X"


# ---------- MAIN ----------


if __name__ == "__main__":
    # Entrada do programa: apresenta, aguarda ENTER e inicia o loop do jogo
    limpar_tela()
    cabecalho()
    print("Você começa sempre como X.\n")
    input("Pressione ENTER para iniciar...")
    jogar()


