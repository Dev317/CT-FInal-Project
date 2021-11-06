import time

def ranking_func(edges, weights, start):
    graph = create_graph(edges)

    all_possible_vertices = []
    all_reacheable_vertices = []

    for vertices in graph:
        if vertices == start:
            continue
        
        # include only items
        if vertices.find("i") != -1:
            all_possible_vertices.append(vertices)
    
    for vertices in all_possible_vertices:
        visited = []
        if check_if_reachable(graph,start,vertices,visited):
            all_reacheable_vertices.append(vertices)
    
    # print(all_reacheable_vertices)
        

    result = []
    for vertice in all_reacheable_vertices:
        max_score = find_highest_scores(edges, weights, start, vertice)
        result.append((vertice,max_score))
    
    # sort by item and max_score
    result_sorted = sorted(result, key=lambda tup: (tup[1], -ord(tup[0][1])))
    result_sorted.reverse()

    if len(result_sorted) < 5:
        return result_sorted

    # print(result_sorted)

    ranked = []
    for i in range(5):
        ranked.append(result_sorted[i])
    
    print(ranked)
    return ranked


def check_if_reachable(graph,start,end,visited):

    if start == end:
        return True
    
    if start in visited:
        return False
    
    visited.append(start)

    for neighbour in graph[start]:
        if check_if_reachable(graph,neighbour,end,visited):
            return True
    
    return False

############
def find_highest_scores(edges, weights, start, end):
    answer = 0.
    # paths_list = [[]]
    paths_list = []

    visited = []
    graph = create_graph(edges)

    # paths_list = dfs_find_all_paths(graph,start,end)
    paths_list = bfs_find_all_paths(graph,start,end,paths_list)
    # print(paths_list)

    edge_weight_map = edge_weight(edges, weights)
    score_list = find_score(edge_weight_map, paths_list)
    # print(score_list)

    max_score = 0


    # create a tupple with path and its weight_product
    score_map = []
    for i in range(len(score_list)):
        if score_list[i] > max_score:
            max_score = score_list[i]
        
        score_map.append((paths_list[i],score_list[i]))
    
    answer = max_score

    return answer

def find_score(edge_weight_map, paths_list):
    final_score = []

    for path in paths_list:
        temp_score = 1
        for i in range(len(path) - 1):
            key = path[i] + "," + path[i+1]
            temp_score *= edge_weight_map[key]
        final_score.append(temp_score)
    
    return final_score


def edge_weight(edges, weights):
    idx = 0
    edge_weight_map = {}
    for edge in edges:

        edge_weight_element = []
        key = edge[0] + "," + edge[1]
        edge_weight_map[key] = weights[idx]

        idx += 1
    
    return edge_weight_map

#BFS
def bfs_find_all_paths(graph,start,end,paths_list):
    queue = []

    curr_path = []

    curr_path.append(start)
    queue.append(curr_path)
    
    # limit to 1000 possible paths
    counter = 0

    while len(queue) != 0 and counter < 1000:
        curr_path = queue.pop(0)

        if curr_path[-1] == end:
            paths_list.append(curr_path)
            counter += 1
        
        for neighbour in neighbours(edges,curr_path[-1]):
            if neighbour not in curr_path:

                new_path = []
                for i in curr_path:
                    new_path.append(i)

                new_path.append(neighbour)
                queue.append(new_path)

    return paths_list

def create_graph(edges):
    graph = {}
    vertex_list = []
    for edge in edges:
        if edge[0] not in vertex_list:
            vertex_list.append(edge[0])
            graph[edge[0]] = [edge[1]]
        else:
            neighbours = graph[edge[0]]
            neighbours.append(edge[1])
            graph[edge[0]] = neighbours
    
    return graph
        
def neighbours(edges, vertex):
    neighbours_list = []
    for edge in edges:
        if edge[0] == vertex:
            neighbours_list.append(edge[1])
    return neighbours_list
#############

