'''
Input:
2
(A); (B); (C)
(A, C); X; X
Output:
3
(2, 0)
'''
from copy import deepcopy
visited = set()

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

    def applyAction(self):
        move = self.action
        item = self.state[move[0]].pop()
        self.state[move[1]].append(item)
        self.path_cost = self.parent.path_cost + 1 + abs(move[1] - move[0])


    def setKey(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                self.key += str(j)
            self.key += ";"

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
                        print(auxNode.state[2][0])

    def calcHeuristic(self, goal):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if(self.state[i][j] != goal.state[i][j]):
                    heuristic_cost = 0



def parse(a):
    a = a.strip().lstrip('(').rstrip(')').split(',')
    a = list(filter(None, a))
    a = list(map(lambda x: x.lstrip(), a))
    return a

def checkValid(stacks,max_height):
    for stack in stacks:
        if len(stack) > max_height:
            return False
    return True


if __name__ == "__main__":
    max_height = int(input())
    stacks = list(map(parse,input().split(';')))
    goal = list(map(parse,input().split(';')))

    initial = Node(stacks, max_height)
    initial.possibleChildren()
    if not checkValid(goal, max_height):
        print('No solution found')
        exit()
    if not checkValid(initial.state, max_height):
        print('No solution found')
        exit()
