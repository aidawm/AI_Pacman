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
from game import AgentState
import random, util

from util import manhattanDistance

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
    
    def find_nearest_object (self,pos,object_list):
    
        nearest_object = None
        nearest_object_dist = 100000
        
        for o in object_list : 
            if(type(o)== AgentState):
                d = manhattanDistance(pos,o.getPosition())
            else:
                d = manhattanDistance(pos,o)
            if(d < nearest_object_dist):
                nearest_object = o
                nearest_object_dist = d

        return (nearest_object,nearest_object_dist)

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
        if successorGameState.isWin():
            return 999999

        total_score = 0

        nearest_food,nearest_food_dist = self.find_nearest_object(newPos,newFood.asList())
        nearest_ghost,nearest_ghost_dist = self.find_nearest_object(newPos,newGhostStates)

        curr_state_near_food = manhattanDistance(currentGameState.getPacmanPosition(),nearest_food)
        if(len(newFood.asList()) < len(currentGameState.getFood().asList())):
            total_score += 2000
        if(curr_state_near_food  > nearest_food_dist):
            total_score += 1500/(nearest_food_dist**2)
        

        if(nearest_ghost_dist<=7):                  
   
            if(manhattanDistance(currentGameState.getPacmanPosition(), nearest_ghost.getPosition())< nearest_ghost_dist):
                capsule_list = successorGameState.getCapsules()
                if(len(capsule_list) >0):
                    nearest_capsule,nearest_capsule_dist = self.find_nearest_object(newPos,capsule_list)  
                    if(manhattanDistance(currentGameState.getPacmanPosition(),  nearest_capsule)< nearest_capsule_dist 
                        and not(nearest_ghost.scaredTimer >0) and nearest_capsule_dist <5):
                        total_score +=2000

                total_score += 1000
    

            if(nearest_ghost_dist<=3):

                if(manhattanDistance(currentGameState.getPacmanPosition(), nearest_ghost.getPosition())< nearest_ghost_dist):
                    total_score += 3000
                else :
                    if(nearest_ghost.scaredTimer >0):
                        if(nearest_ghost_dist < (nearest_ghost.scaredTimer-1)):
                            total_score +=1000
        
                        total_score -=500
                    else: 
                        total_score -=3000

 
        
        
        return total_score

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

    def get_agent_successor_list(self,gameState,agentid):

        agent_actions = gameState.getLegalActions(agentid)

        agent_successor =lambda  a : gameState.generateSuccessor(agentid,a)
        return [agent_successor(a) for a in agent_actions]


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
        pacman_index = 0


        successorGameState_list = self.get_agent_successor_list(gameState, pacman_index)

        pacman_successor_score =lambda successor_state : self.ghost_choices(successor_state, 0,1)

        pacman_score_list = [pacman_successor_score(s) for s in successorGameState_list]
        bestScore = max(pacman_score_list)
        bestIndices = [index for index in range(len(pacman_score_list)) if pacman_score_list[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        
        pacman_actions = gameState.getLegalActions(pacman_index)

        return pacman_actions[chosenIndex]


    def minimax_terminate_state(self,gameState,curr_depth):
        if gameState.isLose() or gameState.isWin():
            return 1
        
        if curr_depth == self.depth : 
            return 1

        return 0 



    def pacman_choices(self,gameState,curr_depth):
        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)

        successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,1)
        pacman_succesors = self.get_agent_successor_list(gameState,0)

        choices_list = [successor_score(s) for s in pacman_succesors]

        return max(choices_list)


    
    def ghost_choices(self,gameState,curr_depth,ghost_id):

        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)


        successor_score =   None

        if(ghost_id == (gameState.getNumAgents() -1) ):
            successor_score = lambda successor_state : self.pacman_choices(successor_state,(curr_depth+1))
        else:
            successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,(ghost_id+1))
        
        ghost_succesors = self.get_agent_successor_list(gameState,ghost_id)

        choices_list = [successor_score(s) for s in ghost_succesors]

        return min(choices_list)
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alfa = -999999
        beta = 999999
        pacman_index = 0
        best_action = -1
        pacman_actions = gameState.getLegalActions(pacman_index)
        for  a in pacman_actions:
        
            state = gameState.generateSuccessor(pacman_index,a)
            score = self.ghost_choices(state, 0,1,alfa,beta)
            
            if (score > alfa):
                alfa = score
                best_action = a
                
            if (alfa > beta):
                return best_action
        
        return best_action


        
    def minimax_terminate_state(self,gameState,curr_depth):
        if gameState.isLose() or gameState.isWin():
            return 1
        
        if curr_depth == self.depth : 
            return 1

        return 0 



    def pacman_choices(self,gameState,curr_depth,alfa,beta):
        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)
        pacman_score = -999999
        pacman_actions = gameState.getLegalActions(0)
        for  a in pacman_actions:
            state = gameState.generateSuccessor(0,a)
            successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,1,alfa,beta)
            score = successor_score(state)
            if(pacman_score < score):
                pacman_score = score
            
            alfa = max(alfa,score)
            if(alfa > beta):
                return alfa
        return pacman_score


    
    def ghost_choices(self,gameState,curr_depth,ghost_id,alfa,beta):
        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)
        ghost_score = 999999
        ghost_actions = gameState.getLegalActions(ghost_id)
        for  a in ghost_actions:
            state = gameState.generateSuccessor(ghost_id,a)

            successor_score =   None

            if(ghost_id == (gameState.getNumAgents() -1) ):
                successor_score = lambda successor_state : self.pacman_choices(successor_state,(curr_depth+1),alfa,beta)
            
            else:
                successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,(ghost_id+1),alfa,beta)

            score = successor_score(state)
            if(ghost_score>score):
                ghost_score = score

            beta = min(beta,score)
           
            if(alfa > beta):
                return beta
        

        return ghost_score
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def get_agent_successor_list(self,gameState,agentid):

        agent_actions = gameState.getLegalActions(agentid)

        agent_successor =lambda  a : gameState.generateSuccessor(agentid,a)
        return [agent_successor(a) for a in agent_actions]
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        "*** YOUR CODE HERE ***"
        pacman_index = 0


        successorGameState_list = self.get_agent_successor_list(gameState, pacman_index)

        pacman_successor_score =lambda successor_state : self.ghost_choices(successor_state, 0,1)

        pacman_score_list = [pacman_successor_score(s) for s in successorGameState_list]
        bestScore = max(pacman_score_list)
        bestIndices = [index for index in range(len(pacman_score_list)) if pacman_score_list[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        
        pacman_actions = gameState.getLegalActions(pacman_index)

        return pacman_actions[chosenIndex]


    def minimax_terminate_state(self,gameState,curr_depth):
        if gameState.isLose() or gameState.isWin():
            return 1
        
        if curr_depth == self.depth : 
            return 1

        return 0 



    def pacman_choices(self,gameState,curr_depth):
        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)

        successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,1)
        pacman_succesors = self.get_agent_successor_list(gameState,0)

        choices_list = [successor_score(s) for s in pacman_succesors]

        return max(choices_list)


    
    def ghost_choices(self,gameState,curr_depth,ghost_id):

        if self.minimax_terminate_state(gameState,curr_depth):
            return self.evaluationFunction(gameState)


        successor_score =   None

        if(ghost_id == (gameState.getNumAgents() -1) ):
            successor_score = lambda successor_state : self.pacman_choices(successor_state,(curr_depth+1))
        else:
            successor_score = lambda successor_state : self.ghost_choices(successor_state,curr_depth,(ghost_id+1))
        
        ghost_succesors = self.get_agent_successor_list(gameState,ghost_id)

        choices_list = [successor_score(s) for s in ghost_succesors]

        return sum(choices_list)/(len(choices_list))
        


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    new_scared_times = [ghostState.scaredTimer for ghostState in newGhostStates]

    food_distance = [0]
    for pos in newFood.asList():
        d = manhattanDistance(newPos, pos) 
        if d !=0:
            food_distance.append(1.0/d)
        else:
            food_distance.append(9999)

    ghost_distance = [0]
    for pos in [ghost.getPosition() for ghost in newGhostStates]:
        ghost_distance.append(manhattanDistance(newPos, pos))

    number_of_power_pellets = len(currentGameState.getCapsules())
    capsule_distance = [0]
    for pos in [capsule for capsule in currentGameState.getCapsules()] : 
        d = manhattanDistance(newPos, pos) 
        if(d!=0):
            capsule_distance.append(1.0/d)
        else : 
            capsule_distance.append(9999)

    min_food = 9999
    for f in food_distance :
        if(min_food> f):
            min_food = f 

    min_ghost = 9999
    for g in ghost_distance :
        if(min_ghost> g):
            min_ghost = g
    score = 0

    total_distance = sum(food_distance) 
    sum_scared_times = sum(new_scared_times)
    sum_ghost_distance = sum(ghost_distance)
    eaten_food_number = len(newFood.asList(False))

    score += currentGameState.getScore() + total_distance + eaten_food_number 

    if sum_scared_times > 0:
        score += sum_scared_times  - sum_ghost_distance + 2*min_food
    else:
        score += sum_ghost_distance + number_of_power_pellets +sum(capsule_distance) - min_ghost*4
    return score
    



# Abbreviation
better = betterEvaluationFunction
