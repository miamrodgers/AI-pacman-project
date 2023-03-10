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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
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

    def evaluationFunction(self, currentGameState, action):
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
        from util import manhattanDistance
        # maximize scared times
        # maximize distance from closest ghost
        # minimize distance from furthest food
        # minimize number of food left
        
        score = 0

        foodList = [manhattanDistance(newPos,food) for food in newFood.asList()]        
        ghostList = [manhattanDistance(newPos,ghost) for ghost in successorGameState.getGhostPositions()]
        
        if len(foodList)==0:
            return 1000
        score += 1/max(foodList)*200
        score += 1/min(foodList)*200
        if(newPos in currentGameState.getFood().asList()):
            score += 1000
        if(min(newScaredTimes) > 2):
            score += 1/min(ghostList)*100
        else:
            if(min(ghostList) == 1):
                return -1000
            if(min(ghostList) < 3):
                score -= 1000
            else:
                score += min(ghostList)
        return score

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        return self.max_value(gameState, 0)[1]
             

    def max_value(self, gameState, depth):
        legal_actions = gameState.getLegalActions(0)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")
        max_val = (float("-inf"), "")

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            current_value = self.min_value(successor, depth, 1)
            if current_value[0] > max_val[0]:
                max_val = (current_value[0], action)
            
        return max_val
            
    def min_value(self, gameState, depth, agent_index):
        legal_actions = gameState.getLegalActions(agent_index)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")
        
        min_val = (float("inf"), "")

        for action in legal_actions:
            successor = gameState.generateSuccessor(agent_index, action)
            successor_index = (agent_index + 1) % gameState.getNumAgents()
            if successor_index == 0:
                current_value = self.max_value(
                    successor, depth+1)
            else:
                current_value = self.min_value(
                    successor, depth, successor_index)
            if current_value[0] < min_val[0]:
                min_val = (current_value[0], action)

        return min_val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, 0, float("-inf"), float("inf"))[1]
    

    def max_value(self, gameState, depth, alpha, beta):
        legal_actions = gameState.getLegalActions(0)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")
        max_val = (float("-inf"), "")

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            current_value = self.min_value(successor, depth, 1, alpha, beta)
            if current_value[0] > max_val[0]:
                max_val = (current_value[0], action)
            alpha = max(alpha, max_val[0])
            if max_val[0] > beta:
                return max_val
        return max_val

    def min_value(self, gameState, depth, agent_index, alpha, beta):
        legal_actions = gameState.getLegalActions(agent_index)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")

        min_val = (float("inf"), "")

        for action in legal_actions:
            successor = gameState.generateSuccessor(agent_index, action)
            successor_index = (agent_index + 1) % gameState.getNumAgents()
            if successor_index == 0:
                current_value = self.max_value(
                    successor, depth+1, alpha, beta)
            else:
                current_value = self.min_value(
                    successor, depth, successor_index, alpha, beta)
            if current_value[0] < min_val[0]:
                min_val = (current_value[0], action)
            beta = min(beta, min_val[0])
            if min_val[0] < alpha:
                return min_val
        return min_val

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, 0)[1]
             

    def max_value(self, gameState, depth):
        legal_actions = gameState.getLegalActions(0)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")
        max_val = (float("-inf"), "")

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            current_value = self.expected_value(successor, depth, 1)
            if current_value[0] > max_val[0]:
                max_val = (current_value[0], action)
            
        return max_val
            
    def expected_value(self, gameState, depth, agent_index):
        legal_actions = gameState.getLegalActions(agent_index)
        # Check if terminal state, if so return evaluation function
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "")
        
        min_val = (float("inf"), "")
        total_util = 0
        for action in legal_actions:
            successor = gameState.generateSuccessor(agent_index, action)
            successor_index = (agent_index + 1) % gameState.getNumAgents()
            if successor_index == 0:
                current_value = self.max_value(
                    successor, depth+1)
            else:
                current_value = self.expected_value(
                    successor, depth, successor_index)
            
            total_util += current_value[0]
        
        return (total_util/len(legal_actions), "")

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: this evaluation function gives a score to a gameState based 
    on the whether the current state is a winning or losing state, the game 
    score, distance to nearest capsule, distance to nearest food, the remaining 
    scare time of the ghosts and distance to the ghosts

    """
    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    numGhosts = len(ghostStates)
    ghostPositions = [ghostState.getPosition() for ghostState in ghostStates]
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    score = currentGameState.getScore()

    if currentGameState.isWin():
        return 10000
    if currentGameState.isLose():
        return -10000
    for capsule in capsules:
        score -= manhattanDistance(pos,capsule)
        
    score -= min([manhattanDistance(pos,f) for f in food.asList()])

    for i in range(numGhosts):
        if scaredTimes[i] > 0:
            score += 100
        score += manhattanDistance(pos,ghostPositions[i])

    return score
    

# Abbreviation
better = betterEvaluationFunction
