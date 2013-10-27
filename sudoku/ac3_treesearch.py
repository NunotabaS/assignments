import ac3_enhanced
import copy

def is_solved(domain):
    if domain == None:
        return False
    for key in domain:
        if len(domain[key]) > 1:
            return False
    return True

def get_successors(domain):
    for key in domain:
        if len(domain[key]) > 1:
            for choice in domain[key]:
                yield (key, choice)

def puzzle_to_domain(puzzle):
    domain = dict()
    for i in xrange(0,9):
        for j in xrange(0,9):
            if(type(puzzle[i][j]) == list):
                domain[(i,j)] = puzzle[i][j]
            else:
                domain[(i,j)] = [puzzle[i][j]]
    return domain

def copy_dict(d):
    copy = dict()
    for key in d:
        copy[key] = list(d[key])
    return copy

def dfs(domain, trace, dontBother, depth):
    if depth <= 0:
        return None
    if domain == None:
        return None
    found = 0
    for successor in get_successors(domain):
        if successor in dontBother:
            continue
        ns = copy_dict(domain)
        ns[successor[0]] = [successor[1]]
        solved = ac3_enhanced.solve(ns)
        if solved == None:
            #print "Didn't find solution"
            dontBother.append(successor)
            continue
        else:
            #print "Solvable for %s,%d" % successor
            found += 1
            if is_solved(solved):
                return solved
            tr = trace[:]
            tr.append(successor)
            return dfs(solved, tr, dontBother, depth)
    return False
            

def run(puzzle, debug = False):
    domain = ac3_enhanced.ac3_basic.generate_domain(puzzle)
    base = ac3_enhanced.solve(domain)
    if base == None:
        return None
    if(is_solved(domain)):
        return ac3_enhanced.domain_to_puzzle(base, puzzle)
    # now we do IDDFS
    dontBother = [] # optimize so we dont check bad choices repeatedly
    depth = 1
    while 1:
        if debug:
            print "Iterating at depth %d" % depth
        sol = dfs(domain, [], dontBother, depth)
        if depth == 4:
           exit()
        if sol == None:
            depth += 1
        elif sol == False:
            return None
        else:
            return ac3_enhanced.domain_to_puzzle(sol, puzzle)
       
