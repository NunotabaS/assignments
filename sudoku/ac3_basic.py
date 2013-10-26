import collections

def generate_domain(puzzle):
    """Generate the domain maintaining binary constraints"""
    domain = dict()
    for x in xrange(0,9):
        for y in xrange(0,9):
            if puzzle[x][y] != 0:
                domain[(x,y)] = [puzzle[x][y]]
            else:
                domain[(x,y)] = [1,2,3,4,5,6,7,8,9]
    return domain
    
def neighbors(point):
    """A generator that creates neighbors of some point"""
    for x in xrange(0,9):
        for y in xrange(0,9):
            if x == point[0] and y == point[1]:
                continue;
            if x == point[0] or y == point[1]:
                yield (x,y)  #in the same row or col
            elif int(x/3) == int(point[0]/3) and int(y/3) == int(point[1]/3):
                yield (x,y)  #in the same block 

def revise_domain(domains, p1, p2):
    """Revise the domains using the constraints"""
    revised = False
    domx = domains[p1]
    domy = domains[p2]
    for valx in domx:
        if reduce(lambda red, y: red or y != valx, domy, False):
            continue; #found valid y in domain
        domains[p1].remove(valx)
        revised = True
    return revised

def ac3(domains):
    """Runner for AC3"""
    arcs = collections.deque([(y,n) for y in domains for n in neighbors(y)])
    while True:
        if len(arcs) == 0:
            break
        p = arcs.pop()
        if revise_domain(domains, p[0], p[1]) :
            if len(domains[p[0]]) == 0:
                return None
            for n in neighbors(p[0]):
                if n != p[1]:
                    arcs.appendleft((p[0], n)) # arc 1
                    arcs.appendleft((n, p[0])) # arc 2
    return domains

def run(puzzle):
    """Wrapper to make everything work"""
    domain = generate_domain(puzzle)
    solved = puzzle[:]
    simplified = ac3(domain)
    for pp in simplified:
        if len(simplified[pp]) == 1:
            solved[pp[0]][pp[1]] = simplified[pp][0]
        else:
            solved[pp[0]][pp[1]] = simplified[pp]
    return solved
