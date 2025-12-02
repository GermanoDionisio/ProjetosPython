###############################
# Jogo da Velha com Q-Learning
# IA aprende a jogar contra um adversário aleatório
# Depois você pode jogar contra a IA treinada
###############################

import random  # Importa a biblioteca random para gerar escolhas aleatórias

########################
# REPRESENTAÇÃO DO JOGO
########################

# Representamos o tabuleiro como uma string de 9 caracteres.
# Cada posição pode ser:
# 'X' - peça do jogador X
# 'O' - peça do jogador O
# '-' - casa vazia
# Índices: 0 1 2
#          3 4 5
#          6 7 8


def inicializar_tabuleiro():
    # Cria um tabuleiro vazio com 9 casas, todas com '-'
    return "-" * 9


def imprimir_tabuleiro(tabuleiro):
    # Imprime o tabuleiro em formato 3x3 para visualização no terminal
    # Cada linha contém 3 posições da string
    print(tabuleiro[0], tabuleiro[1], tabuleiro[2])
    print(tabuleiro[3], tabuleiro[4], tabuleiro[5])
    print(tabuleiro[6], tabuleiro[7], tabuleiro[8])
    print()  # Linha em branco para separar visualmente


def obter_jogadas_possiveis(tabuleiro):
    # Retorna uma lista com os índices das casas vazias (onde é possível jogar)
    jogadas = []  # Lista de jogadas
    for i in range(9):  # Percorre as 9 posições
        if tabuleiro[i] == "-":  # Se a casa está vazia
            jogadas.append(i)  # Adiciona o índice como jogada possível
    return jogadas


def verificar_vencedor(tabuleiro):
    # Verifica se alguém ganhou ou se deu empate
    # Retorna:
    # 'X' se X ganhou
    # 'O' se O ganhou
    # 'empate' se todas as casas estão preenchidas e ninguém ganhou
    # None se o jogo ainda não terminou

    # Define todas as combinações de vitória (linhas, colunas e diagonais)
    combinacoes = [
        (0, 1, 2),  # Linha 1
        (3, 4, 5),  # Linha 2
        (6, 7, 8),  # Linha 3
        (0, 3, 6),  # Coluna 1
        (1, 4, 7),  # Coluna 2
        (2, 5, 8),  # Coluna 3
        (0, 4, 8),  # Diagonal principal
        (2, 4, 6),  # Diagonal secundária
    ]

    # Verifica se X ou O preencheu alguma combinação de vitória
    for (a, b, c) in combinacoes:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] != "-":
            # Se três casas iguais e não vazias, temos um vencedor
            return tabuleiro[a]

    # Se não há vencedor e não há casas vazias, é empate
    if "-" not in tabuleiro:
        return "empate"

    # Caso contrário, o jogo ainda não acabou
    return None


def fazer_jogada(tabuleiro, posicao, jogador):
    # Retorna um novo tabuleiro resultante da jogada
    # 'tabuleiro' é a string atual
    # 'posicao' é o índice de 0 a 8 onde o jogador vai jogar
    # 'jogador' é 'X' ou 'O'
    tabuleiro_lista = list(tabuleiro)  # Converte a string em lista (strings são imutáveis)
    tabuleiro_lista[posicao] = jogador  # Coloca a peça do jogador na posição desejada
    return "".join(tabuleiro_lista)  # Junta de volta em uma string


########################
# Q-LEARNING
########################

# Vamos usar um dicionário como Q-table.
# Chave: (estado, ação) onde:
#   estado: string do tabuleiro
#   ação: índice da jogada (0 a 8)
# Valor: número real representando o valor Q daquela ação naquele estado

Q = {}  # Dicionário global para armazenar os valores Q


def obter_valor_Q(estado, acao):
    # Retorna o valor Q(estado, ação) se existir, senão retorna 0.0
    # Isso significa que inicialmente todas as ações têm valor 0
    return Q.get((estado, acao), 0.0)


def definir_valor_Q(estado, acao, valor):
    # Define o valor Q(estado, ação) no dicionário Q
    Q[(estado, acao)] = valor