# read sample.txt and return the data in the format of start, edges, weights.
def read_triple_weight_txt(filename):
    edges = []
    weights = []
    first = True
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split(' ')
            if first == True:
                start = line[0]
                first = False
            else:
                edges.append([line[0], line[2]])
                weights.append(round(float(line[3]),2))
    return start, edges, weights

#evaluation for q2
def evaluation_q2_ranking(pd_sample, sample_answer):
    gt_ranking_sample = sample_answer[:5]
    predicted_items = [k for k,v in pd_sample][:5]
    accumulative_scores = []
    accumulative_score = 0.
    visited_dict = dict([('i'+str(k), 0) for k in range(1000)])
    for i in range(len(gt_ranking_sample)):
        gt_ranking_sample_dict = dict(gt_ranking_sample[:i+1])

        predicted_pair = pd_sample[i]
        predicted_item = predicted_pair[0]
        predicted_score = predicted_pair[1]
        if visited_dict[predicted_item]!=1 and predicted_item in gt_ranking_sample_dict:
            # rel is the weighted intersection score shown in the above description of evaluation metric
            rel = round(1 - abs(predicted_score - gt_ranking_sample_dict[predicted_item]),2)
            visited_dict[predicted_item] = 1
        else:
            rel = 0
        
        # p(k)
        accumulative_score += rel
        # try:
        # prepare for the final score
        accumulative_scores.append(accumulative_score/(i+1))
        # except:
        #     accumulative_scores.append(0.)
    # overallScore = correctness score 2.0 + 3 x final Score
    overallScore = 2.0 + 3*(sum(accumulative_scores)/len(accumulative_scores))
    return overallScore


###########################################################################
####################### test case sample1.txt #############################

t1 = time.time()
sample_filename = './sample1.txt'
start, edges, weights = read_triple_weight_txt(sample_filename)
ranking = ranking_func(edges, weights, start)

sample_answer = [('i0', 1.0), ('i1', 0.5), ('i3', 0.36000000000000004), ('i2', 0.045)]

print ('ranking_list:', ranking)

evaluation_score = evaluation_q2_ranking(ranking, sample_answer)

# print (len(ranking))
print ('evaluation_score:',evaluation_score)
t2 = time.time()
print (f'time: {t2-t1}')




###########################################################################
####################### test case sample2.txt #############################
# t1 = time.time()
# sample_filename = './sample2.txt'
# start, edges, weights = read_triple_weight_txt(sample_filename)
# ranking = ranking_func(edges, weights, start)

# sample_answer = [('i0', 0.7), ('i1', 0.6), ('i2', 0.6), ('i6', 0.504), ('i4', 0.44799999999999995), ('i5', 0.44799999999999995), ('i3', 0.3528), ('i7', 0.3528)]

# print ('ranking_list:', ranking)

# evaluation_score = evaluation_q2_ranking(ranking, sample_answer)

# # print (len(ranking))
# print ('evaluation_score:',evaluation_score)
# t2 = time.time()
# print (f'time: {t2-t1}')


###########################################################################
####################### test case sample3.txt #############################
# t1 = time.time()
# sample_filename = './sample3.txt'
# start, edges, weights = read_triple_weight_txt(sample_filename)
# ranking = ranking_func(edges, weights, start)

# sample_answer =[('i11', 0.9), ('i5', 0.54), ('i6', 0.48600000000000004), ('i7', 0.48600000000000004), ('i9', 0.48600000000000004), ('i10', 0.48600000000000004), ('i8', 0.38880000000000003), ('i4', 0.34992000000000006), ('i2', 0.3), ('i0', 0.2916), ('i3', 0.27216), ('i1', 0.1)]

# print ('ranking_list:', ranking)

# evaluation_score = evaluation_q2_ranking(ranking, sample_answer)

# # print (len(ranking))
# print ('evaluation_score:',evaluation_score)
# t2 = time.time()
# print (f'time: {t2-t1}')
