import time

def ranking_func(edges, weights, start):
    ranked = []
    return ranked

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



"""
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
"""