'''Creating a Graph with an Eulerian Tour
'''
from random import randint

def edge(x, y):
    return (x, y) if x < y else (y, x)

def poprandom(nodes):
    x_i = randint(0, len(nodes) - 1)
    return nodes.pop(x_i)

def pickrandom(nodes):
    x_i = randint(0, len(nodes) - 1)
    return nodes[x_i]

def check_nodes(x, nodes, tour):
    for i, n in enumerate(nodes):
        t = edge(x, n)
        if t not in tour:
            tour.append(t)
            nodes.pop(i)
            return n
    return None

'''Assume that there are at least three input nodes given to create_tour'''
def create_tour(nodes):
    # there are lots of ways to do this
    # a boring solution could just connect
    # the first node with the second node
    # second with third... and the last with the
    # first
    tour = []
    l = len(nodes)
    for i in range(l):
        t = edge(nodes[i], nodes[(i+1) % l])
        tour.append(t)
    return tour

def create_tour_random(nodes):
    connected = []
    degree = {}
    unconnected = [n for n in nodes]
    tour = []

    # create a connected Graph
    # first, pick two random nodes for an edge
    x = poprandom(unconnected)
    y = poprandom(unconnected)
    connected.append(x)
    connected.append(y)
    tour.append(edge(x,y))
    degree[x] = 1
    degree[y] = 1

    # then, pick a random node from the unconnected list and create an edge to it
    while len(unconnected) > 0:
        x = pickrandom(connected)
        y = poprandom(unconnected)
        connected.append(y)
        tour.append(edge(x, y))
        degree[x] += 1
        degree[y] = 1

    '''now make sure each node has an even degree'''
    # have the problem of not adding a duplicate edge
    odd_nodes = [k for k, v in degree.items() if v%2 == 1]
    even_nodes = [k for k, v in degree.items() if v%2 == 0]
    # there will always be an even number of odd nodes
    # (hint: the sum of degrees of a graph is even)
    # so we can just connect pairs of unconnected edges
    while len(odd_nodes) > 0:
        x = poprandom(odd_nodes)
        cn = check_nodes(x, odd_nodes, tour)
        if cn is not None:
            even_nodes.append(x)
            even_nodes.append(cn)
        else:
            # if we get here, the node is already connected to all the odd_nodes
            # so we need to find an even one to connect to
            cn = check_nodes(x, even_nodes, tour)
            # cn cannot be None, and needs to be added to the odd_nodes list
            odd_nodes.append(cn)
            # but x is now an even node
            even_nodes.append(x)
    return tour

nodes = [1, 2, 4, 5, 8]
print create_tour(nodes)
print create_tour_random(nodes)
print
print ''' Find Eulerian Tour'''
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]
import random
# def find_eulerian_tour(graph):
#     # your code here
#     current_node = None
#     start = None
#     tour = []
#     explored = []
#     graph_ = graph[:]
#     while len(graph) > 0:
#         i = random.randint(0, len(graph)-1)
#         s, e = graph[i]
#         # if only one edge, check if e == start
#         if len(graph) == 1:
#             if e != start:
#                 # restart
#                 graph = graph_[:]
#                 i = random.randint(0, len(graph)-1)
#                 s, e = graph[i]
#                 while s in explored:
#                     i = random.randint(0, len(graph)-1)
#                     s, e = graph[i]
#                 start = s
#                 explored.append(start)
#
#         if not current_node:
#             current_node = e
#             graph.pop(i)
#             start = s
#             explored.append(start)
#             tour.append(s)
#             tour.append(e)
#         elif s == current_node:
#             current_node = e
#             graph.pop(i)
#             tour.append(e)
#
#     return tour

'''Solution from @zhh358'''
def find_eulerian_tour(graph):
    return helper([], graph)

def helper(result, restGraph):
    if len(restGraph) is 0:
        return result

    elif len(result) is 0:
        return helper([restGraph[0][0], restGraph[0][1]], restGraph[1:])

    else:
        # pick last node in result
        last = result[-1]
        for i in xrange(len(restGraph)):
            currentEdge = restGraph[i]
            if currentEdge[0] == last:
                result.append(currentEdge[1])
                del restGraph[i]
                triedResult = helper(result, restGraph)

                if triedResult:
                    return triedResult
                else:
                    del result[-1]
                    restGraph.append(currentEdge)

            elif currentEdge[1] == last:
                result.append(currentEdge[0])
                del restGraph[i]
                triedResult = helper(result, restGraph)

                if triedResult:
                    return triedResult
                else:
                    del result[-1]
                    restGraph.append(currentEdge)
            else:
                continue

        return None


graph = [(1, 2), (2, 3), (3, 1)]
print find_eulerian_tour(graph), '\n'

graph = [(0, 1), (1, 5), (1, 7), (4, 5),
(4, 8), (1, 6), (3, 7), (5, 9),
(2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
print find_eulerian_tour(graph),'\n'

graph = [(1, 13), (1, 6), (6, 11), (3, 13),
(8, 13), (0, 6), (8, 9),(5, 9), (2, 6), (6, 10), (7, 9),
(1, 12), (4, 12), (5, 14), (0, 1),  (2, 3), (4, 11), (6, 9),
(7, 14),  (10, 13)]
print find_eulerian_tour(graph),'\n'

graph =  [(8, 16), (8, 18), (16, 17), (18, 19),
(3, 17), (13, 17), (5, 13),(3, 4), (0, 18), (3, 14), (11, 14),
(1, 8), (1, 9), (4, 12), (2, 19),(1, 10), (7, 9), (13, 15),
(6, 12), (0, 1), (2, 11), (3, 18), (5, 6), (7, 15), (8, 13), (10, 17)]
print find_eulerian_tour(graph)
