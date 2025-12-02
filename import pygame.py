import random

class GameState:
    def __init__(self, pacman_pos, ghost_positions, pellets, score=0, is_over=False):
        self.pacman_pos = pacman_pos
        self.ghost_positions = ghost_positions
        self.pellets = pellets  # conjunto de posições
        self.score = score
        self.is_over = is_over

    def getNumAgents(self):
        return 1 + len(self.ghost_positions)

    def isWin(self):
        # ganha se coletou todas moedas
        return len(self.pellets) == 0

    def isLose(self):
        # perde se Pacman na mesma posição que algum fantasma
        return self.pacman_pos in self.ghost_positions

    def getLegalActions(self, agentIndex):
        # Gera ações válidas para cada agente: 'Up', 'Down', 'Left', 'Right', 'Stop'
        directions = ['Up', 'Down', 'Left', 'Right', 'Stop']
        pos = self.pacman_pos if agentIndex == 0 else self.ghost_positions[agentIndex - 1]
        valid = []
        for d in directions:
            new_pos = self.generateNewPos(pos, d)
            if 0 <= new_pos[0] < 5 and 0 <= new_pos[1] < 5:  # limite 5x5 para simplicidade
                valid.append(d)
        return valid

    def generateNewPos(self, pos, direction):
        x, y = pos
        if direction == 'Up':
            return (x, y-1)
        elif direction == 'Down':
            return (x, y+1)
        elif direction == 'Left':
            return (x-1, y)
        elif direction == 'Right':
            return (x+1, y)
        else:
            return (x, y)

    def generateSuccessor(self, agentIndex, action):
        # gera próximo estado após um agente fazer um movimento
        if self.isWin() or self.isLose():
            return self  # estado terminal sem mudanças
        pacman_pos = self.pacman_pos
        ghost_positions = list(self.ghost_positions)
        pellets = set(self.pellets)
        score = self.score

        if agentIndex == 0:
            # atualiza posição do Pacman
            new_pos = self.generateNewPos(pacman_pos, action)
            pacman_pos = new_pos
            # coleta pellet se existir
            if new_pos in pellets:
                pellets.remove(new_pos)
                score += 10
        else:
            # atualiza posição do fantasma
            new_pos = self.generateNewPos(ghost_positions[agentIndex -1], action)
            ghost_positions[agentIndex -1] = new_pos

        return GameState(pacman_pos, tuple(ghost_positions), pellets, score, False)

class MinimaxAgent:
    def __init__(self, depth=2):
        self.depth = depth
        self.index = 0  # Pacman é o agente 0

    def evaluationFunction(self, state):
        # Avalia posição por score e distância para fantasmas (quanto mais longe, melhor)
        if state.isLose():
            return -float('inf')
        if state.isWin():
            return float('inf')
        pac_pos = state.pacman_pos
        ghost_dist = min(abs(pac_pos[0]-gx)+abs(pac_pos[1]-gy) for gx,gy in state.ghost_positions)
        return state.score - 2 / max(ghost_dist, 1)

    def getAction(self, gameState):
        def minimax(agentIndex, depth, state):
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            num_agents = state.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents
            next_depth = depth + 1 if next_agent == 0 else depth
            legalActions = state.getLegalActions(agentIndex)
            if agentIndex == 0:  # maximizador
                max_score = -float('inf')
                best_action = None
                for action in legalActions:
                    val = minimax(next_agent, next_depth, state.generateSuccessor(agentIndex, action))
                    if val > max_score:
                        max_score = val
                        best_action = action
                if depth == 0:
                    return best_action
                else:
                    return max_score
            else:  # minimizador (fantasmas)
                min_score = float('inf')
                for action in legalActions:
                    val = minimax(next_agent, next_depth, state.generateSuccessor(agentIndex, action))
                    min_score = min(min_score, val)
                return min_score

        return minimax(0, 0, gameState)

# Usa o agente aprofundando em 2 níveis exemplos
if __name__ == "__main__":
    pellets = {(1,1), (2,2), (3,3)}
    ghosts = ((4,4), (0,4))
    currentState = GameState((0,0), ghosts, pellets)
    agent = MinimaxAgent(depth=2)

    action = agent.getAction(currentState)
    print(f"Ação escolhida para Pac-Man: {action}")
