import time

def find_highest_scores_and_paths(edges, weights, start, end):
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

    score_map = []
    for i in range(len(score_list)):
        if score_list[i] > max_score:
            max_score = score_list[i]
        
        score_map.append((paths_list[i],score_list[i]))
    
    answer = max_score
    final_path_list = []

    for tupple in score_map:
        if tupple[1] == max_score:
            final_path_list.append(tupple[0])


    return answer, final_path_list

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

# DFS
# def dfs_find_all_paths(graph, start, end, path=[]):
#         path = path + [start]
#         if start == end:
#             return [path]
#         if start not in graph:
#             return []
#         paths = []
#         for node in graph[start]:
#             if node not in path:
#                 newpaths = find_all_paths(graph, node, end, path)
#                 for newpath in newpaths:
#                     paths.append(newpath)
#         return paths  

#BFS
def bfs_find_all_paths(graph,start,end,paths_list):
    queue = []

    curr_path = []

    curr_path.append(start)
    queue.append(curr_path)
    counter = 0

    while len(queue) != 0 and counter < 10000:
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

    # print(paths_list)
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
    



# read sample.txt and return the data in the format of start, end, edges, weights.
def read_triple_weight_txt(filename):
    edges = []
    weights = []
    first = True
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split(' ')
            if first == True:
                start = line[0]
                end = line[1]
                first = False
            else:
                # head_relation_tail = line[:3]
                # weight = line[3]
                edges.append([line[0], line[2]])
                weights.append(round(float(line[3]),2))
    return start, end, edges, weights

def is_valid_path(path, edges):
    edge_dict = set()
    for edge in edges:
        edge_dict.add('->'.join(edge))
    len_ = len(path)-1
    for i in range(len_):
        edge = path[i]+'->'+path[i+1]
        if edge not in edge_dict:
            return 0
    return 1

# evaluation for q1
def evaluate_q1(predict_sample, sample_answer, edges):
    '''
    predict_sample: algorithm answer
    sample_answer: ground truth answer
    '''
    for path in predict_sample[1]:
        if is_valid_path(path, edges) == 0:
            return 0

    #award correctness score of 2.0
    score = 2.0
    gt_sample = sample_answer

    ### these are for the special case, no path between the starting user and the end item in graph
    if gt_sample[0] == 0 and gt_sample[1] == []:
        if predict_sample[0] == 0 and predict_sample[1] == []:
            score += 3.0
            return score
    
    ### Path Scoring
    if abs(gt_sample[0] - predict_sample[0]) < 1e-5:
        score += 2.0
    else:
        score += (1-abs(gt_sample[0] - predict_sample[0])*1.0/gt_sample[0])*2
        return score

    ### if algo path score is max path score, then compare path list.
    gt_dict = {}
    gt_visited_dict = {}
    for path in gt_sample[1]:
        gt_dict['_'.join(path)]= 0.0
        gt_visited_dict['_'.join(path)] = 0
    for path in predict_sample[1]:
        if '_'.join(path) in gt_dict and gt_visited_dict['_'.join(path)]==0:
            gt_dict['_'.join(path)] = 1.0/len(gt_sample[1])
            gt_visited_dict['_'.join(path)] = 1

    score += sum(list(gt_dict.values()))
    return score

def print_graph(start,end,edges,weights):
    print("Starting point:", start)
    print("Ending point:", end)
    print("Edges: ", edges)
    print("Weights: ", weights)

###########################################################################
####################### test case sample1.txt #############################

t1 = time.time()
sample_filename = './sample1.txt'
start, end, edges, weights = read_triple_weight_txt(sample_filename)
print_graph(start,end,edges,weights)
# max_score answer for sample1.txt
sample1_answer = (0.045, [['u0', 'i1', 'u1', 'i2']])

# run your algorithm
maxscore, paths_list = find_highest_scores_and_paths(edges, weights, start, end)

# evaluation
evaluation_score = evaluate_q1(predict_sample=[maxscore, paths_list], sample_answer=sample1_answer, edges=edges)

print (f'maxscore: {maxscore}')
print (f'paths_list: {paths_list}')
print (f'evaluation_score: {evaluation_score}')
t2 = time.time()
print (f'Time:{t2-t1}')


###########################################################################
####################### test case sample2.txt #############################
t1 = time.time()
sample_filename = './sample2.txt'
start, end, edges, weights = read_triple_weight_txt(sample_filename)

# max_score answer for sample2.txt
sample2_answer = (0.504, [['u0', 'i0', 'obj7', 'i6'], ['u0', 'i0', 'u3', 'i6']])

# run your algorithm
maxscore, paths_list = find_highest_scores_and_paths(edges, weights, start, end)

# evaluation
evaluation_score = evaluate_q1(predict_sample=[maxscore, paths_list], sample_answer=sample2_answer, edges=edges)

print (f'maxscore: {maxscore}')
print (f'paths_list: {paths_list}')
print (f'evaluation_score: {evaluation_score}')
t2 = time.time()
print (f'Time:{t2-t1}')


###########################################################################
####################### test case sample3.txt #############################
t1 = time.time()
sample_filename = './sample3.txt'
start, end, edges, weights = read_triple_weight_txt(sample_filename)

# max_score answer for sample3.txt
sample3_answer = (0.34992, [['u0', 'i11', 'obj7', 'i5', 'obj5', 'obj3', 'obj2', 'i4']])

# run your algorithm
maxscore, paths_list = find_highest_scores_and_paths(edges, weights, start, end)

# evaluation
evaluation_score = evaluate_q1(predict_sample=[maxscore, paths_list], sample_answer=sample3_answer, edges=edges)

print (f'maxscore: {maxscore}')
print (f'paths_list: {paths_list}')
print (f'evaluation_score: {evaluation_score}')
t2 = time.time()
print (f'Time:{t2-t1}')

###########################################################################
###########################################################################
