import sudoku_reader as reader
import sys

def pretty_print(puzzle, outall = False):
    if puzzle == None:
        print "no solution"
        return
    c = 0
    for line in puzzle:
        output = map(lambda x: ("\033[1;32m" + str(x) + "\033[m") if x != 0 and type(x) != list else "." if x == 0 else "M" if not outall else str(x), line)
        if c % 3 == 0:
            print "-------+-------+-------"
        print " %s %s %s | %s %s %s | %s %s %s " % tuple(output)
        c += 1
    print "-------+-------+-------"
    print "Use 'input' to get output matching the input"
    print "Use 'pretty-full' to not replace multichoice with M (debugging)"
    print "M in the display means multiple choices (did not completely solve)"
    
def format_print(puzzle):
    if puzzle == None:
        print "no solution"
        return
    for line in puzzle:
        output = map(lambda x: str(x) if x != 0 else "*", line)
        print "%s%s%s%s%s%s%s%s%s" % tuple(output)

def print_solution(solution, mode):
    if format == "pretty-full":
        pretty_print(solution, True)
    elif format == "pretty":
        pretty_print(solution)
    else:
        format_print(solution)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "usage: %s [solver_type=simple, advanced, full] [puzzle] [format=pretty, pretty-full, input]" % sys.argv[0]
        exit(-1)
    puzzle = sys.argv[2] if len(sys.argv) > 2 else "sudoku/dp_puzzle"
    format = sys.argv[3] if len(sys.argv) > 3 else "pretty"
    if sys.argv[1] in ["simple", "advanced", "full"]:
        if sys.argv[1] == "simple":
            import ac3_basic as solver
        elif sys.argv[1] == "advanced":
            import ac3_enhanced as solver
        elif sys.argv[1] == "full":
            import ac3_treesearch as solver
        else:
            raise Exception("Not implemented")
        print_solution(solver.run(reader.read(puzzle)), format)
    else:
        print_solution(solver.run(reader.read(puzzle)), format)
