import os
import time

# ---------- INTERFACE ----------

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def cabecalho():
    print("=" * 35)
    print("   JOGO DA VELHA - IA (MINIMAX)    ")
    print("      DIFICULDADE: ALTA (LIMITADA) ")
    print("=" * 35)
    print("Você: X    IA: O")
    print()

def imprimir_tabuleiro(tab):
    linhas = []
    for l in range(3):
        linha = []
        for c in range(3):
            idx = l * 3 + c
            linha.append(tab[idx])
        linhas.append(" " + " | ".join(linha) + " ")

    sep = "---+---+---"
    mapa = [" 0 | 1 | 2 ", " 3 | 4 | 5 ", " 6 | 7 | 8 "]

    print("TABULEIRO        POSIÇÕES")
    print(linhas[0] + "     " + mapa[0])
    print(sep + "     " + sep)
    print(linhas[1] + "     " + mapa[1])
    print(sep + "     " + sep)
    print(linhas[2] + "     " + mapa[2])
    print()

# ---------- LÓGICA DO JOGO ----------

def inicializar_tabuleiro():
    return "-" * 9

def jogadas_possiveis(tab):
    return [i for i, v in enumerate(tab) if v == "-"]

def vencedor(tab):
    linhas = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in linhas:
        if tab[a] == tab[b] == tab[c] != "-":
            return tab[a]
    if "-" not in tab:
        return "empate"
    return None

def jogar_pos(tab, pos, jogador):
    lista = list(tab)
    lista[pos] = jogador
    return "".join(lista)

# ---------- MINIMAX COM PROFUNDIDADE LIMITADA ----------

def minimax(tab, maximizando, profundidade, profundidade_max=4):
    """
    Minimax com limite de profundidade para reduzir dificuldade.
    - profundidade_max=4: IA analisa no máximo 4 jogadas à frente
    - Isso deixa ela forte, mas não perfeita (você pode vencer!)
    
    Vitória IA (O): +1
    Vitória humano (X): -1
    Empate: 0
    """
    g = vencedor(tab)
    if g == "O":
        return 1 + (profundidade_max - profundidade) * 0.1  # Bônus por vitória rápida
    elif g == "X":
        return -1 - (profundidade_max - profundidade) * 0.1  # Penalidade por derrota rápida
    elif g == "empate":
        return 0

    # SE A PROFUNDIDADE MÁXIMA FOI ATINGIDA, FAZ AVALIAÇÃO HEURÍSTICA
    if profundidade >= profundidade_max:
        # Avaliação simples: quantos X vs quantos O
        score_x = tab.count("X")
        score_o = tab.count("O")
        return score_o - score_x  # IA (O) quer mais O's que X's

    jogadas = jogadas_possiveis(tab)

    if maximizando:  # vez da IA (O)
        melhor = float("-inf")
        for a in jogadas:
            novo = jogar_pos(tab, a, "O")
            score = minimax(novo, False, profundidade + 1, profundidade_max)
            melhor = max(melhor, score)
        return melhor
    else:  # vez do humano (X)
        melhor = float("inf")
        for a in jogadas:
            novo = jogar_pos(tab, a, "X")
            score = minimax(novo, True, profundidade + 1, profundidade_max)
            melhor = min(melhor, score)
        return melhor

def melhor_jogada_ia(tab, profundidade_max=4):
    """Escolhe a melhor jogada para IA (O) com profundidade limitada."""
    melhor_score = float("-inf")
    melhor_acao = None
    for a in jogadas_possiveis(tab):
        novo = jogar_pos(tab, a, "O")
        score = minimax(novo, False, 1, profundidade_max)
        if score > melhor_score:
            melhor_score = score
            melhor_acao = a
        # Se encontrar jogada que garante vitória, para imediatamente
        elif score >= 1:
            return a
    return melhor_acao

# ---------- JOGO CONTRA HUMANO ----------

def jogar():
    """Você começa como X, IA responde com Minimax limitado (profundidade 4)."""
    tab = inicializar_tabuleiro()
    vez = "X"

    while True:
        limpar_tela()
        cabecalho()
        imprimir_tabuleiro(tab)

        g = vencedor(tab)
        if g == "X":
            print("Resultado: Você venceu! 🎉")
            break
        elif g == "O":
            print("Resultado: A IA venceu.")
            break
        elif g == "empate":
            print("Resultado: Empate.")
            break

        if vez == "X":
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
            tab = jogar_pos(tab, pos, "X")
            vez = "O"
        else:
            print("Vez da IA (O)... Pensando...")
            time.sleep(1.2)  # Simula "pensamento"
            acao = melhor_jogada_ia(tab, profundidade_max=4)
            tab = jogar_pos(tab, acao, "O")
            print(f"IA jogou na posição {acao}")
            vez = "X"

# ---------- MAIN ----------

if __name__ == "__main__":
    limpar_tela()
    cabecalho()
    print("IA com Minimax limitado (profundidade 4).")
    print("Ela é forte, mas você tem chance de vencer!\n")
    input("Pressione ENTER para começar...")
    jogar()

