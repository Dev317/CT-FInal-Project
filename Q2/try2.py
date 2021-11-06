import time

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
    
    print(ranked)
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
t1 = time.time()
sample_filename = './sample2.txt'
start, edges, weights = read_triple_weight_txt(sample_filename)
ranking = ranking_func(edges, weights, start)

sample_answer = [('i0', 0.7), ('i1', 0.6), ('i2', 0.6), ('i6', 0.504), ('i4', 0.44799999999999995), ('i5', 0.44799999999999995), ('i3', 0.3528), ('i7', 0.3528)]

print ('ranking_list:', ranking)

evaluation_score = evaluation_q2_ranking(ranking, sample_answer)

# print (len(ranking))
print ('evaluation_score:',evaluation_score)
t2 = time.time()
print (f'time: {t2-t1}')


###########################################################################
####################### test case sample3.txt #############################
t1 = time.time()
sample_filename = './sample3.txt'
start, edges, weights = read_triple_weight_txt(sample_filename)
ranking = ranking_func(edges, weights, start)

sample_answer =[('i11', 0.9), ('i5', 0.54), ('i6', 0.48600000000000004), ('i7', 0.48600000000000004), ('i9', 0.48600000000000004), ('i10', 0.48600000000000004), ('i8', 0.38880000000000003), ('i4', 0.34992000000000006), ('i2', 0.3), ('i0', 0.2916), ('i3', 0.27216), ('i1', 0.1)]

print ('ranking_list:', ranking)

evaluation_score = evaluation_q2_ranking(ranking, sample_answer)

# print (len(ranking))
print ('evaluation_score:',evaluation_score)
t2 = time.time()
print (f'time: {t2-t1}')