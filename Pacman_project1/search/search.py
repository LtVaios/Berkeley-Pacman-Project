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
from util import Stack 
from util import Queue
from util import PriorityQueue
from game import Directions

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
    st = Stack()
    checked=set() #this is the set of the visited nodes
    st.push(problem.getStartState())
    father={} #this is the dictionary to hold the father node of all nodes and the action to get from the father to the child node
    #deapth first search method without the pathing to goal
    while 1:
        temp=st.pop()
        checked.add(temp)
        if problem.isGoalState(temp):
            break
        succ=problem.getSuccessors(temp)
        for succesor,direc,cost in succ:
            if succesor not in checked:
                st.push(succesor)
                father[succesor]=(temp,direc)
    #making the path to the goal using the father dictionary
    dest=temp #destination node will always be the last node we poped out of the frontier
    #we begin from the destination and we go backwards until the start state by bacjtracing nodes (and actions) into the father dictionary
    path=[]
    while dest!=problem.getStartState(): 
        path.insert(0,father[dest][1]) #path stores the actions (we insert them at the start so the result will be the original path not the backtracked one)
        dest=father[dest][0]
    return path
    util.raiseNotDefined()

#BFS is almost the same as DFS only the data structure changes
def breadthFirstSearch(problem):
    qu = Queue()
    checked=set()
    qu.push(problem.getStartState())
    father={}
    while 1:
        temp=qu.pop()
        checked.add(temp)
        if problem.isGoalState(temp):
            break
        succ=problem.getSuccessors(temp)
        for succesor,direc,cost in succ:
            if succesor not in checked and succesor not in qu.list:
                qu.push(succesor)
                father[succesor]=(temp,direc)
    dest=temp
    path=[]
    while dest!=problem.getStartState(): 
        path.insert(0,father[dest][1])
        dest=father[dest][0]
    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    pq = PriorityQueue()
    checked=set()
    father={}
    pq.push(problem.getStartState(),0)
    #flag is a helping tool that helps us find if a node already exists in the heap, 
    #if it does then we dont proceed to adding that node into the heap and istead we update its priority(if its needed)
    flag=0
    while(not pq.isEmpty()):
        #cost holds the cumulative cost of the node we will pop because we need to add it in his kids cost
        cost=pq.heap[0] 
        temp=pq.pop() 
        checked.add(temp)
        if problem.isGoalState(temp):
            break
        succ=problem.getSuccessors(temp) #taking all neighboor nodes of the poped one
        for succesor,direc,cost_2 in succ:
            #now we search if the node is already in the heap and we update its priority if its needed
            for pri,count,item  in pq.heap:
                if succesor==item:
                    pq.update(succesor,cost_2+cost[0])
                    if(pri > cost_2+cost[0]): #if the priority gets updated then we also update the father of the node to the current that has lower path cost
                        father[succesor]=(temp,direc)
                    flag=1
                    break
            if (succesor not in checked) and flag==0: #if flag==0 that means the node was not found into the priority queue
                pq.push(succesor,cost_2+cost[0]) #cost_2+cost[0] is the node's cumulative cost
                father[succesor]=(temp,direc)
            flag=0 
    #The code from now on is make the path with pacman actions (same as before)
    dest=temp
    path=[]
    while dest!=problem.getStartState(): 
        path.insert(0,father[dest][1])
        dest=father[dest][0]
    return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#This function is the almost the same as UFS, it uses the same flag system to check for the priorities in the queue (the different lines in the code are commented)
def aStarSearch(problem, heuristic=nullHeuristic):
    pq = PriorityQueue()
    checked=set()
    father={}
    pq.push(problem.getStartState(),0)
    flag=0
    cumul_cost={problem.getStartState():0} #cumul_cost holds the cost of the cheapest path from start to n currently known.
    while(not pq.isEmpty()):
        cost=pq.heap[0] 
        temp=pq.pop() 
        checked.add(temp)
        if problem.isGoalState(temp):
            break
        succ=problem.getSuccessors(temp)
        for succesor,direc,cost_2 in succ:
            for pri,count,item  in pq.heap:
                #we check if the succesor already exists in the heap
                if succesor==item:
                    if(cumul_cost[succesor] > cumul_cost[temp]+cost_2): #if it does exist and has more expensive path we update his cumulative cost and his parent based on the current node
                        cumul_cost[succesor] = cumul_cost[temp]+cost_2 #we also change his cumulative cost because we found a cheaper path
                        pq.update(succesor,cumul_cost[succesor]+heuristic(succesor,problem)) #we also update its priority in the priority queue based os its new cumulative cost
                        father[succesor]=(temp,direc) #we also update his parent because the current father (which is temp) offers a cheaper path
                    flag=1
                    break
            #if it is not visited and it doesnt exist in the priority queue then we push it in with priority his cumulative cost+heuristic cost
            if (succesor not in checked) and flag==0:
                cumul_cost[succesor] = cumul_cost[temp]+cost_2
                pq.push(succesor,cumul_cost[temp]+cost_2+heuristic(succesor,problem))
                father[succesor]=(temp,direc)
            flag=0 
    dest=temp
    path=[]
    while dest!=problem.getStartState(): 
        path.insert(0,father[dest][1])
        dest=father[dest][0]
    return path
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
