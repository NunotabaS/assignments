from Tkinter import *
from robotUtilities import read
import sys

def drawboard(canvas, board):
    (start, end, polygons)=board
    drawPoint(canvas, start, "red")
    drawPoint(canvas, end, "red")
    for polygon in polygons:
        for i in range(len(polygon)):
            drawLine(canvas, polygon[i], polygon[(i+1)%len(polygon)], "blue") 
def drawPath(canvas, path):
    realpath = [(path[x], path[x+1]) for x in xrange(0, len(path) - 1)]
    print realpath
    for line in realpath:
        drawLine(canvas, line[0], line[1], "red")

def drawPoint(canvas, point, col):
    (x,y)=point
    canvas.create_oval(((x+5.0)/10.0)*600-2,((y+5.0)/10.0)*600-2,((x+5.0)/10.0)*600+2,((y+5.0)/10.0)*600+2,fill=col)

def drawLine(canvas, point1, point2, col):
    (x1,y1)=point1
    (x2,y2)=point2
    drawPoint(canvas, point1, col)
    drawPoint(canvas, point2, col)
    canvas.create_line(((x1+5.0)/10.0)*600,((y1+5.0)/10.0)*600,((x2+5.0)/10.0)*600,((y2+5.0)/10.0)*600,fill=col)

def testWith (algorithm, dataset):
    if algorithm in ["BFS","DFS","ASTAR"]:
        alg = __import__("pathfind_" + algorithm)
        data = read(dataset)
        master = Tk()
        w = Canvas(master, width=600, height=600)
        drawboard(w, data)
        path = alg.callAlgorithm(data)
        print path
        if not path == None:
            drawPath(w, path)
        w.pack()
        mainloop()
    else:
        print "No Algorithm Given!"
        master = Tk()
        w = Canvas(master, width=600, height=600)
        drawboard(w, read(dataset))
        w.pack()
        mainloop()

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "usage: %s [search type=DFS, BFS, ASTAR] [map]" % sys.argv[0]
        exit(-1)
    data = sys.argv[2] if len(sys.argv) > 2 else "big_triangles"
    testWith(sys.argv[1], data);
