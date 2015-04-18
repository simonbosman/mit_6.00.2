# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#
# The nodes of the weighted Digraph are the buildings of the MIT campus
# The edges are the paths between de MIT buildings 

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become for d in self.edges[k]: an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    g = WeightedDigraph()
    print "Loading map from file..."
   
    #First add all the nodes to the graph
    with open(mapFilename) as f:
        for line in f:
            entry = line.split()  
            n1 = Node(entry[0])
            n2 = Node(entry[1])
            try:
                g.addNode(n1)
                g.addNode(n2)
            except ValueError:
                continue
    #Second add al the edges
    with open(mapFilename) as f:
        for line in f:
            entry = line.split()  
            n1 = Node(entry[0])
            n2 = Node(entry[1])
            edge = WeightedEdge(n1, n2, entry[2], entry[3])
            try:
                g.addEdge(edge)
            except ValueError:
                continue 
    return g

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#
# Minimize the path within the constraints of total distance and the total distance outdoors 


def findValidPaths(graph, start, end, maxDistOutdoors=1.0, s=[]):
    initPath = [start]
    foundPaths = []
    s.insert(0, initPath)
    while len(s) != 0:
        tmpPath = s.pop(0)
        lastNode = tmpPath[len(tmpPath) -1]
        
        #Found a path, check if its within constraints maxDistOutdoors
        if lastNode == end:
            #Found a path, check if its within the constraint
            totalDist = 0
            for idx in range(len(tmpPath)-1):
                #check every edge in node
                for d in graph.edges[Node(tmpPath[idx])]:
                    #if destination edge is next element in path
                    if d[0] == Node(tmpPath[idx+1]):
                        totalDist += d[1][1]
            #check for constraint
            if not totalDist > maxDistOutdoors:
                foundPaths.append([node.getName() for node in tmpPath])
        
        #add children of the node on the stack, avoid loops
        for child in graph.childrenOf(lastNode):
            if child not in tmpPath:
                newPath = tmpPath + [child]
                s.insert(0, newPath)
       
    if len(foundPaths) == 0:
        raise ValueError           
    return foundPaths
    
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #Get all valid paths with constrain maxDistOutDoors
    validPaths = findValidPaths(digraph, Node(start), Node(end), maxDistOutdoors)
    bestPath = None
    bestTotalDist = 0 
         
    for path in validPaths:
        totalDist = 0
        for idx in range(len(path)-1):
            #check every edge in node
            for d in digraph.edges[Node(path[idx])]:
                #if destination edge is next element in path
                if d[0] == Node(path[idx+1]):
                      totalDist += d[1][0]
        if totalDist <= bestTotalDist or bestTotalDist == 0:
            bestTotalDist = totalDist
            bestPath = path
   
    #check for constraint
    if bestTotalDist > maxTotalDist:
        raise ValueError
            
    if bestPath == None:
        raise ValueError
    return bestPath
 
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def getTotalDistances(graph, path):
    totalDist = 0
    totalOutdoors = 0
    
    for idx in range(len(path)-1):
        #check every edge in node
        for d in graph.edges[Node(path[idx])]:
            #if destination edge is next element in path
            if d[0] == Node(path[idx+1]):
                totalDist += d[1][0]
                totalOutdoors += d[1][1]
    return totalDist, totalOutdoors
   

def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    start = Node(start)
    end = Node(end)
    initPath = [start]
    s = []
    s.insert(0, initPath)
    bestTotal = None
    bestPath = None
    while len(s) != 0:
        tmpPath = s.pop(0)
        lastNode = tmpPath[len(tmpPath) -1]
        
        #Found a path, check if it is the best path so far
        if lastNode == end:
            distances = getTotalDistances(digraph, tmpPath)
            if bestTotal == None or distances[0] <= bestTotal:
                bestTotal = distances[0]
                bestPath = tmpPath
        
        #add children of the node on the stack, avoid loops
        for child in digraph.childrenOf(lastNode):
            if child not in tmpPath:
                #Check for totalDistance and totalDistOutdoors
                newPath = tmpPath + [child]
                distances = getTotalDistances(digraph, newPath)
                if distances[1] <= float(maxDistOutdoors):
                    if distances[0] <= float(maxTotalDist):
                        s.insert(0, newPath)
       
    if bestPath == None:
        raise ValueError
    else:
        return [node.getName() for node in bestPath]
            
# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
#     Test cases
    mitMap = load_map("/home/simon/Source/mit_600.2/ProblemSet5/mit_map.txt")
    #print isinstance(mitMap, Digraph)
    #print isinstance(mitMap, WeightedDigraph)
#    print 'nodes', mitMap.nodes
#   print 'edges', mitMap.edges


    LARGE_DIST = 1000000

#     Test case 1
#    print "---------------"
#    print "Test case 1:"
#    print "Find the shortest-path from Building 32 to 56"
#    expectedPath1 = ['32', '56']
#    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#    print "Expected: ", expectedPath1
#    print "Brute-force: ", brutePath1
#     print "DFS: ", dfsPath1
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#    print "---------------"
#    print "Test case 2:"
    #print "Find the shortest-path from Building 32 to 56 without going outdoors"
    #expectedPath2 = ['32', '36', '26', '16', '56']
    #brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    #print "Expected: ", expectedPath2
    #print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    #print "---------------"
    #print "Test case 3:"
    #print "Find the shortest-path from Building 2 to 9"
    ##expectedPath3 = ['2', '3', '7', '9']
    #brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    #print "Expected: ", expectedPath3
    #print "Brute-force: ", brutePath3
#    print mitMap
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    #print "---------------"
    #print "Test case 7:"
    #print "Find the shortest-path from Building 8 to 50 without going outdoors"
    #bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
    #try:
    #    bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    #except ValueError:
    #    bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
    #print "Expected: No such path! Should throw a value error."
    #print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    #try:
    #    bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    #except ValueError:
    #    bruteRaisedErr = 'Yes'
    #
    try:
         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
         dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

g = WeightedDigraph()
g.addNode(Node(1))
g.addNode(Node(2))
g.addNode(Node(3))
g.addNode(Node(4))
#g.addNode(Node(5))

e1 = WeightedEdge(Node(1), Node(2), 10.0, 5.0)
e2 = WeightedEdge(Node(1), Node(4), 5.0, 1.0)
e3 = WeightedEdge(Node(2), Node(3), 8.0, 5.0)
e4 = WeightedEdge(Node(4), Node(3), 8.0, 5.0)
#e5 = WeightedEdge(Node(4), Node(3), 5.0, 1.0)
#e6 = WeightedEdge(Node(4), Node(5), 20.0, 1.0)

g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
g.addEdge(e4)
#g.addEdge(e5)
#g.addEdge(e6)

#print bruteForceSearch(g, "4", "5", 20, 1)
#print bruteForceSearch(g, "1", "5", 35, 9)
#print bruteForceSearch(g, "1", "5", 35, 8)
#print bruteForceSearch(g, "4", "5", 21, 11)
#print bruteForceSearch(g, "4", "5", 21, 1)
#print bruteForceSearch(g, "4", "5", 19, 1)
#print bruteForceSearch(g, "3", "2", 100, 100)
#print bruteForceSearch(g, "4", "5", 8, 2)
#print bruteForceSearch(g, "1", "3", 15, 15)
#print g
#print directedDFS(g, "1", "3", 18, 18)
#print directedDFS(g, "1", "3", 15, 15)