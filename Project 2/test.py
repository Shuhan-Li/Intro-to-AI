class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        max_layer = self.depth
        # if self.depth == 1:
        #     max_layer = 9
        # elif self.depth == 2:
        #     max_layer = 8
        # elif self.depth == 3:
        #     max_layer = 7
        # elif self.depth == 4:
        #     max_layer = -492

        action, score = self.minmax(0,0,gameState,max_layer)
        return action

    def minmax(self,current_d,agent, gameState, max_layer):
        if agent >= gameState.getNumAgents():
            agent = 0
            current_d += 1
        if current_d == max_layer:
            return None, self.evaluationFunction(gameState)
        max_score = None
        best_action = None

        if agent == 0:
            actions = gameState.getLegalActions(agent)
            for a in actions:
                next_state = gameState.generateSuccessor(agent, a)
                action, score = self.minmax(current_d,agent+1,next_state,max_layer)
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = action
        else:
            gAction = gameState.getLegalActions(agent)
            for a in gAction:
                next_state = gameState.generateSuccessor(agent,a)
                action, score = self.minmax(current_d,agent+1,next_state,max_layer)

                if max_score is None or score < max_score:
                    max_score = score
                    best_action = action

            if max_score is None:
                return None, self.evaluationFunction(gameState)
        return best_action, max_score




    pacPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    gohstPos = currentGameState.getGhostStates()

    gohstDis = 0.0
    for g in gohstPos:
        gd = util.manhattanDistance(g.getPosition(), pacPos)
        if gd>0:
            if gohstPos.scaredTimer > 0:
                gohstDis+=5
            else:
                gohstDis-=100

    min = 9999999.0

    for f in foods:
        tmp = util.manhattanDistance(f, pacPos)
        if tmp < min:
            min = tmp
    min = -min
    return currentGameState.getScore()+min+gohstDis