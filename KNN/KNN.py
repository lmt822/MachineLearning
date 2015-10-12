# Mengtian Li
# Comp135 a1
# Sept 27, 2015
import sys
from operator import itemgetter

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
		sum = sum + (w[i] * pow((data1[i] - data2[i]), 2))
	return pow(sum, .5)
# Reading data files
# data structure is a list of features in a list called data_list
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

# Calculate KNN, assume k is odd
# For each test data, maintain a list of size k to record the nearest neighbors
# Each element in that list is a vector with training data itself and the distance
# Once the maximum distance in that list is larger than the new distance from current data
# Update the list
# Finally, compare the elements in list to conclude which outcome is dominant
def Calculate_KNN(training, test, k):
	accurate = 0.0
	for te in test:
		nearest_so_far=[]
		for tr in training:
			if len(nearest_so_far) < k:
				nearest_so_far.append([tr, calculate_dist(te, tr)])
			else:
				curr_dist = calculate_dist(te, tr)
				nearest_so_far = sorted(nearest_so_far, key=itemgetter(1))
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


# two arguments for training and test data, third is k must be odd
def main():
 	read_data(sys.argv[1], training_data)
 	read_data(sys.argv[2], test_data)
	global num_of_features 
	num_of_features = len(training_data[0]) - 1
	k = int(sys.argv[3])
	accuracy = Calculate_KNN(training_data, test_data, k)
	print num_of_features, "", accuracy
main()