def read(filename):
    tate = []
    with open(filename, 'r') as f:
        for line in f:
            yoko = []
            cells = list(line.strip())
            for cell in cells:
                if cell == "*":
                    yoko.append(0)
                else:
                    yoko.append(int(cell))
            if len(yoko) != 9:
                raise Exception("Not a valid sudoku input")
            tate.append(yoko)
    if len(tate) != 9:
        raise Exception("Not a valid sudoku input")
    return tate
