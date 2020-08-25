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

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***" 
        """ the result takes in care :
            1.the distance to the nearest ghost
            2.the score of the state
            3.the distance to the nearest food
            4.if the pacman has eat a power pellet and effect the ghosts 

        """
        #find the nearest ghost
        nearestGhostDist = float("inf")
        for ghost in newGhostStates:
            temp = manhattanDistance(newPos , ghost.configuration.pos)
            if nearestGhostDist > temp:
               nearestGhostDist = temp
            
            if ghost.configuration.pos == newPos:
                return -10000

        #find the nearest food
        nearestFood = float("inf")
        for food in newFood:
           temp = manhattanDistance(newPos,food)
           if nearestFood > temp:
               nearestFood = temp

        #find if there is effect from a power pellet
        scared = float("inf")
        for sc in newScaredTimes:
            if scared > sc:
                scared = sc

        nearestFoodStatistic =  1 / float(nearestFood) 
        score = successorGameState.getScore() * 0.5
        PelletsStatistic = scared * 0.5
        ghostDistanceStatistic = -1/ float(nearestGhostDist)
        
        #return the sum of all values
        return score + nearestFoodStatistic + ghostDistanceStatistic + PelletsStatistic

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
        """
        "*** YOUR CODE HERE ***"
        #this is the root of the minimax
        #every turn is a move for pacman and then a move for each existing ghost
        #so there is one max turn and then some min turns(equal to number of ghost)
        depth = 0
        agentIndex = 0
        max_action = ""
        max_val = - float("inf")
        actions = gameState.getLegalActions(agentIndex)
        #find the best move and return its action
        for action in actions:
            val = self.MINIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex +1 ,depth+1 )
            if val > max_val:
                max_val = val
                max_action = action
        return max_action
        util.raiseNotDefined()

    def MINIMAX(self, gameState, indexAgent, depth):
        agentsNumber = gameState.getNumAgents()
        # the base case which ends the minimax search and returns a value to the recursion
        if (depth == self.depth and indexAgent % agentsNumber == 0) or ( gameState.isWin() or gameState.isLose()) :
            return self.evaluationFunction(gameState) 

        #when plays the last ghost the indexAgent should be 0 to play pacman in next turn
        indexAgent = indexAgent % agentsNumber
        if indexAgent  == 0:
            return self.maxV(gameState,indexAgent,depth+1) #increase depth when pacman plays
        else:
            return self.minV(gameState,indexAgent,depth)


    def minV(self, gameState, indexAgent, depth):                
        actions = gameState.getLegalActions(indexAgent)
        #base case
        if (len(actions) == 0):
            return self.evaluationFunction(gameState)
        #find the best move for the ghost
        #increase the indexAgent every time
        minValue = float("inf")
        for action in actions:
            value = self.MINIMAX(gameState.generateSuccessor(indexAgent,action) , indexAgent+1, depth)
            if value < minValue:
                minValue = value

        return minValue 


    def maxV(self, gameState, indexAgent, depth):
    
        actions = gameState.getLegalActions(indexAgent)

        if (len(actions) == 0):
            return self.evaluationFunction(gameState) 
        #find the best move for the pacman
        #increase the indexAgent and the depth every time
        maxValue = - float("inf")
        for action in actions:
            value = self.MINIMAX(gameState.generateSuccessor(indexAgent,action), indexAgent+1, depth)
            if value > maxValue:
                maxValue = value

        return maxValue 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #the root of the minimax search with alpha beta pruning
        #initialize values
        depth = 0
        agentIndex = 0
        max_action = ""
        max_val = - float("inf")
        a = - float("inf")
        b = float("inf")
        actions = gameState.getLegalActions(agentIndex)
        #find the best move for the pacman who is in the root
        for action in actions:
            value = self.MINIMAX_AlphaBeta(gameState.generateSuccessor(agentIndex,action),agentIndex +1 ,depth+1 , a , b )
            if value > max_val:
                max_val = value
                max_action = action
            #check the pruning
            if value > b:
                return action
            if value > a:
                a = value

        return max_action

    def MINIMAX_AlphaBeta(self, gameState, indexAgent, depth , a , b):
        #same as MINIMAX of minimax search
        agentsNumber = gameState.getNumAgents()
        
        if (depth == self.depth and indexAgent % agentsNumber == 0) or ( gameState.isWin() or gameState.isLose()) :
            return self.evaluationFunction(gameState) 

        indexAgent = indexAgent % agentsNumber
        if indexAgent  == 0:
            return self.maxV_AlphaBeta(gameState,indexAgent,depth+1 , a , b)
        else:
            return self.minV_AlphaBeta(gameState,indexAgent,depth , a , b)


    def minV_AlphaBeta(self, gameState, indexAgent, depth , a, b):                
        actions = gameState.getLegalActions(indexAgent)
        #same as minV of minimax search with conditions for pruning some actions
        if (len(actions) == 0):
            return self.evaluationFunction(gameState)

        minValue = float("inf")
        for action in actions:
            value = self.MINIMAX_AlphaBeta(gameState.generateSuccessor(indexAgent,action) , indexAgent+1, depth,a,b)
            if value < minValue:
                minValue = value
            if value < a:
                return value
            if value < b:
                b = value
        return minValue 


    def maxV_AlphaBeta(self, gameState, indexAgent, depth, a, b):
    
        actions = gameState.getLegalActions(indexAgent)
        #same as maxV of minimax search with conditions for pruning some actions
        if (len(actions) == 0):
            return self.evaluationFunction(gameState) 

        maxValue = - float("inf")
        for action in actions:
            value = self.MINIMAX_AlphaBeta(gameState.generateSuccessor(indexAgent,action), indexAgent+1, depth,a,b)
            if value > maxValue:
                maxValue = value
            if value > b:
                return value
            if value > a:
                a = value
        return maxValue 

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
        #root of expectimax search
        #initialize values
        #same aw minimax but now the ghosts-min dont search for the better move , they earn a probability value for each move
        depth = 0
        agentIndex = 0
        max_action = ""
        max_val = - float("inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            val = self.expectiMAX(gameState.generateSuccessor(agentIndex,action),agentIndex +1 ,depth+1 )
            if val > max_val:
                max_val = val
                max_action = action
        return max_action
      
        util.raiseNotDefined()

    def expectiMAX(self, gameState, indexAgent, depth):
        agentsNumber = gameState.getNumAgents()
        #same as minimax
        if (depth == self.depth and indexAgent % agentsNumber == 0) or ( gameState.isWin() or gameState.isLose()) :
            return self.evaluationFunction(gameState)

        indexAgent = indexAgent % agentsNumber
        if indexAgent  == 0:
            return self.maxV(gameState,indexAgent,depth+1)
        else:
            return self.probV(gameState,indexAgent,depth)


    def probV(self, gameState, indexAgent, depth):                
        actions = gameState.getLegalActions(indexAgent)

        if (len(actions) == 0):
            return self.evaluationFunction(gameState)
        #earn the probability value as a sum of all values from the actions divide by the number of the actions
        value = 0 
        NumActions = 0
        for action in actions:
            v = self.expectiMAX(gameState.generateSuccessor(indexAgent,action) , indexAgent+1, depth)
            value = value + v
            NumActions = NumActions+1

        return float(value) / NumActions


    def maxV(self, gameState, indexAgent, depth):
        #same as minimax
        actions = gameState.getLegalActions(indexAgent)

        if (len(actions) == 0):
            return self.evaluationFunction(gameState) 

        maxValue = - float("inf")
        for action in actions:
            value = self.expectiMAX(gameState.generateSuccessor(indexAgent,action), indexAgent+1, depth)
            if value > maxValue:
                maxValue = value

        return maxValue 

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """ the result takes in care :
        1.the distance to the nearest ghost
        2.the score of the state
        3.the distance to the nearest food
        4.if the pacman has eat a power pellet and effect the ghosts 
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    #find the distance to the nearest ghost
    nearestGhostDist = float("inf")
    for ghost in newGhostStates:
        temp = manhattanDistance(newPos , ghost.configuration.pos)
        if nearestGhostDist > temp:
           nearestGhostDist = temp
            
        if ghost.configuration.pos == newPos:
            return -10000

    #find the distance to the nearest food
    nearestFood = float("inf")
    for food in newFood:
       temp = manhattanDistance(newPos,food)
       if nearestFood > temp:
           nearestFood = temp

    #find if there is effect from a power pellet
    scared = float("inf")
    for sc in newScaredTimes:
        if scared > sc:
            scared = sc

    nearestFoodStatistic =  1 / float(nearestFood)
    PelletsStatistic = scared * 0.5
    score = currentGameState.getScore() * 0.5 
    
    #if the ghosts are scared dont take in mind the distance to the nearest ghost
    if scared == 0:
        ghostDistanceStatistic = -1 / float(nearestGhostDist)
    else:
        ghostDistanceStatistic = 1

    return score + ghostDistanceStatistic + nearestFoodStatistic + PelletsStatistic
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

