# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from util import heappush, heappop
import time

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
      """
      Returns the start state for the search problem
      """
      util.raiseNotDefined()

    def isGoalState(self, state):
      """
      state: Search state

      Returns True if and only if the state is a valid goal state
      """
      util.raiseNotDefined()

    def getSuccessors(self, state):
      """
      state: Search state

      For a given state, this should return a list of triples,
      (successor, action, stepCost), where 'successor' is a
      successor to the current state, 'action' is the action
      required to get there, and 'stepCost' is the incremental
      cost of expanding to that successor
      """
      util.raiseNotDefined()

    def getCostOfActions(self, actions):
      """
      actions: A list of actions to take

      This method returns the total cost of a particular sequence of actions.  The sequence must
      be composed of legal moves
      """
      util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure that you implement the graph search version of DFS,
    which avoids expanding any already visited states. 
    Otherwise your implementation may run infinitely!
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    problem.getStartState() -> (x, y)
    problem.isGoalState() -> True/False
    problem.getSuccessors(state) -> [((x,y), 'Direction', cost), ((x,y), 'Direction', cost)]
    """
    # Call stack from util.py and push start state with the path from start state
    stack = util.Stack()
    stack.push((problem.getStartState(),[]))

    # create a closed set for visited spaces
    visited_spaces = set()

    # iterates while stack contains data
    while not stack.isEmpty():
       # pop state and add to visited states
       # state = ((x, y), ['Action 1', 'Action 2', ...])
       state, path = stack.pop()
       # Adds (x,y) coordinates to visited set
       visited_spaces.add(state)
       # result assumes list of actions
       result = path
       # Goal state? If so, returns list of actions
       if problem.isGoalState(state):
          return result
       # gets (x,y) neighbors
       neighbor_states = problem.getSuccessors(state)
       # checks if there are successors
       if neighbor_states: 
          # iterates through the coordinate position of neighbor states
          for pos in neighbor_states:
             # if coordinates not visited before pushes ((x,y), [list of actions + new action for the new state])
             if pos[0] not in visited_spaces:
                stack.push((pos[0], result + [pos[1]]))
    return []
    

def breadthFirstSearch(problem):
    # Call queue from util.py and push start state with the path from start state
    queue = util.Queue()
    # .push() uses .insert(0, item)
    queue.push((problem.getStartState(),[]))

    # create a closed set for visited spaces
    visited_spaces = set()

    # iterates while queue contains data
    while not queue.isEmpty():
       # pop state and add to visited states
       # state = ((x, y), ['Action 1', 'Action 2', ...])
       state, path = queue.pop()
       # Adds (x,y) coordinates to visited set
       visited_spaces.add(state)
       # result assumes list of actions
       result = path
       # Goal state? If so, returns list of actions
       if problem.isGoalState(state):
          return result
       # gets (x,y) neighbors
       neighbor_states = problem.getSuccessors(state)
       # checks if there are successors
       if neighbor_states: 
          # iterates through the coordinate position of neighbor states
          for pos in neighbor_states:
             # if coordinates not visited before pushes ((x,y), [list of actions + new action for the new state])
             if pos[0] not in visited_spaces:
                visited_spaces.add(pos[0])
                queue.push((pos[0], result + [pos[1]]))
    return []



def uniformCostSearch(problem):
    """
    YOUR CODE HERE
    """
    #  Call priority queue from util.py and push start state with the path from start state
    pQueue = util.PriorityQueue()
    
    # pushes start state, [] -> action, 0 -> initial cost, 0 -> priority value for the p queue
    pQueue.push((problem.getStartState(), [], 0), 0)
    
    # using a dictionary instead of a set() to avoid visiting states with a higher cost
    visited_spaces = {}
    
    # iterates while pQueue contains data
    while not pQueue.isEmpty():
       # pop state with lowest cost
       state, result, cost = pQueue.pop()
       
       # check if state was already visited and if the cost is less than or qual to the cost
       if state in visited_spaces and visited_spaces[state] <= cost:
          continue
       # add the current state to visited with the lwoest cost found
       visited_spaces[state] = cost
       # Goal state? If so, returns list of actions
       if problem.isGoalState(state):
          return result
       # gets (x,y) neighbors
       neighbors = problem.getSuccessors(state)
       # checks if there are successors 
       if neighbors:
          # iterates through the coordinate position of neighbor states
          for pos in neighbors:
             new_cost = cost + pos[2]
             # updates pQueue if neighbor has not been visited or a cheaper path is found
             if pos[0] not in visited_spaces or visited_spaces[pos[0]] > new_cost:
                pQueue.update((pos[0], result + [pos[1]], new_cost), new_cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    YOUR CODE HERE
    """
    pQueue = util.PriorityQueue()
    
    # pushes start state, [] -> action, 0 -> initial cost, 0 -> priority value for the p queue
    pQueue.push((problem.getStartState(), [], 0), 0)
    
    # using a dictionary instead of a set() to avoid visiting states with a higher cost
    visited_spaces = {}
    
    # iterates while pQueue contains data
    while not pQueue.isEmpty():
       # pop state with lowest cost
       state, result, cost = pQueue.pop()
       
       # check if state was already visited and if the cost is less than or qual to the cost
       if state in visited_spaces and visited_spaces[state] <= cost:
          continue
       # add the current state to visited with the lwoest cost found
       visited_spaces[state] = cost
       # Goal state? If so, returns list of actions
       if problem.isGoalState(state):
          return result
       # gets (x,y) neighbors
       neighbors = problem.getSuccessors(state)
       # checks if there are successors 
       if neighbors:
          # iterates through the coordinate position of neighbor states
          for pos in neighbors:
             new_cost = cost + pos[2]
             # updates pQueue if neighbor has not been visited or a cheaper path is found with heuristic value
             if pos[0] not in visited_spaces or visited_spaces[pos[0]] > new_cost:
                pQueue.update((pos[0], result + [pos[1]], new_cost), new_cost + heuristic(pos[0], problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
