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
        new_food=newFood.asList()
        ghost_pos=successorGameState.getGhostPositions()
        posx,posy=newPos
        score=successorGameState.getScore()
        closest_ghost=ghost_pos[0] #this will keep track og the ghost that is closer to the pacman
        n=0
        #if there is a ghost in pacman proximity we return -99999 so he for sure doesnt go that way
        for i in range(0,len(ghost_pos)):
            ghostx=ghost_pos[n][0]
            ghosty=ghost_pos[n][1]
            if (abs(posx-ghost_pos[n][0]) +  abs(posy-ghost_pos[n][1])) < (abs(posx-ghost_pos[n-1][0]) +  abs(posy-ghost_pos[n-1][1])):
                closest_ghost=ghost_pos[n]
            if (abs(posx-ghostx) +  abs(posy-ghosty)) <=1:
                score=-99999
                return score
            n+=1
        #if new_food is empty we take the step to win the game or if there is a food in the new position we must go there
        #this might sound greedy but it works just fine because we checked for ghosts in that position in the previous loop so it is safe to go
        if not new_food or newPos in new_food:
            score=99999
            return score
        #if the new position is neutral we add the manhattan distance of the closest food minus the manhattan of the new position and the ghost's position
        min,min_food=9999,0
        #in this loop we search for the closest food
        for food in new_food:
            if util.manhattanDistance(newPos,food) < min:
                min=manhattanDistance(newPos,food)
                min_food=food
        score = score + 1/float(util.manhattanDistance(newPos,min_food)) -  1/float(util.manhattanDistance(newPos,closest_ghost))
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
        self.move=0 #I added a variable here so we store the pacman action from each value chosen in minimax tree

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
        #we pass self.depth*gameState.getNumAgents() in the function because we have more than one agent and all agents need to have a layer in the tree based on the depth
        self.max_value(self.depth*gameState.getNumAgents(),gameState)
        return self.move
        util.raiseNotDefined()
    
    #this is the maximizing function for pacman
    def max_value(self,depth,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            #we store the values in a list because we also want to store the action paired with each value
            v.append((self.min_value(depth-1,1,gameState.generateSuccessor(0,action)),action))
        max_val = max(v) #picking the max
        self.move=max_val[1] #here we store the action of the pacman each time (the last one will be the chosen action)
        return max_val[0]

    #this one is for ghosts
    def min_value(self,depth,player,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        actions = gameState.getLegalActions(player)
        for action in actions:
            if player+1 == gameState.getNumAgents(): #if we don't need to add any more minimum layers in the tree then its time for pacman to play
                v.append((self.max_value(depth-1,gameState.generateSuccessor(player,action)),action))
            else: #here we add all the minimum layers in the tree
                v.append((self.min_value(depth-1,player+1,gameState.generateSuccessor(player,action)),action))
        min_ = min(v)
        return min_[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.max_value(self.depth*gameState.getNumAgents(),-99999,99999,gameState)
        return self.move
        util.raiseNotDefined()

    #This is alphsa beta pruning algorithm implemented just like Question 3 shows with the peudocode, the only difference is 
    # that I use a list to store values just like in the minimax algorithm, because i want to store the pcman action paired with each value
    def max_value(self,depth,a,b,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            v.append((self.min_value(depth-1,1,a,b,gameState.generateSuccessor(0,action)),action))
            #because I work with v to be a list I check the last node inserted each time if it is bigger than b
            if v[len(v)-1][0] > b:
                max_val = max(v)
                self.move=max_val[1] #here I store the pacman move each time (the last one that is stored will be the correct move from the state we are)
                return max_val[0]
            max_val = max(v)
            a=max(a,max_val[0]) #rearranging a
        #if the for loop finishes that means we checked all the children of the node without pruning so it acts like minimax
        max_val = max(v)
        self.move=max_val[1]
        return max_val[0]
    
    #this is the minimazing alpha-beta function that works just like the previous one and adds as many minimum layers as the ghost agents (just like minimax) 
    # and checks each layer for alpha beta pruning
    def min_value(self,depth,player,a,b,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        actions = gameState.getLegalActions(player)
        for action in actions:
            if player+1 == gameState.getNumAgents():
                v.append((self.max_value(depth-1,a,b,gameState.generateSuccessor(player,action)),action))
                if v[len(v)-1][0] < a:
                    min_ = min(v)
                    return min_[0]
                min_ = min(v)
                b=min(b,min_[0])
            else:
                v.append((self.min_value(depth-1,player+1,a,b,gameState.generateSuccessor(player,action)),action))
                if v[len(v)-1][0] < a:
                    min_ = min(v)
                    return min_[0]
                min_ = min(v)
                b=min(b,min_[0])
        min_ = min(v)
        return min_[0]

#This function has the same code as minimax only 3 lines change at the exp_value (which is the the previous min_value) 
# that return the average of each ghost's action instead of the minimum
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        self.max_value(self.depth*gameState.getNumAgents(),gameState)
        return self.move
        util.raiseNotDefined()
    
    def max_value(self,depth,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            v.append((self.exp_value(depth-1,1,gameState.generateSuccessor(0,action)),action))
        max_val = max(v)
        self.move=max_val[1]
        return max_val[0]

    def exp_value(self,depth,player,gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = []
        exp=0
        actions = gameState.getLegalActions(player)
        for action in actions:
            if player+1 == gameState.getNumAgents():
                v.append((self.max_value(depth-1,gameState.generateSuccessor(player,action)),action))
            else:
                v.append((self.exp_value(depth-1,player+1,gameState.generateSuccessor(player,action)),action))
        #adding all values
        for i in range (len(v)):
            exp += v[i][0]
        #returning the average
        return exp/len(actions)
        util.raiseNotDefined()

#This function is almost the same as the previous evaluation function I made but also chases the ghosts if they are scared 
# so it achieves better score
def betterEvaluationFunction(currentGameState):

    pos = currentGameState.getPacmanPosition()

    newFood = currentGameState.getFood()
    new_food=newFood.asList()

    score=currentGameState.getScore()

    #saving the new scared times of ghosts
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    ghost_pos=currentGameState.getGhostPositions()
    closest_ghost=ghost_pos[0]
    #finding the closest ghost and returning -inf if it is ready to eat the pacman
    for ghost in ghost_pos:
        if util.manhattanDistance(pos,ghost) < util.manhattanDistance(pos,closest_ghost):
            closest_ghost=ghost
        if util.manhattanDistance(pos,ghost) <=1:
            score=-99999
            return score
    #if new_food is empty we take the step to win the game or if there is a food in the position we must go there
    #this might sound greedy but it works just fine because we checked for ghosts in that position in the previous loop so it is safe to go
    if not new_food or pos in new_food:
        score=99999
        return score
    #finding the closest food here
    min,min_food=9999,0
    for food in new_food:
        if util.manhattanDistance(pos,food) < min:
            min=manhattanDistance(pos,food)
            min_food=food
    #if newScaredTimes[0] != 0 that means the ghosts are scared so WE ADD the manhattan of the closest ghost ISTEAD OF SUBTRACTING it
    if newScaredTimes[0] != 0:
        score = score + 1/float(util.manhattanDistance(pos,min_food)) +  1/float(util.manhattanDistance(pos,closest_ghost))
        return score
    score = score + 1/float(util.manhattanDistance(pos,min_food)) -  1/float(util.manhattanDistance(pos,closest_ghost))
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
