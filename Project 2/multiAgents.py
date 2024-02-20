# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"


        min = 9999999.0

        foods = currentGameState.getFood().asList()

        for f in foods:
            tmp = util.manhattanDistance(f,newPos)
            if tmp < min:
                min = tmp
        min = -min
        for s in newGhostStates:
            if s.scaredTimer == 0 and newPos == s.getPosition():
                return -9999

        if action == 'stop':
            return -9999

        return min

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

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
                score = self.minmax(current_d,agent+1,next_state,max_layer)[1]
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = a
        else:
            gAction = gameState.getLegalActions(agent)
            for a in gAction:
                next_state = gameState.generateSuccessor(agent,a)
                score = self.minmax(current_d,agent+1,next_state,max_layer)[1]

                if max_score is None or score < max_score:
                    max_score = score
                    best_action = a

        if max_score is None:
            return None, self.evaluationFunction(gameState)
        return best_action, max_score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
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

        alpha = float('inf')*-1
        beta = float('inf')
        action, score = self.minmax(0, 0, gameState, max_layer,alpha, beta)
        return action

    def minmax(self, current_d, agent, gameState, max_layer,alpha, beta):
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
                score = self.minmax(current_d, agent + 1, next_state, max_layer,alpha, beta)[1]
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = a
                alpha = max(score, alpha)
                if alpha > beta:
                    break
        else:
            gAction = gameState.getLegalActions(agent)
            for a in gAction:
                next_state = gameState.generateSuccessor(agent, a)
                score = self.minmax(current_d, agent + 1, next_state, max_layer,alpha, beta)[1]

                if max_score is None or score < max_score:
                    max_score = score
                    best_action = a
                beta = min(score, beta)
                if beta < alpha:
                    break

        if max_score is None:
            return None, self.evaluationFunction(gameState)
        return best_action, max_score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
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

        action, score = self.minmax(0, 0, gameState, max_layer)
        return action

    def minmax(self, current_d, agent, gameState, max_layer):
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
                score = self.minmax(current_d, agent + 1, next_state, max_layer)[1]
                if max_score is None or score > max_score:
                    max_score = score
                    best_action = a
        else:
            gAction = gameState.getLegalActions(agent)
            prob = 0
            if len(gAction) != 0:
                prob = 1 / len(gAction)
            for a in gAction:
                next_state = gameState.generateSuccessor(agent, a)
                score = self.minmax(current_d, agent + 1, next_state, max_layer)[1]

                if max_score is None:
                    max_score = 0.0
                max_score += score* prob
                best_action = a

        if max_score is None:
            return None, self.evaluationFunction(gameState)
        return best_action, max_score

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Max score =  current score + food award + ghost distance punishment(negative when scared and positive otherwise)
    """

    "*** YOUR CODE HERE ***"

    pacPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    gohstPos = currentGameState.getGhostStates()

    gohstDis = 0.0
    for g in gohstPos:
        gd = util.manhattanDistance(g.getPosition(), pacPos)
        if gd>0:
            if g.scaredTimer > 0:
                gohstDis+=10/gd
            else:
                gohstDis-=100/gd

    min = 9999999.0

    for f in foods:
        tmp = util.manhattanDistance(f, pacPos)
        if tmp < min:
            min = tmp
    min = -min
    return currentGameState.getScore()+10/min*1.25+gohstDis

# Abbreviation
better = betterEvaluationFunction
