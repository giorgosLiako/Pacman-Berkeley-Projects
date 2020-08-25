# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import *

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    
    """Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    explored = {}   #set to remember relationships father-child
    frontier = Stack()
    #node = [state,action,cost ,father]
    node = [problem.getStartState() ,[], 0 , []] #start node
    frontier.push(node)

    while frontier.isEmpty() == False:

        newNode = frontier.pop()
        #print newNode
        if problem.isGoalState( newNode[0]) == True: #found the goal
            path = []
            path.insert(0,newNode[1])  #take the last action to goal
            
            findpath = explored[(newNode[3])] #find the father of the goal(newNode[0])
            #take the path from the explored set
            #end when the father-node is the start node
            while findpath[1] != [] and findpath[1] != problem.getStartState():
                path.insert(0,findpath[0])  #insert in the front of the list path
                findpath = explored[(findpath[1])]  #take the father of the next node

            if findpath[1] != []:
                    path.insert(0,findpath[0]) #the first action from the start-node
            return path
        
        if newNode[0] not in explored: #dont explore an already explored node

            #remember father-child and the action from father to child
            #child is the key and the value is action,father 
            explored[(newNode[0])] = [ newNode[1] , newNode[3]] #child : action , father 
            print explored[(newNode[0])]
            successors = problem.getSuccessors(newNode[0])
            for succ in successors:
                if succ[0] not in explored and succ not in frontier.list:

                    nod = [succ[0] ,succ[1], succ[2] , newNode[0]] #make the node               
                    frontier.push(nod)  

    if (frontier.isEmpty() == True):
        return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first."
    "*** YOUR CODE HERE ***"
    node = [problem.getStartState() ,[], 0 , []]
    if problem.isGoalState( node[0]) == True:
        return []
    #same ad dfs but now we have a queue
    explored = {} #set to remember relationships father-child
    frontier = Queue()
    frontier.push(node)

    while frontier.isEmpty() == False:

        newNode = frontier.pop()

        if problem.isGoalState( newNode[0]) == True:
            path = []
            path.insert(0,newNode[1])
            findpath = explored[(newNode[3])]
                        
            while findpath[1] != [] and findpath[1] != problem.getStartState() : 
                path.insert(0,findpath[0])
                findpath = explored[(findpath[1])]

            if findpath[1] != []:
                path.insert(0,findpath[0])
            return path

        if newNode[0] not in explored: #not explored an already explored node
            #remember father-child and the action from father to child
            #child is the key and the value is action,father 
            explored[(newNode[0])] =   [ newNode[1] , newNode[3]]          
            successors = problem.getSuccessors(newNode[0])
            for succ in successors:
                if succ[0] not in explored and succ not in frontier.list:
                    #the same as dfs

                    nod = [succ[0] ,succ[1], succ[2] , newNode[0]] #make node                
                    frontier.push(nod)

    if (frontier.isEmpty() == True):
        return []


    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #node = [state,action,cost ,father]
    node = [problem.getStartState() ,[], 0 , []]
    if problem.isGoalState( node[0]) == True:
        return []
    
    explored = {} #set to remember relationships father-child
    frontier = PriorityQueue()
    frontier.push(node,node[2])

    while frontier.isEmpty() == False:

        newNode = frontier.pop()
        if problem.isGoalState( newNode[0]) == True:
            #same way to find the path as in the others functions
            path = []
            path.insert(0,newNode[1])
            findpath = explored[(newNode[3])]
            while findpath[1] != [] and findpath[1] != problem.getStartState() : 
                path.insert(0,findpath[0])
                findpath = explored[(findpath[1])]

            if findpath[1] != []:
                path.insert(0,findpath[0])
            return path


        if newNode[0] not in explored:   #dont explore an already explored node
            #remember father-child and the action from father to child
            #child is the key and the value is action,father 
            explored[(newNode[0])] = [ newNode[1] , newNode[3]]           
            successors = problem.getSuccessors(newNode[0])
            for succ in successors:
                if succ[0] not in explored and succ not in frontier.heap:
                    nod = [succ[0] ,succ[1], succ[2] +newNode[2] , newNode[0]]                
                    frontier.push(nod,succ[2]+newNode[2])

                elif succ in frontier.heap: 
                    #if this successor already exists in frontier
                    #but has bigger cost update this cost with the new smaller cost of this successor
                    for counter in frontier.heap:
                        if counter[0] == succ[0] and counter[2] > succ[2]:
                            succ[2] = succ[2]+newNode[2]
                            frontier.update(succ , succ[2])


    if (frontier.isEmpty() == True):
        return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #node = [state,action,cost ,father]
    node = [problem.getStartState() ,[], 0 , []]
    if problem.isGoalState( node[0]) == True:
        return []
    
    explored = {} #set to remember relationships father-child
    frontier = PriorityQueue()
    frontier.push(node,node[2] + heuristic(node[0],problem))

    while frontier.isEmpty() == False:

        newNode = frontier.pop()
        if problem.isGoalState( newNode[0]) == True:
            #same way to find the path as in the others functions
            path = []
            path.insert(0,newNode[1])
            findpath = explored[(newNode[3])]
            while findpath[1] != [] and findpath[1] != problem.getStartState() : 
                path.insert(0,findpath[0])
                findpath = explored[(findpath[1])]

            if findpath[1] != []:
                path.insert(0,findpath[0])
            return path

        if newNode[0] not in explored:   #dont explore an already explored node
            #remember father-child and the action from father to child
            #child is the key and the value is action,father 
            explored[(newNode[0])] = [ newNode[1] , newNode[3]]            
            successors = problem.getSuccessors(newNode[0])
            for succ in successors:
                if succ[0] not in explored or succ not in frontier.heap:
                    nod = [succ[0] ,succ[1], succ[2] + newNode[2] , newNode[0]]                
                    frontier.push(nod,succ[2]+newNode[2] + heuristic(succ[0],problem))

                elif succ in frontier.heap:
                    #if this successor already exists in frontier
                    #but has bigger cost update this cost with the new smaller cost of this successor                   
                    for counter in frontier.heap:
                        if counter[0] == succ[0] and counter[2] > succ[2]:
                            succ[2] = succ[2]+newNode[2] + heuristic(succ[0],problem)
                            frontier.update(succ , succ[2])

    if (frontier.isEmpty() == True):
        return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
