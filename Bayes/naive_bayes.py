# Mengtian Li
# Comp135 a2
# Oct 10 2015
# Naive_bayes.py
import sys
import os
import re
import math
from operator import itemgetter

# read index from file
def read_index(file_path, index_list):
	with open(file_path) as f:
		for line in f:
			index_list.append(int(line))

# Read CLEAN files from given data_path and given index, if the
# index matches the training or test index given, then stores
# the content of each file to a file_list. Each index correspond to 
# the file name. 
def read_files(data_path, training_index, test_index):
	file_list = [None] * int(len(os.listdir(data_path)))	
	for entry in os.listdir(data_path):
		if entry.endswith("clean"):
			index = int(re.findall('\d+',entry)[0])
			if (index in training_index) or (index in test_index):
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
def calculate_prob(token_freq, token_count):
	for element in token_freq:
		element[1] = float(element[1]) / float(token_count)

# input file should include a file that specifies the index
# for training set.(Assume all in boundry)
# argument list:
# 1: path to data files
# 2: training index file
# 3: test index file
def main():
	# Read from file
	# list with data inside and each index correspond to the number of clean files
	# only read in files that is specified in the second argument
	data_files = []
	# list with training data specified by training index list and each index correspond to 
	# the number of clean files
	training_data = []
	# similar as training data
	test_data = []
	# training index that are specified by argument
	training_index = []
	# similar as training index
	test_index = []
	# text file with positive index read from index.full or index.short
	positive_index = []
	# similar as positive index
	negative_index = []
	# Parsed token list that has positive labels in training file
	positive_token_list = []
	# similar to positive token list
	negative_token_list = []
	# each element is a vector of the token and its frequency(probabililty)
	positive_token_freq = []
	# similar to negative token list
	negative_token_freq = []
	# test score to hold the text name, positive score, negative score as vector
	test_score = []
	read_index(sys.argv[2], training_index)
	read_index(sys.argv[3], test_index)
	data_files = read_files(sys.argv[1], training_index, test_index)
	# split training and test data
	training_data = split_data(data_files, training_index)
	test_data = split_data(data_files, test_index)
	# short or full
	read_class(sys.argv[1], positive_index, negative_index, "index.short")
	# parse training data
	parse_tokens(training_data, positive_index, positive_token_list, training_index)
	parse_tokens(training_data, negative_index, negative_token_list, training_index)
	# Calculate the possiblity that positive and negative in training data
	training_size = len(positive_index) + len(negative_index)
	P_positive = float(len(positive_index)) / float(training_size)
	P_negative = float(len(negative_index)) / float(training_size)
	calculate_freq(positive_token_list, positive_token_freq)
	calculate_freq(negative_token_list, negative_token_freq)
	# token_size used to calculate vocab size
	p_token_size = calculate_freq(positive_token_list, positive_token_freq)
	n_token_size = calculate_freq(negative_token_list, negative_token_freq)
	calculate_prob(positive_token_freq, len(positive_token_list))
	calculate_prob(negative_token_freq, len(negative_token_list))	# calculate score for each test data
	for text in test_data:
		if text == None:
			continue
		else:
			temp_score = []
			temp_score.append(test_data.index(text))
			temp_text = text.split()
			# calculate positive score
			# Use the sum of log(P) to avoid underflow
			sum = math.log(P_positive)
			for token in temp_text:
				# check if a token has been seen in current class
				# if not seen in current class but seen in the other
				# record 0 count for that token
				check = 1
				for element in positive_token_freq:
					if element[0] == token:
						sum = sum + math.log(element[1])
						check = 0
						break
				if check:
					for element in negative_token_freq:
						if element[0] == token:
							sum = sum - float("inf")
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
					for element in positive_token_freq:
						if element[0] == token:
							sum = sum - float("inf")
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
	print accuracy
main()
