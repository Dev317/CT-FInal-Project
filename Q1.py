import time

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

def find_highest_scores_and_paths(edges, weights, start, end):
  answer = 0.
  paths_list = []
  # TODO: edit this function.
  return answer, paths_list







###########################################################################
####################### test case sample1.txt #############################

t1 = time.time()
sample_filename = './sample1.txt'
start, end, edges, weights = read_triple_weight_txt(sample_filename)

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

"""
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
"""