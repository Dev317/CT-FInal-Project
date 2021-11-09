import heapq
from collections import defaultdict
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
    
    result_sorted = sorted(result, key=lambda tup: (tup[1], -ord(tup[0][1])), reverse=True)
    # result_sorted.reverse()

    if len(result_sorted) < 5:
        return result_sorted

    ranked = []
    for i in range(5):
        ranked.append(result_sorted[i])
    
    # print(ranked)
    return ranked

def find_highest_scores(graph, start, end):
    answer = 0.
    heap = [(-1,start)]

    seen = defaultdict(lambda : 0)

    while heap:
        # print(heap)
        prob, node = heapq.heappop(heap)
        prob *= -1

        for neighbor, edge_prob in graph[node]:
            new_prob = prob * edge_prob

            if seen[neighbor] <= new_prob:
                heapq.heappush(heap, (-new_prob, neighbor))
                seen[neighbor] = new_prob
    # print(seen[end])
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
                first = False
            else:
                edges.append([line[0], line[2]])
                weights.append(round(float(line[3]),3))
    return start, edges, weights

def is_in_gt_pool(pred_item, sample_pool):
    for k, v in sample_pool.items():
        # print ('ff', k, v)
        if pred_item in v:
            return float(k)
    return 0.

#evaluation for q2 (updated Nov 7, 12:36pm)
def evaluation_q2_ranking(pd_sample, sample_answer):
    gt_ranking_sample = sample_answer
    gt_sample_pool = {}
    count = 0
    for elem in gt_ranking_sample:
        if str(elem[1]) not in gt_sample_pool:
            count +=1
            if count >=6:
                break
            gt_sample_pool[str(elem[1])] = [elem[0]]
            
        else:
            gt_sample_pool[str(elem[1])].append(elem[0])
    # print (gt_sample_pool)
    predicted_items = [k for k,v in pd_sample][:5]
    # gold_items = [k for k, v in gt_ranking_sample]
    # pi = []
    accumulative_scores = []
    accumulative_score = 0.
    visited_dict = dict([('i'+str(k), 0) for k in range(1000)])
    iter_len = 5 if len(sample_answer)>5 else len(sample_answer)
    for i in range(iter_len):
        # gt_ranking_sample_dict = dict(gt_ranking_sample[:i+1])

        try: ### try except is for the case where the number of prediction is less than 5.
            predicted_pair = pd_sample[i]
            predicted_item = predicted_pair[0]
            predicted_score = predicted_pair[1]
            # if visited_dict[predicted_item]!=1 and predicted_item in gt_ranking_sample_dict:
            ret_val = is_in_gt_pool(predicted_item, gt_sample_pool)
            # print (f'pre:{predicted_pair}, s:{ret_val}')
            if visited_dict[predicted_item]!=1 and ret_val!=0.:
                # rel is the weighted intersection score shown in the above description of evaluation metric
                # rel = round(1 - abs(predicted_score - gt_ranking_sample_dict[predicted_item]),2)
                rel = round(1 - abs(predicted_score - sample_answer[i][1]),2)
                visited_dict[predicted_item] = 1
            else:
                rel = 0
        except:
            rel = 0
        
        # p(k)
        accumulative_score += rel
        # try:
        # prepare for the final score
        accumulative_scores.append(accumulative_score/(i+1))
        # except:
        #     accumulative_scores.append(0.)
    # final score: \sum_{k=1}^{n}{p(k)} / n
    #return sum(accumulative_scores)/len(accumulative_scores)
    # Overall Score = correctness Score + 3xfinal Score
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