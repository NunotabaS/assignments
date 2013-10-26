import ac3_basic

def check_block_constraint(domain, debug = False):
    """Remove all constraining variables (see problem 3's description of what is done here)"""
    if domain == None:
        return False
    restrain = False
    #check the row constraints
    for i in xrange(0,9):
        rowlist = [1,2,3,4,5,6,7,8,9]
        for item in rowlist:
            canPlace = []
            for j in xrange(0,9):
                if item in domain[(i,j)]:
                    canPlace.append((i,j))
            if len(canPlace) == 1 and len(domain[canPlace[0]]) > 1:
                domain[canPlace[0]] = [item]
                if debug:
                    print "Restrain %s to %d due to row" % (canPlace[0], item)
                restrain = True
    #check the col constraints
    for j in xrange(0,9):
        collist = [1,2,3,4,5,6,7,8,9]
        for item in collist:
            canPlace = []
            for i in xrange(0,9):
                if item in domain[(i,j)]:
                    canPlace.append((i,j))
            if len(canPlace) == 1 and len(domain[canPlace[0]]) > 1:
                
                domain[canPlace[0]] = [item]
                if debug:
                    print "Restrain %s to %d due to col" % (canPlace[0], item)
                restrain = True
    #check block constraints
    for i in xrange(0,9):
        blocklist = [1,2,3,4,5,6,7,8,9]
        for item in blocklist:
            canPlace = []
            for j in xrange(0,9):
                indexX = 3 * int(i / 3) + int(j / 3)
                indexY = 3 * int(i % 3) + int(j % 3)
                if item in domain[(indexX, indexY)]:
                    canPlace.append((indexX, indexY));
            if len(canPlace) == 1 and len(domain[canPlace[0]]) > 1:
                domain[canPlace[0]] = [item]
                if debug:
                    print "Restrain %s to %d due to block" % (canPlace[0], item)
                restrain = True
    return restrain

def domain_to_puzzle(dom, puz):
    if dom == None:
        return None
    for pp in dom:
        if len(dom[pp]) == 1:
            puz[pp[0]][pp[1]] = dom[pp][0]
        else:
            puz[pp[0]][pp[1]] = dom[pp]
    return puz
def solve(domain, debug = False):
    simplified = ac3_basic.ac3(domain)
    while(check_block_constraint(simplified, debug)):
        if debug:
            pretty_print(domain_to_puzzle(simplified, solved), True) # debugging
        simplified = ac3_basic.ac3(simplified)
    return simplified
    
def run(puzzle, debug = False):
    if debug:
        from sudoku_solver import pretty_print
    domain = ac3_basic.generate_domain(puzzle)
    solution = solve(domain, debug)
    return domain_to_puzzle(solution,puzzle[:])
    
