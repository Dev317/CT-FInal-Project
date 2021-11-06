
def find_highest_scores_and_paths(edges, weights, start, end):
    answer = .0
    paths_list = []

    # create a graph
    graph = create_graph(edges,weights)
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
            
        limit = 0
        list_weight = []
        for neighbour in graph[curr_path[-1]]:
            list_weight.append(neighbour[1])
        
        for i in list_weight:
            limit += i
        limit /= len(list_weight)

        for neighbour in graph[curr_path[-1]]:
            if neighbour[0] not in curr_path and neighbour[1] >= limit:
                new_path = curr_path + [neighbour[0]]
                new_product = curr_product * neighbour[1]
                queue.append((new_path, new_product))
    
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