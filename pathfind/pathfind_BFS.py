from robotUtilities import *
from collections import deque

def getParent(point, polytracker):
    """wrapper to safely get the parent polygon of a point"""
    try:
        return polytracker[point]
    except KeyError:
        return None

def getVertices(polygons):
    """gets all vertices excluding the bounding box"""
    return [point for poly in polygons for point in poly if not poly == ((-5,-5),(5, -5),(5, 5),(-5, 5)) ]

def getVerticesSE(polygons, start, end):
    """gets all vertices including the start and end"""
    v = getVertices(polygons)
    if not start in v:
        v.append(start)
    if not end in v:
        v.append(end)
    return v

def getLines(polygons):
    """gets all the edges of every polygon thats not the bound box"""
    return [(poly[p],poly[(p+1)% len(poly)]) for poly in polygons for p in xrange(0,len(poly)) if not poly == ((-5,-5),(5, -5),(5, 5),(-5, 5)) ]

def createPolyTracker(polygons):
    """initialize the reverse checklist for a vertex's parent polygon"""
    polylist = {}
    for polygon in polygons:
        if polygon == ((-5,-5),(5, -5),(5, 5),(-5, 5)):
            continue;
        for point in polygon:
            polylist[point] = polygon
    return polylist

def genSuccessors(vertex, vertices, lines, polytracker):
    """returns all possible successors of the current vertex"""
    successors = []
    parentPolygon = getParent(vertex, polytracker)
    if parentPolygon:
        plen = len(parentPolygon)
        vindex = parentPolygon.index(vertex)
        left = parentPolygon[(plen + vindex - 1) % plen]
        right = parentPolygon[(plen + vindex + 1) % plen]
    
    for v in vertices:
        if v == vertex:
            continue;
        if not pathIntersectsAnyLines(vertex, v, lines):
            if parentPolygon:
                if v in parentPolygon and (not v == left) and (not v == right):
                    continue;
            successors.append(v)
    return successors
    
def bfs(input_data):
    """does the dfs search"""
    vertices = getVerticesSE(input_data[2], input_data[0], input_data[1])
    lines = getLines(input_data[2])
    start = input_data[0]
    end = input_data[1]
    polytracker = createPolyTracker(input_data[2])
    
    queue = deque()
    visited = set()
    
    queue.appendleft(start)
    reversePtr = dict()
    while(1):
        node = queue.pop()
        print "Visiting %s" % (node,)
        if node == end or distance(node, end) < EPSILON:
            #build the backtracking path
            print "Found Path!"
            path = []
            cn = node
            while ( cn != start ):
                path.append(cn)
                cn = reversePtr[cn]
            path.append(cn)
            path.reverse()
            return tuple(path)
        
        for n in genSuccessors(node, vertices, lines, polytracker):
            if not (n in visited):
                visited.add(n)
                reversePtr[n] = node
                queue.appendleft(n)
        if len(queue) == 0:
            return None

def callAlgorithm (dataset):
    return bfs(dataset)

