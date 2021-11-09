import heapq
from collections import defaultdict

def ranking_func(edges, weights, start):
    graph = create_graph(edges,weights)
    all_possible_vertices = []
    all_reacheable_vertices = []

    for vertice in graph:
        if vertice == start:
            continue
        
        # include only items
        if vertice.find("i") != -1:
            all_possible_vertices.append(vertice)
    
    # find all the vertices that the starting can reach
    for vertice in all_possible_vertices:
        visited = []
        if check_if_reachable(graph,start,vertice,visited):
            all_reacheable_vertices.append(vertice)

    # find all the max weight product for each pair of starting point and ending point
    result = []
    for vertice in all_reacheable_vertices:
        max_score = find_highest_scores(graph, start, vertice)
        result.append((vertice,max_score))
    
    # sort in descending order
    result_sorted = sorted(result, key=lambda tup: (tup[1], -ord(tup[0][1])), reverse=True)

    if len(result_sorted) < 5:
        return result_sorted

    ranked = []
    for i in range(5):
        ranked.append(result_sorted[i])
    
    return ranked

# implementatio is similar to pq1, just that need to find max weight product only
def find_highest_scores(graph, start, end):
    answer = 0.
    heap = [(-1,start)]

    seen = defaultdict(lambda : 0)

    while heap:
        prob, node = heapq.heappop(heap)
        prob *= -1

        for neighbor, edge_prob in graph[node]:
            new_prob = prob * edge_prob

            if seen[neighbor] <= new_prob:
                heapq.heappush(heap, (-new_prob, neighbor))
                seen[neighbor] = new_prob
                
    answer = seen[end]
    return answer

def check_if_reachable(graph,start,end,visited):

    if start == end:
        return True
    
    if start in visited:
        return False
    
    visited.append(start)

    for neighbour in graph[start]:
        if check_if_reachable(graph,neighbour[0],end,visited):
            return True
    
    return False

def create_graph(edges, weights):
    graph = {}
    for idx in range(len(edges)):
        
        # if the vertex is not in the graph, create a new mapping
        if edges[idx][0] not in graph:
            new_list = []
            new_list.append((edges[idx][1], weights[idx]))
            graph[edges[idx][0]] = new_list
        else:
            current_list = graph[edges[idx][0]]
            current_list.append((edges[idx][1], weights[idx]))
            graph[edges[idx][0]] = current_list
    
    return graph