import heapq
from copy import deepcopy
visited = set()

# Node class definition
class Node():
    def __init__(self, stacks, sz):
        self.parent = None
        self.state = deepcopy(stacks)
        self.path_cost = 0
        self.heuristic_cost = 0
        self.action = None
        self.children = []
        self.stacksize = sz
        self.key = ""
    def __lt__(self, other):
        return self.path_cost < other.path_cost

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
    def possibleChildren(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if len(self.state[i]) > 0:
                    if i != j and len(self.state[j]) < self.stacksize:
                        auxNode = Node(self.state, self.stacksize)
                        auxNode.action = (i,j)
                        auxNode.parent = self
                        auxNode.applyAction()
                        auxNode.setKey()
                        self.children.append(auxNode)

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
# tkes a node and a list to apped the path recursively
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
    visited = []
    min_heap = []
    count = 0
    max_height = int(input())
    stacks = list(map(parse,input().split(';')))
    goal = list(map(parse,input().split(';')))

    initial = Node(stacks, max_height)
    goalNode = Node(goal, max_height)

    if not checkValid(goal, max_height):
        print('No solution found')
        exit()
    if not checkValid(initial.state, max_height):
        print('No solution found')
        exit()
    # Add initial to frontier to start
    heapq.heappush(min_heap, initial)
    while(True):
        # If there are no elements in thequeue then there is n solution
        if(len(min_heap) == 0):
            print("No solution found")
            exit()
        # Take out the first/smallest element to evaluate if it is our goal
        current = heapq.heappop(min_heap)
        count += 1
        visited.append(current)
        # Expand the node
        current.possibleChildren()
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
