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
    
    for vertice in all_possible_vertices:
        visited = []
        if check_if_reachable(graph,start,vertice,visited):
            all_reacheable_vertices.append(vertice)
    
    
    result = []
    for vertice in all_reacheable_vertices:
        max_score = find_highest_scores(graph, start, vertice)
        result.append((vertice,max_score))
    
    # sort by item and max_score
    result_sorted = sorted(result, key=lambda tup: (tup[1], -ord(tup[0][1])))
    result_sorted.reverse()

    if len(result_sorted) < 5:
        return result_sorted

    ranked = []
    for i in range(5):
        ranked.append(result_sorted[i])
    
    return ranked

def find_highest_scores(graph, start, end):
    answer = .0
    paths_list = []

    queue = []
    queue_element = ([start],1)
    queue.append(queue_element)
    stored_paths = []

    while len(queue) != 0:
        curr_element = queue.pop(0)
        curr_path = curr_element[0]
        curr_product = curr_element[1]

        if curr_path[-1] == end:
            if curr_product > answer and curr_path not in stored_paths:
                stored_paths.append(curr_path)
                answer = curr_product
                while len(paths_list) != 0:
                    paths_list.pop(0)
                paths_list.append(curr_path)
            
            if curr_product == answer and curr_path not in stored_paths:
                stored_paths.append(curr_path)
                paths_list.append(curr_path)
            

        list_weight = []
        for neighbour in graph[curr_path[-1]]:
            list_weight.append(neighbour[1])
        list_weight.sort(reverse=True)

        limit = 0
        if len(list_weight) >= 2:
            limit = list_weight[1]
        else:
            limit = list_weight[0]

        for neighbour in graph[curr_path[-1]]:
            if neighbour[0] not in curr_path and neighbour[1] >= limit:
                new_path = curr_path + [neighbour[0]]
                new_product = curr_product * neighbour[1]
                queue.append((new_path, new_product))
    
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