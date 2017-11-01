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
import operator

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        return successorGameState.getScore()

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
    Both this and the AlphaBeta algorithm is a dirrect translation of the books example exept for the handeling of more than two agents
    """

    #function for the maximizing player, in this case pacman. Packman wants to pick the highest score he can
    def maxAgent(self, gameState, depth, agent, pacman = 0):
        #if we have reached an end state, return the evaluation of the gamestate. This is the same as Terminal-test in the book
        if depth == 0 or gameState.getLegalActions() == []:
            return self.evaluationFunction(gameState),None
        value = bestValue= float("-inf")
        bestAction = None
        #for all the actions that pacman can do, find the highest value it can and the corresponding action, this is the same as the for-each action in state part form the book
        #the action is only used in the getAction function
        for action in gameState.getLegalActions(pacman):
            #since we know the next agent is the first ghost we can just call the next agen nr.1
            #This will go recursively until eighter a ghost or pacman reaches an end state
            value =  self.minAgent(gameState.generateSuccessor(pacman, action), depth, 1)
            if value > bestValue:
                bestAction = action
                bestValue = value
        return bestValue, bestAction

    #function for the minimizing agents, in this case the ghosts. They want to pick the lowest score possible.
    #I didn't comment this as it's pretty much the exact same as the maxAgent exept that we need to check what the next agent
    #is so we can call maxAgent again when its pacmans turn
    def minAgent(self, gameState, depth, agent, pacman = 0):
        if depth == 0 or gameState.getLegalActions() == []:
            return self.evaluationFunction(gameState)
        value = float("inf")
        if agent + 1 == gameState.getNumAgents():
            for action in gameState.getLegalActions(agent):
                value = min(value, self.maxAgent(gameState.generateSuccessor(agent, action), depth-1, 0)[0])
        else:
            for action in gameState.getLegalActions(agent):
                value = min(value, self.minAgent(gameState.generateSuccessor(agent, action), depth, agent+1))
        return value

    def getAction(self, gameState):
        #since we are pacman we need to maximize the score
        return self.maxAgent(gameState, self.depth,0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):

    """
    The AlphaBetaAgent is not commented since its exactly the same as MinimaxAgent exept for the alfa and beta test.
    The algorithm is more effichent than the normal Minimax algorithm because it doesn't expand nodes that it knows can't
    give a lower/higher value. The alpha value is the highest value we have found along the path and beta is the lowest.
    As in the book the logic behind the alfa and beta values can be found in the for loops for each agent function.
    """
    def maxAgent(self, gameState, depth, agent,alpha,beta, pacman = 0):
        if depth == 0 or gameState.getLegalActions() == []:
            return self.evaluationFunction(gameState), None
        value = bestValue= float("-inf")
        bestAction = None
        for action in gameState.getLegalActions(pacman):
            value =  self.minAgent(gameState.generateSuccessor(pacman, action), depth, 1,alpha,beta)
            if value > bestValue:
                bestAction = action
                bestValue = value
            if bestValue > beta:
                return bestValue,bestAction
            alpha =max(alpha,bestValue)
        return bestValue, bestAction

    def minAgent(self, gameState, depth, agent,alpha,beta, pacman = 0):
        if depth == 0 or gameState.getLegalActions() == []:
            return self.evaluationFunction(gameState)
        value = float("inf")
        if agent + 1 == gameState.getNumAgents():
            for action in gameState.getLegalActions(agent):
                value = min(value, self.maxAgent(gameState.generateSuccessor(agent, action), depth-1, 0,alpha,beta)[0])
                if value < alpha:
                    return value
                beta = min(beta,value)
        else:
            for action in gameState.getLegalActions(agent):
                value = min(value, self.minAgent(gameState.generateSuccessor(agent, action), depth, agent+1,alpha,beta))
                if value < alpha:
                    return value
                beta = min(beta,value)
        return value

    def getAction(self, gameState):
        #since we are pacman we need to maximize the score
        return self.maxAgent(gameState, self.depth,0,float("-inf"),float("inf"))[1]


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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
