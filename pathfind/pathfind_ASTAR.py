from robotUtilities import *
import heapq

def xcontains(l, item):
    return item in [v[1] for v in l]

def heuristic(vertex, end):
    dist = distance(vertex, end)
    return 0 if dist < EPSILON else dist 

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
    return [(poly[p],poly[(p+1) % len(poly)]) for poly in polygons for p in xrange(0,len(poly)) if not poly == ((-5,-5),(5, -5),(5, 5),(-5, 5)) ]

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
    
def astar(input_data):
    vertices = getVerticesSE(input_data[2], input_data[0], input_data[1])
    lines = getLines(input_data[2])
    print len(lines)
    start = input_data[0]
    end = input_data[1]
    polytracker = createPolyTracker(input_data[2])
    
    pq = []
    visited = set()
    
    # init the best score mappings
    f = {}
    g = {}
    
    # init the scores for start
    g[start] = 0
    f[start] = g[start] + heuristic(start, end)
    
    # reverse pointers to seek back our tracks
    reverse = {}
    
    # add in the first item
    heapq.heappush(pq, (f[start], start))
    while(1):
        if len(pq) <= 0:
            break;
        current = heapq.heappop(pq)
        if current[1] == end or distance(current[1], end) < EPSILON:
            path = []
            cn = current[1]
            while ( cn != start ):
                path.append(cn)
                cn = reverse[cn]
            path.append(cn)
            path.reverse()
            return path

        visited.add(current[1])
        print "Visiting %s" % (current[1],)
            
        for n in genSuccessors(current[1], vertices, lines, polytracker):
            t_g = g[current[1]] + distance(current[1], n)
            t_f = t_g + heuristic(n, end)
            if n in visited and t_f >= f[n]:
                continue; # worse
            
            if not xcontains(pq, n) or t_f < f[n]:
                reverse[n] = current[1]
                g[n] = t_g
                f[n] = t_f
                if not xcontains(pq, n):
                    heapq.heappush(pq, (f[n], n))
    return None

def callAlgorithm (dataset):
    return astar(dataset)

