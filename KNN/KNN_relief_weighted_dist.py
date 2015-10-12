# Mengtian Li
# Comp135 a1
# Sept 27, 2015
import sys
from operator import itemgetter
import random
# Lists to hold data read from arff file
training_data=[]
test_data=[]
k=0;

# Assume data1 and data2 have same number of features, leave the last 
# classification alone
def calculate_dist(data1,data2):
	sum = 0.0
	for i in range(0, num_of_features):
		sum = sum + pow((data1[i] - data2[i]), 2)
	return pow(sum, .5)
# Same as above except w is a list of weights for features
def calculate_wdist(data1,data2,w):
	sum = 0.0
	for i in range(0, num_of_features):
		sum = sum + (w[i][1] * pow((data1[i] - data2[i]), 2))
	return pow(sum, .5)
# Reading data files
# data structure is lists of features in data_name which is also list
def read_data(file_path, data_list):
	with open(file_path) as f:
		for line in f:
			if line[0].isdigit():
				features = []
				feature = line.split(',')
				for data in feature:
					try:
						features.append(float(data))
					except:
						features.append(data)
				data_list.append(features)

# Calculate KNN, assume k is odd, use weighted distance
# For each test data, maintain a list of size k to record the nearest neighbors
# Each element in that list is a vector with training data itself and the distance
# Once the maximum distance in that list is larger than the new distance from current data
# Update the list
# Finally, compare the elements in list to conclude which outcome is dominant
def Calculate_KNN(training, test, k, w):
	accurate = 0.0
	for te in test:
		nearest_so_far=[]
		for tr in training:
			if len(nearest_so_far) < k:
				nearest_so_far.append([tr, calculate_wdist(te, tr, w)])
			else:
				curr_dist = calculate_wdist(te, tr, w)
				nearest_so_far=sorted(nearest_so_far, key=itemgetter(1))
				cmp_dist = nearest_so_far[k-1][1]
				if curr_dist < cmp_dist:
					del nearest_so_far[-1]
					nearest_so_far.append([tr, curr_dist])
		count0 = 0
		count1 = 0
		for list in nearest_so_far:
			if list[0][num_of_features] == 0:
				count0+=1;
			else:
				count1+=1;
		if count0 > count1:
			if te[num_of_features] == 0:
				accurate = accurate + 1.0
		else:
			if te[num_of_features] == 1:
				accurate = accurate + 1.0		
	return (accurate / float(len(test))) * 100		
# Relief for w
# First, pick a index randomly. Keep a list of vectors <data, distance from chosen data>
# Calculate distance for each training data points, then sort based on distance
# Apply two while loop to go through the list to find the nearest same label data as well
# as opposite label data
# Then update the weights using the formula provided in instruction
# Repeat for m times
def relief(training, k, m, w):
	for i in range(0,m):
		neighbors=[]
		r = random.randint(0, len(training) - 1)
		for tr in training:
			if training.index(tr) != r:
				curr_dist = calculate_dist(tr, training[r])
				neighbors.append([tr, curr_dist])
		neighbors=sorted(neighbors, key=itemgetter(1))
		hit_flag = 1
		hit_index = 0
		i = 0
		while(hit_flag):
			if neighbors[i][0][num_of_features] == training[r][num_of_features]:
				hit_flag = 0
				hit_index = i
			i += 1
		miss_flag = 1
		miss_index = 0
		j = 0
		while(miss_flag):
			if neighbors[j][0][num_of_features] != training[r][num_of_features]:
				miss_flag = 0
				miss_index = j
			j += 1
		for element in w:
			diff1 = abs(neighbors[hit_index][0][element[0]] - training[r][element[0]])
			diff2 = abs(neighbors[miss_index][0][element[0]] - training[r][element[0]])
			element[1] = element[1] -  diff1 + diff2
# Two arguments for training and test data, third is k must be odd, fourth is m
# Maintain the weights in a list called w. Each element in w is a vector with No. of feature
# weight of that feature
# After relief, do normal Calculate_KNN but with weighted distance. If weight is negative,
# adjust to zero
def main():
 	read_data(sys.argv[1], training_data)
 	read_data(sys.argv[2], test_data)
	global num_of_features 
	w = []
	num_of_features = len(training_data[0]) - 1
	k = int(sys.argv[3])
	m = int(sys.argv[4])
	for i in range(0, num_of_features):
		w.append([i, 0])
	relief(training_data, k, m, w)
	for element in w:
		if element[1] < 0:
			element[1] = 0
	accuracy = Calculate_KNN(training_data, test_data, k, w)
	print num_of_features, "", accuracy
main()