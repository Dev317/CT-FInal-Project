import heapq
from collections import defaultdict

def find_highest_scores_and_paths(edges, weights, start, end):
    answer = 0.
    paths_list = []

    # create a graph with key as vertice, value as a tuple of neigbour vertice and weight
    graph = create_graph(edges, weights)

    # create a priority queue
    heap = [(-1,start,[start])]

    # a dictionary storing all the max product weight and path from a starting point to other points in the graph
    seen = defaultdict(lambda : (0, list))

    # modified dijkstra's algorithm
    while heap:
        product_weight, node, curr_path = heapq.heappop(heap)

        # convert product weight back to positive
        product_weight *= -1

        for neighbor, edge_weight in graph[node]:

            # find the new product weight
            new_product_weight = product_weight * edge_weight

            new_path = []
            for i in curr_path:
                new_path.append(i)
            
            # check if the new product weight is larger or equal to the current product weight
            if seen[neighbor][0] <= new_product_weight:
                new_path.append(neighbor)

                # convert product weight back to negative for sorting
                # large positive product weight -> when negative -> becomes small
                heapq.heappush(heap, (-new_product_weight, neighbor, new_path))

                # push the found path to paths_list once the ending point is reached
                if neighbor == end:
                    paths_list.append(new_path)

                seen[neighbor] = (new_product_weight, new_path)

    answer = seen[end][0]
    return answer, paths_list


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
