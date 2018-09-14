def parse(a):
    a = a.strip().lstrip('(').rstrip(')').split(',')
    a = list(filter(None, a))
    return a

max_height = int(input())
stacks = list(map(parse,input().split(';')))
goal = list(map(parse,input().split(';')))
print(max_height)
print(stacks)
print(goal)
