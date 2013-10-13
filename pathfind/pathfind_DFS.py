from robotUtilities import *
from collections import deque

def getParent(point, polytracker):
    try:
        return polytracker[point]
    except KeyError:
        return None

def getVertices(polygons):
    return [point for poly in polygons for point in poly if not poly == ((-5,-5),(5, -5),(5, 5),(-5, 5)) ]

def getVerticesSE(polygons, start, end):
    v = getVertices(polygons)
    if not start in v:
        v.append(start)
    if not end in v:
        v.append(end)
    return v

def getLines(polygons):
    return [(poly[p % len(poly)],poly[(p+1)% len(poly)]) for poly in polygons for p in xrange(0,len(poly)) if not poly == ((-5,-5),(5, -5),(5, 5),(-5, 5)) ]

def createPolyTracker(polygons):
    polylist = {}
    for polygon in polygons:
        if polygon == ((-5,-5),(5, -5),(5, 5),(-5, 5)):
            continue;
        for point in polygon:
            polylist[point] = polygon
    return polylist

def genSuccessors(vertex, vertices, lines, polytracker):
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
    
def dfs(input_data):
    vertices = getVerticesSE(input_data[2], input_data[0], input_data[1])
    lines = getLines(input_data[2])
    start = input_data[0]
    end = input_data[1]
    polytracker = createPolyTracker(input_data[2])
    
    stack = []
    visited = set()
    
    stack.append(start)
    while(1):
        node = stack[-1]
        print "Visiting %s" % (node,)
        if node == end or distance(node, end) < EPSILON:
            return tuple(stack)
        
        hasElem = False
        for n in genSuccessors(node, vertices, lines, polytracker):
            if not (n in visited):
                hasElem = True
                visited.add(n)
                stack.append(n)
                break;
        if not hasElem:
            if len(stack) == 0:
                return None
            stack.pop();

def callAlgorithm (dataset):
    return dfs(dataset)