def escolher_acao_epsilon_greedy(estado, jogador, epsilon):
    # Escolhe uma ação usando a política epsilon-greedy
    # 'estado' é o tabuleiro atual
    # 'jogador' é 'X' ou 'O' (quem está tomando a decisão)
    # 'epsilon' é a taxa de exploração (probabilidade de escolher ação aleatória)
    jogadas_possiveis = obter_jogadas_possiveis(estado)  # Lista de ações possíveis

    # Com probabilidade epsilon, escolhe uma jogada aleatória (exploração)
    if random.random() < epsilon:
        return random.choice(jogadas_possiveis)

    # Caso contrário, escolhe a ação com maior valor Q (exploração do que já aprendeu)
    melhor_valor = None  # Melhor valor Q encontrado
    melhores_acoes = []  # Lista de ações com melhor valor Q

    for acao in jogadas_possiveis:
        valor_q = obter_valor_Q(estado, acao)  # Valor Q para (estado, ação)
        if (melhor_valor is None) or (valor_q > melhor_valor):
            # Se ainda não temos melhor ou encontramos um Q maior, atualizamos
            melhor_valor = valor_q
            melhores_acoes = [acao]  # Começamos uma nova lista com essa ação
        elif valor_q == melhor_valor:
            # Empate de valor Q: adicionamos à lista para desempatar aleatoriamente
            melhores_acoes.append(acao)

    # Se houver várias melhores ações, escolhemos uma aleatoriamente entre elas
    return random.choice(melhores_acoes)


def atualizar_Q(estado, acao, recompensa, proximo_estado, alpha, gamma, jogo_terminou):
    # Atualiza o valor Q(estado, ação) usando a regra do Q-Learning
    # estado: estado atual
    # acao: ação tomada nesse estado
    # recompensa: recompensa recebida depois da ação
    # proximo_estado: estado após a ação
    # alpha: taxa de aprendizado
    # gamma: fator de desconto
    # jogo_terminou: booleano indicando se o próximo estado é terminal (fim do jogo)

    valor_atual = obter_valor_Q(estado, acao)  # Q(s, a) atual

    if jogo_terminou:
        # Se o jogo terminou, não há valor futuro, então alvo é só a recompensa
        alvo = recompensa
    else:
        # Se o jogo não terminou, consideramos o melhor valor futuro
        jogadas_possiveis = obter_jogadas_possiveis(proximo_estado)
        if not jogadas_possiveis:
            # Se por algum motivo não há jogadas possíveis, consideramos valor futuro 0
            melhor_valor_futuro = 0.0
        else:
            # Melhor valor Q no próximo estado
            melhor_valor_futuro = max(obter_valor_Q(proximo_estado, a) for a in jogadas_possiveis)
        # Alvo é recompensa imediata + valor futuro descontado
        alvo = recompensa + gamma * melhor_valor_futuro

    # Regra de atualização Q-Learning:
    # Q_novo = Q_atual + alpha * (alvo - Q_atual)
    novo_valor = valor_atual + alpha * (alvo - valor_atual)
    definir_valor_Q(estado, acao, novo_valor)  # Salva o novo valor na Q-table


########################
# TREINAMENTO DA IA
########################

def jogar_epoca_treinamento(alpha, gamma, epsilon):
    # Faz uma "época" (episódio) de treinamento completa.
    # A IA será o jogador 'X' e o oponente será um jogador aleatório 'O'.

    estado = inicializar_tabuleiro()  # Começa com tabuleiro vazio
    jogador_atual = "X"  # IA começa jogando
    jogo_terminou = False  # Flag para indicar se o jogo acabou

    while not jogo_terminou:
        # Verifica se o jogo já terminou antes da jogada
        resultado = verificar_vencedor(estado)
        if resultado is not None:
            # Se já terminou, saímos do loop
            jogo_terminou = True
            break

        if jogador_atual == "X":
            # Turno da IA: escolhe ação com epsilon-greedy
            acao = escolher_acao_epsilon_greedy(estado, jogador_atual, epsilon)
            proximo_estado = fazer_jogada(estado, acao, jogador_atual)  # Aplica a jogada

            # Verifica o resultado após a jogada
            resultado = verificar_vencedor(proximo_estado)

            # Define a recompensa de acordo com o resultado
            if resultado == "X":
                # IA ganhou
                recompensa = 1.0
                jogo_terminou = True
            elif resultado == "O":
                # IA perdeu (em teoria não deveria acontecer neste momento)
                recompensa = -1.0
                jogo_terminou = True
            elif resultado == "empate":
                # Empate
                recompensa = 0.0
                jogo_terminou = True
            else:
                # Jogo continua, sem recompensa imediata
                recompensa = 0.0
                jogo_terminou = False

            # Atualiza Q-table com base na jogada da IA
            atualizar_Q(estado, acao, recompensa, proximo_estado, alpha, gamma, jogo_terminou)

            # Atualiza o estado atual para o próximo
            estado = proximo_estado

            # Alterna jogador para o adversário aleatório
            jogador_atual = "O"

        else:
            # Turno do jogador 'O' (oponente aleatório)
            jogadas_possiveis = obter_jogadas_possiveis(estado)
            if not jogadas_possiveis:
                # Se não há jogadas, termina
                jogo_terminou = True
                break
            # Escolhe uma jogada aleatória para oponente
            acao = random.choice(jogadas_possiveis)
            # Aplica a jogada
            estado = fazer_jogada(estado, acao, jogador_atual)

            # Agora verificamos se o oponente venceu
            resultado = verificar_vencedor(estado)
            if resultado == "O":
                # IA perdeu, então precisamos dar recompensa negativa
                # Mas a atualização de Q da IA já foi feita na vez dela.
                # Uma forma simples: na próxima época a IA aprenderá a evitar esse estado.
                jogo_terminou = True
            elif resultado == "empate":
                # Empate
                jogo_terminou = True
            else:
                # Jogo continua; passa a vez para a IA novamente
                jogador_atual = "X"


