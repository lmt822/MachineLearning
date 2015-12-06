# Mengtian Li
# python run script for a4 experiment
# Dec 1, 2015
# Output sequence: for each data set, Primal Perceptron, Kernel Perceptron with Polynomial, Kernel Perceptron 
# with RBF; Primal KNN, Kernel KNN with Polynomial, Kernel KNN with RBF
import os

def main():
	d = [1,2,3,4,5]
	s = [0.1, 0.5, 1]
	print 'A'
	os.system('python Primal_pcpt.py ' + str(1) +' data/ATrain.arff data/ATest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(2) +' data/ATrain.arff data/ATest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(2) +' data/ATrain.arff data/ATest.arff 1 ' + str(num))
	os.system('python Primal_pcpt.py ' + str(3) +' data/ATrain.arff data/ATest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(4) +' data/ATrain.arff data/ATest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(4) +' data/ATrain.arff data/ATest.arff 1 ' + str(num))
	
	print 'B'
	os.system('python Primal_pcpt.py ' + str(1) +' data/BTrain.arff data/BTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(2) +' data/BTrain.arff data/BTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(2) +' data/BTrain.arff data/BTest.arff 1 ' + str(num))
	os.system('python Primal_pcpt.py ' + str(3) +' data/BTrain.arff data/BTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(4) +' data/BTrain.arff data/BTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(4) +' data/BTrain.arff data/BTest.arff 1 ' + str(num))

	print 'back'
	os.system('python Primal_pcpt.py ' + str(1) +' data/backTrain.arff data/backTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(2) +' data/backTrain.arff data/backTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(2) +' data/backTrain.arff data/backTest.arff 1 ' + str(num))
	os.system('python Primal_pcpt.py ' + str(3) +' data/backTrain.arff data/backTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(4) +' data/backTrain.arff data/backTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(4) +' data/backTrain.arff data/backTest.arff 1 ' + str(num))

	print 'sonar'
	os.system('python Primal_pcpt.py ' + str(1) +' data/sonarTrain.arff data/sonarTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(2) +' data/sonarTrain.arff data/sonarTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(2) +' data/sonarTrain.arff data/sonarTest.arff 1 ' + str(num))
	os.system('python Primal_pcpt.py ' + str(3) +' data/sonarTrain.arff data/sonarTest.arff')
	for num in d:
		os.system('python Primal_pcpt.py ' + str(4) +' data/sonarTrain.arff data/sonarTest.arff 0 ' + str(num))
	for num in s:
		os.system('python Primal_pcpt.py ' + str(4) +' data/sonarTrain.arff data/sonarTest.arff 1 ' + str(num))
main()