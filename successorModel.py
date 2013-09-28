#!/usr/bin/env python
def prettyPrint(state):
    print "___________"
    l = [(state[3 * n],state[3 * n+1],state[3 * n+2]) for n in xrange(0,3)]
    for elem in l:
        print " " + str(elem[0]) + " | " + str(elem[1]) + " | " + str(elem[2])
    print "-----------"

def swap(l, i, j):
    l = l[:]
    l[i], l[j] = l[j], l[i]
    return l;

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
    if index - 3 > 0:
        swappable.append(index-3)
    if index + 3 < 9:
        swappable.append(index+3)
    return [swap(state, index, item) for item in swappable]

def eightPuzzleDemo(startState):
    successors = getSuccessors(startState)
    for successor in successors:
        prettyPrint(successor)

eightPuzzleDemo([7,2,4,5,0,6,8,3,1])