def treinar_agente(num_epocas=5000, alpha=0.1, gamma=0.9, epsilon=0.1):
    # Função que repete várias épocas de treinamento
    # num_epocas: quantos jogos de treino serão simulados
    # alpha: taxa de aprendizado
    # gamma: fator de desconto
    # epsilon: taxa de exploração
    for epoca in range(num_epocas):
        # Para cada época, chamamos jogar_epoca_treinamento
        jogar_epoca_treinamento(alpha, gamma, epsilon)

        # (Opcional) você pode imprimir alguma coisa a cada N épocas para acompanhar
        # Aqui deixamos quieto para o treinamento ser rápido.


########################
# MODO DE JOGO HUMANO VS IA
########################

def escolher_acao_melhor(estado, jogador):
    # Escolhe a melhor ação conhecida pela Q-table (sem exploração, apenas exploração do aprendido)
    jogadas_possiveis = obter_jogadas_possiveis(estado)
    melhor_valor = None
    melhores_acoes = []

    for acao in jogadas_possiveis:
        valor_q = obter_valor_Q(estado, acao)
        if (melhor_valor is None) or (valor_q > melhor_valor):
            melhor_valor = valor_q
            melhores_acoes = [acao]
        elif valor_q == melhor_valor:
            melhores_acoes.append(acao)

    # Se por algum motivo não há jogadas possíveis, retorna None
    if not melhores_acoes:
        return None
    # Escolhe aleatoriamente entre as melhores ações
    return random.choice(melhores_acoes)


def jogar_contra_humano():
    # Permite que um humano jogue contra a IA treinada
    # IA será o jogador 'X'
    # Humano será 'O'
    estado = inicializar_tabuleiro()  # Tabuleiro vazio
    jogador_atual = "X"  # IA começa jogando

    print("Bem-vindo ao Jogo da Velha com IA (Q-Learning)!")
    print("A IA é 'X' e você é 'O'.\n")
    imprimir_tabuleiro(estado)

    while True:
        resultado = verificar_vencedor(estado)
        if resultado == "X":
            print("A IA venceu!")
            break
        elif resultado == "O":
            print("Você venceu! Parabéns!")
            break
        elif resultado == "empate":
            print("Empate!")
            break

        if jogador_atual == "X":
            # Turno da IA: escolhe a melhor ação conhecida
            acao = escolher_acao_melhor(estado, jogador_atual)
            if acao is None:
                # Se não houver jogadas, é empate
                print("Sem jogadas possíveis. Empate!")
                break
            estado = fazer_jogada(estado, acao, jogador_atual)
            print("IA jogou na posição", acao)
            imprimir_tabuleiro(estado)
            jogador_atual = "O"  # Passa a vez para o humano
        else:
            # Turno do humano
            jogadas_possiveis = obter_jogadas_possiveis(estado)
            print("Sua vez! Casas disponíveis:", jogadas_possiveis)
            try:
                entrada = input("Digite uma posição de 0 a 8: ")
                acao = int(entrada)  # Converte a entrada para inteiro
            except ValueError:
                print("Entrada inválida. Tente novamente.")
                continue

            # Verifica se a posição escolhida é válida
            if acao not in jogadas_possiveis:
                print("Jogada inválida. Tente novamente.")
                continue

            # Aplica a jogada do humano
            estado = fazer_jogada(estado, acao, jogador_atual)
            imprimir_tabuleiro(estado)
            jogador_atual = "X"  # Volta a vez para a IA


########################
# PROGRAMA PRINCIPAL
########################

if __name__ == "__main__":
    # Primeiro, treinamos a IA
    print("Treinando a IA... isso pode levar alguns segundos.")
    # Chamamos treinar_agente com parâmetros padrão
    treinar_agente(
        num_epocas=5000,  # Número de jogos de treino (pode aumentar ou diminuir)
        alpha=0.1,        # Taxa de aprendizado
        gamma=0.9,        # Fator de desconto
        epsilon=0.1       # Taxa de exploração
    )
    print("Treinamento concluído!\n")

    # Depois do treinamento, permitimos jogar contra a IA
    jogar_contra_humano()
