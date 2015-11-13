# Mengtian Li
# Comp135 a2
# Oct 10 2015
# Cross_Validation_m.py
import sys
import os
import re
import math
import random
from operator import itemgetter

# read index from file either short or full
def read_index(file_path, index_list):
	with open(file_path) as f:
		for line in f:
			index_list.append(int(line))

# Read CLEAN files from given data_path and given index, then stores
# the content of each file to a file_list. Each index correspond to 
# the file name
def read_files(data_path, data_index):
	file_list = [None] * int(len(os.listdir(data_path)))	
	for entry in os.listdir(data_path):
		if entry.endswith("clean"):
			index = int(re.findall('\d+',entry)[0])
			if index in data_index:
				path = os.path.join(data_path, entry)
				with open(path, 'r') as f:
					temp = f.read()
					file_list[index] = temp
	return file_list

# Read a given file that contains the outcome of each text file
# store each index to either positive_index list or negative_index
# list
def read_class(dir_path, positive_index, negative_index, file_name):
	path = os.path.join(dir_path, file_name)
	with open(path) as f:
		for line in f:
			line = line.split('|')
			if line[1].lower().startswith('y'):
				positive_index.append(int(line[0]))
			else:
				negative_index.append(int(line[0]))

# Parse each training data to a list of tokens extract from text file
def parse_tokens(data_files, index_list, token_list, training_index):
	temp_list = []
	for i in index_list:
		if i in training_index:
			temp_list.append(data_files[i].split())
	for element in temp_list:
		for token in element:
			token_list.append(token)

# For each token in the token list, count the frequency of each token
# store each token and corresponding frequency in a vector in a list
# return the length of the number of distinct tokens
def calculate_freq(token_list, token_freq):
	token_seen = []
	for token in token_list:
		if token in token_seen:
			for element in token_freq:
				if element[0] == token:
					element[1] += 1
		else:
			token_seen.append(token)
			temp = []
			temp.append(token)
			temp.append(int(1))
			token_freq.append(temp)
	return len(token_seen)

# Return a data file list with index provided in index_list
def split_data(data_files, index_list):
	to_rtn = [None] * len(data_files)
	for i in index_list:
		to_rtn[i] = data_files[i]
	return to_rtn

# Given frequency list and total number of tokens, calculate with
# probability and smooth with m and vocabulary size
def calculate_prob(token_freq, token_count, m, v):
	for element in token_freq:
		element[1] = float(element[1] + m) / float(token_count + m*v)

# Return mean of a list
def mean(list):
	return sum(list) / float(len(list))

# Return sum of square deviations of sequence data.
def _ss(data):
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

# calculate standard deviation for list
def stdev(data):
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5	

# input file should include a file that specifies the index
# for training set.(Assume all in boundry)
# argument list:
# 1: path to data files
# 2: index list to select
# 3: m as smoothing factor
def main():
	# Read from file
	N = 0.5
	for m in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
		data_files = []
		positive_index = []
		negative_index = []
		index_list = []	
		k_fold_list = [[] for i in range(2)]
		read_index(sys.argv[2], index_list)
		data_files = read_files(sys.argv[1], index_list)
		# prepare for 10-fold, get two list with positive text and negative
		# text 
		read_class(sys.argv[1], positive_index, negative_index, "index.Full")
		for index in index_list:
			if index in positive_index:
				k_fold_list[0].append(index)
			else:
				k_fold_list[1].append(index)
		random.shuffle(k_fold_list[0])
		random.shuffle(k_fold_list[1])
		# start 10 fold, if not divisble by 10, attach the remainders to 
		# last fold
		hold_positive = int(len(k_fold_list[0]) / 10)
		hold_negative = int(len(k_fold_list[1]) / 10)
		# attch first half in each fold with positive index and later half
		# with negative class
		for i in range(0, 10):
			tmp_list = []
			if i != 9:
				for j in range(0,hold_positive):
					tmp_list.append(k_fold_list[0].pop(0))
					j += 1
				for k in range(0, hold_negative):
					tmp_list.append(k_fold_list[1].pop(0))
					k += 1
			else:
				for index in k_fold_list[0]:
					tmp_list.append(index)
				for index in k_fold_list[1]:
					tmp_list.append(index)
			k_fold_list.append(tmp_list)
			i += 1
		# pop the first two list that is used to store the index of positive
		# and negative class
		k_fold_list.pop(0)
		k_fold_list.pop(0)
		
		# Run the cross validation
		accuracies = []
		for i in range(0, 10):
			training_data = []
			test_data = []
			training_index = []
			test_index = []
			positive_token_list = []
			negative_token_list = []
			positive_token_freq = []
			negative_token_freq = []
			test_score = []

			
			test_index = k_fold_list[i]
			for k in range(0, 10):
				if k != i:
					for element in k_fold_list[k]:
						training_index.append(element)
			# shuffle the training data so that each 0.x * N is randomized
			random.shuffle(training_index)
			# Select N number of sub sample
			cut = int(N * len(training_index))
			training_index = training_index[:cut] 
			
			# rest is basically same as naive_bayes.py
			training_data = split_data(data_files, training_index)
			test_data = split_data(data_files, test_index)
			
			# parse training data
			parse_tokens(training_data, positive_index, positive_token_list, training_index)
			parse_tokens(training_data, negative_index, negative_token_list, training_index)
			# Calculate the possiblity that positive and negative in training data
			training_size = len(positive_index) + len(negative_index)
			P_positive = float(len(positive_index)) / float(training_size)
			P_negative = float(len(negative_index)) / float(training_size)
			p_token_size = calculate_freq(positive_token_list, positive_token_freq)
			n_token_size = calculate_freq(negative_token_list, negative_token_freq)
			calculate_prob(positive_token_freq, len(positive_token_list), m, p_token_size)
			calculate_prob(negative_token_freq, len(negative_token_list), m, n_token_size)
			# Used for smoothing
			positive_token_count = len(positive_token_list)
			negative_token_count = len(negative_token_list)
			positive_v = p_token_size
			negative_v = n_token_size
			# calculate score for each test data
			for text in test_data:
				if text == None:
					continue
				else:
					temp_score = []
					temp_score.append(test_data.index(text))
					temp_text = text.split()
					# calculate positive score with smooth
					sum = math.log(P_positive)
					for token in temp_text:
						check = 1
						for element in positive_token_freq:
							if element[0] == token:
								sum = sum + math.log(element[1])
								check = 0
								break
						if check:
							sum = sum + math.log(float(m)/float(positive_token_count + m * positive_v))
					temp_score.append(sum)
					sum = math.log(P_negative)
					for token in temp_text:
						check = 1
						for element in negative_token_freq:
							if element[0] == token:
								sum = sum + math.log(element[1])
								check = 0
								break
						if check:
							sum = sum + math.log(float(m)/float(negative_token_count + m * negative_v))
					temp_score.append(sum)
				test_score.append(temp_score)
			# make prediction on threshold 0.5
			positive_prediction = []
			negative_prediction = []
			for element in test_score:
				if element[1] > element[2]:
					positive_prediction.append(element[0])
				else:
					negative_prediction.append(element[0])
			# calculate accuracy
			num_correct = 0
			for element in positive_prediction:
				if element in positive_index:
					num_correct += 1
			for element in negative_prediction:
				if element in negative_index:
					num_correct += 1
			accuracy = float(num_correct) / float(len(test_index))
			accuracies.append(accuracy)
		print m, mean(accuracies), stdev(accuracies)
main()
