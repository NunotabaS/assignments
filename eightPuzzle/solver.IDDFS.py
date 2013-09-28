#!/usr/bin/env python
def prettyPrint(state):
    print "___________"
    l = [(state[3 * n],state[3 * n+1],state[3 * n+2]) for n in xrange(0,3)]
    for elem in l:
        print " " + str(elem[0]) + " | " + str(elem[1]) + " | " + str(elem[2])
    print "-----------"

def swap(l, i, j):
    r = l[:]
    r[i], r[j] = r[j], r[i]
    return r

def getSuccessors(state):
    swappable = []
    index = state.index(0)
    if index % 3 == 0:
        swappable.append(index+1)
    elif index % 3 == 1:
        swappable.append(index+1)
        swappable.append(index-1)
    else:
        swappable.append(index-1)
    if index - 3 >= 0:
        swappable.append(index-3)
    if index + 3 < 9:
        swappable.append(index+3)
    return [swap(state, index, item) for item in swappable]

def dfs(state, goal, trace, depth):
    if depth <= 0:
        return (False, None)
    trace.append(tuple(state))
    successors = getSuccessors(state)
    for successor in successors:
        tup = tuple(successor)
        if tup == goal:
           print "Found solution in %i moves" % (len(trace) + 1)
           trace.append(successor)
           return (True, trace)
        if tup in trace:
           continue #dont explore already explored ones
        result = dfs(successor, goal, trace[:], depth-1)
        if result[0]:
           return result
    return (False, None)

def eightPuzzleDemo(startState):
    depth = 0
    goal = (0,1,2,3,4,5,6,7,8)
    while(1):
        print "Working in depth %i" % depth
        result = dfs(startState, goal, [], depth)
        if result[0]:
            return result[1]
        else:
            depth += 1

def createStepPuzzle(steps = 5):
    import random
    puzzle = [0,1,2,3,4,5,6,7,8]
    while(steps > 0):
        succ = getSuccessors(puzzle)
        idx = random.randint(0,len(succ) - 1)
        puzzle = succ[idx]
        steps -= 1
    return puzzle

def testTrivial ():
    result = eightPuzzleDemo([1,0,2,3,4,5,6,7,8])
    for step in result:
        prettyPrint(step)

def testRandPuzzle ():
    puzzle = createStepPuzzle()
    print "Initial State:"
    prettyPrint(puzzle)
    print "Trace:"
    result = eightPuzzleDemo(puzzle)
    for step in result:
        prettyPrint(step)

testTrivial()
testRandPuzzle()

print "Solving Hard Puzzle:"
result = eightPuzzleDemo([7,2,4,5,0,6,8,3,1])
counter = 0
for step in result:
    print "Step %i:" % counter
    prettyPrint(step)
    counter += 1
exit()
