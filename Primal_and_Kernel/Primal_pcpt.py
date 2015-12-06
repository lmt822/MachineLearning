# Mengtian Li
# Comp135 a4
# Dec 1, 2015
# Despite the name, this program can handle 4 different Machine Learning algorithms
# 1 is primal perceptron
# 2 is kernel perceptron
# 3 is primal KNN
# 4 is kernel KNN
import sys, math
from operator import itemgetter

# Lists to hold data read from arff file
training_data=[]
test_data=[]

# calculate norm between features
def calculate_dist(data1,data2):
	sum = 0.0
	for i in range(0, num_of_features):
		sum = sum + pow((data1[i] - data2[i]), 2)
	return pow(sum, .5)

# sign function
def sign(num):
	if num > 0:
		return 1
	return -1

# calculate dot product
def product(list1, list2):
	sum = 0.0
	for i in range(0, len(list1)):
		sum += float(list1[i]) * float(list2[i])  
	return sum

# calculate kernel value
# 0 for polynomial kernel
# 1 for RBF kernel
# Notice list must not contain labels
def kernel(list1, list2, kernel_name, kernel_param):
	if kernel_name == 0:
		d = kernel_param
		return pow(product(list1, list2)+1, d) 
	if kernel_name == 1:
		s = kernel_param
		return math.exp(-1*(pow(calculate_dist(list1, list2), 2)/(2*pow(s,2))))

# Reading data files
# data structure is a list of features in a list called data_list
def read_data(file_path, data_list):
	with open(file_path) as f:
		for line in f:
			if line[0].isdigit() or line[0] == '-':
				features = []
				feature = line.split(',')
				for data in feature:
					try:
						features.append(float(data))
					except:
						features.append(data)
				data_list.append(features)

# KNN implementation from old assignment
# Update: depending on algorithm, the distance is calculate in different ways
# 3 is for Primal KNN
# 4 is for Kernel KNN
def Calculate_KNN(training, test, k, algo):
	accurate = 0.0
	for te in test:
		nearest_so_far=[]
		for tr in training:
			if len(nearest_so_far) < k:
				if algo == 3:
					nearest_so_far.append([tr, calculate_dist(te, tr)])
				if algo == 4:
					tmp = 0.0
					tmp += kernel(te[:-1], te[:-1], kernel_name, kernel_param)
					tmp += kernel(tr[:-1], tr[:-1], kernel_name, kernel_param)
					tmp = tmp - 2*kernel(te[:-1], tr[:-1], kernel_name, kernel_param)
					nearest_so_far.append([tr, pow(tmp, .5)])
			else:
				if algo == 3:
					curr_dist = calculate_dist(te, tr)
				if algo == 4:
					tmp = 0.0
					tmp += kernel(te[:-1], te[:-1], kernel_name, kernel_param)
					tmp += kernel(tr[:-1], tr[:-1], kernel_name, kernel_param)
					tmp = tmp - 2*kernel(te[:-1], tr[:-1], kernel_name, kernel_param)
					curr_dist = pow(tmp, .5)
				nearest_so_far = sorted(nearest_so_far, key=itemgetter(1))
				cmp_dist = nearest_so_far[k-1][1]
				if curr_dist < cmp_dist:
					del nearest_so_far[-1]
					nearest_so_far.append([tr, curr_dist])
		count0 = 0
		count1 = 0
		for list in nearest_so_far:
			if list[0][num_of_features] == -1:
				count0+=1;
			else:
				count1+=1;
		if count0 > count1:
			if te[num_of_features] == -1:
				accurate = accurate + 1.0
		else:
			if te[num_of_features] == 1:
				accurate = accurate + 1.0		
	return (accurate / float(len(test)))

# Primal perceptron algorithm implementation
def primal_perceptron(training_data, tau, w):
	for i in range(0, 50):
		for element in training_data:
			# Classify
			O = sign(product(element[:-1], w))
			# Update
			if (element[-1] * product(element[:-1], w)) < tau:
				for i in range(num_of_features):
					w[i] = w[i] + element[-1]*element[i]

