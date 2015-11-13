# Mengtian Li
# Comp135 a3
# Kmeans.py
# Nov 2, 2015
from __future__ import division
import sys, random, math


data=[] # Hold raw data 
data_class=[] # Hold class labels
real_cluster=[] # Actual class with real label

# Reading data files, store real labels in real_cluster and data correspond to real labels in real_cluster
# data structure is a list of features in a list called data_list
def read_data(file_path, data_list):
	global data_class
	global real_cluster
	with open(file_path) as f:
		for line in f:
			if 'class' in line:
				data_class = line.split()
				data_class = data_class[2].split(',')
				data_class[0] = data_class[0][1:]
				data_class[-1] = data_class[-1][:-1]
				real_cluster = [[] for i in range(len(data_class))]
				continue
			if line[0].isdigit() or line[0] == '-':
				features = []
				feature = line.split(',')
				for data in feature:
					try:
						features.append(float(data))
					except:
						features.append(data)
				data_list.append(features)
				for label in data_class:
					if label in str(features[-1]):
						real_cluster[data_class.index(label)].append(features[:-1])


# Calculate the distance between two points
def dist(data1, data2):
	sum = 0.0
	for i in range(0, len(data1)):
		sum = sum + pow((data1[i] - data2[i]), 2)
	return pow(sum, .5)

# Argument 1: data path
# Argument 2: k
# Argument 3: seed
def main():
	read_data(sys.argv[1], data)
	# Hold data without label
	data_clear=[]
	for point in data:
		data_clear.append(point[:-1])
	k = int(sys.argv[2])
	# Generate seed
	seed = int(sys.argv[3]) * k
	num_data = len(data_clear)
	# To hold the center points without label
	centers=[]
	# Generate k random center
	for i in range(seed,k+seed):
		random.seed(i)
		centers.append(data_clear[int(random.randint(0,num_data))])
	# Each index is a list of points corresponds to center inex
	clusters=[[] for i in range(k)]
	while (1):
		curr_clusters=[[] for i in range(k)]
		# Associate examples with centers
		for point in data_clear:
			# Store distance from each center
			tmp=[]
			for i in range(0,k):
				tmp.append(dist(point, centers[i]))
			label = tmp.index(min(tmp))
			curr_clusters[label].append(point)
		# Check for convergence
		flag = 1
		for i in range(0,k):
			for element in curr_clusters[i]:
				if element not in clusters[i]:
					flag = 0
		if flag:
			break
		# Calculate means
		for i in range(0,k):
			# Store the mean for each feature
			tmp=[]
			for j in range(0, len(data_clear[0])):
				sum = 0
				count = 0
				for element in curr_clusters[i]:
					sum = sum + element[j]
					count += 1
				if count == 0 :
					sys.exit(1)
				tmp.append(float(sum)/float(count))
			centers[i]=tmp
		clusters = curr_clusters
	# Calculate CS
	CS = 0
	for c in clusters:
		for element in c:
			CS += pow(dist(element, centers[clusters.index(c)]), 2)
	# Build the contingency table, each row corresponds to real label
	contingency=[[] for i in range(len(data_class))]
	for element in contingency:
	    for i in range(0,k):
		element.append([])
	H_real=0
	H_cluster=0
	N=0
	a=[]
	b=[]
	# Count overlap
	for i in range(0,len(data_class)):
	    for j in range(0, k):
		contingency[i][j]=0
		for element in real_cluster[i]:
		    if element in clusters[j]:
			contingency[i][j]+=1
	# Calculate both N and ai
	for i in range(0,len(data_class)):
	    tmp_sum = 0
	    for j in range(0,k):
		N+=contingency[i][j]
		tmp_sum+=contingency[i][j]
	    a.append(tmp_sum)
	# Calculate bi
	for j in range(0,k):
	    tmp_sum = 0
	    for i in range(0, len(data_class)):
		tmp_sum+=contingency[i][j]
	    b.append(tmp_sum)
	# Calculate H for real label
	for i in range(0, len(data_class)):
	    H_real+=((a[i] / N)*(math.log(a[i] / N)))
	# Calculate H for generated cluster
	for i in range(0,k):
	    H_cluster+=((b[i] / N)*(math.log(b[i] / N)))
	H_real = -1 * H_real
	H_cluster = -1 * H_cluster
	# Calculate I
	I=0
	for i in range(0, len(data_class)):
	    for j in range(0, k):
		if contingency[i][j] == 0:
		    continue
		I+=((contingency[i][j] / N) * math.log((contingency[i][j] / N) / (a[i]*b[j] / pow(N, 2))))
	NMI=2*I/(H_real + H_cluster)
	print CS, NMI
main()