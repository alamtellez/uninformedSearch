'''
Input:
2
(A); (B); (C)
(A, C); X; X

7
(A, C, D); (T, Y); ()
(C); (D, Y); (A, T)
Output:
3
(2, 0)
'''
import heapq
from copy import deepcopy
import random



# Node class definition
class Node():
    def __init__(self, stacks, sz):
        self.parent = None
        self.state = deepcopy(stacks)
        self.path_cost = 0
        self.heuristic_cost = 0
        self.f_cost = 0
        self.action = None
        self.children = []
        self.stacksize = sz
        self.key = ""
    def __lt__(self, other):
        return self.f_cost < other.f_cost

    # This method recieves a node with its parent state and applies the action given
    def applyAction(self):
        move = self.action
        item = self.state[move[0]].pop()
        self.state[move[1]].append(item)
        self.path_cost = self.parent.path_cost + 1 + abs(move[1] - move[0])

    # Optional key for visited if needed
    def setKey(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                self.key += str(j)
            self.key += ";"

    # Function that expands the node to the possible children
    def possibleChildren(self, goal):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if len(self.state[i]) > 0:
                    if i != j and len(self.state[j]) < self.stacksize:
                        auxNode = Node(self.state, self.stacksize)
                        auxNode.action = (i,j)
                        auxNode.parent = self
                        auxNode.applyAction()
                        auxNode.setKey()
                        # To use a consistent or inconsistent heuristic
                        # just comment one of the lines below
                        # auxNode.calcInconsistentHeuristic()
                        auxNode.calcHeuristicCost(goal)
                        self.children.append(auxNode)

    # A consistent heuristic that increases whenever a container
    # is not in the goal state
    def calcHeuristicCost(self, goal):
        for i in range(len(goal.state)):
            if(self.state[i] != list() and goal.state[i] != list()):
                for j in range(min(len(goal.state[i]), len(self.state[i]))):
                    if(self.state[i][j] != goal.state[i][j]):
                        self.heuristic_cost += 1
        self.f_cost = self.heuristic_cost + self.path_cost

    # This is an inconsistent heuristic that will most likely
    # make A Star fail and not find an optimal solution
    def calcInconsistentHeuristic(self):
        self.heuristic_cost = random.randint(0, 100)
        self.f_cost = self.heuristic_cost + self.path_cost

# Parsing the input into:
#   limit height of the problem
#   the initial goal stacks
#   the goal status using X's to ignore
def parse(a):
    a = a.strip().lstrip('(').rstrip(')').split(',')
    a = list(filter(None, a))
    a = list(map(lambda x: x.lstrip(), a))
    return a

# Check if the stack has a valid height
def checkValid(stacks,max_height):
    for stack in stacks:
        if len(stack) > max_height:
            return False
    return True
# takes a node and a list to apped the path recursively
def print_action(node, actions):
    if (node.parent == None):
        return
    print_action(node.parent, actions)
    actions.append(node.action)

# Compare every stack of given goal and the current state to see if it is the goal
def is_goal(node, goal):
    for i in range(len(goal.state)):
        if(goal.state[i] != ['X']):
            if(goal.state[i] != node.state[i]):
                return False
    return True


if __name__ == "__main__":
    min_heap = []
    visited = set()
    max_height = int(input())
    stacks = list(map(parse,input().split(';')))
    goal = list(map(parse,input().split(';')))
    count = 0
    initial = Node(stacks, max_height)
    goalNode = Node(goal, max_height)

    if not checkValid(goal, max_height):
        print('No solution found')
        exit()
    if not checkValid(initial.state, max_height):
        print('No solution found')
        exit()

    heapq.heappush(min_heap, initial)
    while(True):
        # If there are no elements in thequeue then there is n solution
        if(len(min_heap) == 0):
            print("No solution found")
            exit()
        # Take out the first/smallest element to evaluate if it is our goal
        current = heapq.heappop(min_heap)
        count += 1
        if current.key not in visited:
            visited.add(current.key)
            # Expand the node
            current.possibleChildren(goalNode)
            # Check if the node is our goal
            if is_goal(current, goalNode):
                print(current.path_cost)
                path = []
                print_action(current, path)
                print("; ".join(map(str, path)))
                #print(count)
                break
            # If node isnt goal, expand it nd continue searching
            for i in range(len(current.children)):
                heapq.heappush(min_heap, current.children[i])