# Kernel perceptron algorithm implmenetation 
def kernel_perceptron(training_data, tau, alpha):
	for i in range(0, 50):
		# Classify
		for element in training_data:
			tmp_sum = 0.0
			for k in range(len(training_data)):
				tmp_sum += alpha[k]*training_data[k][-1]*kernel(element[:-1], training_data[k][:-1], kernel_name, kernel_param)
			O = sign(tmp_sum)
			# Update
			if element[-1]*tmp_sum < tau:
				alpha[training_data.index(element)] += 1

# Calculate threshold tau depending on algorithms
# 1 is for Primal perceptron
# 2 is for Kernel perceptron
def calc_tau(training_data, algo):
	if algo == 1:
		sum = 0.0
		for element in training_data:
			tmp_sum = 0.0
			for i in range(0, num_of_features):
				tmp_sum += pow(float(element[i]), 2)
			tmp_sum = pow(tmp_sum, .5)
			sum += tmp_sum
		return 0.1 * sum / len(training_data)
	if algo == 2:
		sum = 0.0
		for element in training_data:
			sum += pow(kernel(element[:-1], element[:-1], kernel_name, kernel_param), .5)
		return 0.1 * sum / len(training_data)

# 1st parameter is number of algorithm
# 1 is for Primal perceptron
# 2 is for Kernel Perceptron
# 3 is for Primal KNN
# 4 is for Kernel KNN
# 2nd, 3rd parameter is training data and test data
# Option 4th, 5th parameter
# if using Kernel method, 4th parameter is kernel method, 
# 5th parameter is kernel param
# 0 for polynomial kernel
# 1 for RBF kernel 
def main():
 	read_data(sys.argv[2], training_data)
 	read_data(sys.argv[3], test_data)
 	algo = int(sys.argv[1])
 	k = 1
 	global num_of_features, kernel_name, kernel_param
 	# Primal Perceptron
 	if algo == 1:
 		num_of_features = len(training_data[0])
 		# Add a new feature with value of 1
 		for element in training_data:
 			tmp = element[-1]
 			element[-1] = 1
 			element.append(tmp)
 		for element in test_data:
 			tmp = element[-1]
 			element[-1] = 1
 			element.append(tmp)
	 	tau = calc_tau(training_data, algo)
	 	# w is a list with k size
	 	w=[0 for i in range(num_of_features)]
		primal_perceptron(training_data, tau, w)
		# Test
		error = 0
		for element in test_data:
			O = sign(product(element[:-1], w))
			if O != element[-1]:
				error += 1
		print 1 - (float(error)/len(test_data))
	# Kernel Perceptron
	if algo == 2:
		num_of_features = len(training_data[0]) - 1
		kernel_name = int(sys.argv[4])
		kernel_param = float(sys.argv[5])
		tau = calc_tau(training_data, algo)
		# alpha is a list with N size
		alpha = [0 for i in range(len(training_data))]
		kernel_perceptron(training_data, tau, alpha)
		# Test
		error = 0
		for element in test_data:
			tmp_sum = 0.0
			for k in range(len(training_data)):
				tmp_sum += alpha[k]*training_data[k][-1]*kernel(element[:-1], training_data[k][:-1], kernel_name, kernel_param)
			O = sign(tmp_sum)
			if O != element[-1]:
				error += 1
		print 1 - (float(error)/len(test_data))
	# Primal KNN
	if algo == 3:
		# Add a feature of 1 to each example
		num_of_features = len(training_data[0])
		for element in training_data:
 			tmp = element[-1]
 			element[-1] = 1
 			element.append(tmp)
 		for element in test_data:
 			tmp = element[-1]
 			element[-1] = 1
 			element.append(tmp)
 		accuracy = Calculate_KNN(training_data, test_data, k, algo)
 		print accuracy
 	# Kernel KNN
 	if algo ==4:
 		num_of_features = len(training_data[0]) - 1
		kernel_name = int(sys.argv[4])
		kernel_param = float(sys.argv[5])
		accuracy = Calculate_KNN(training_data, test_data, k, algo)
		print accuracy
main()