# Mengtian Li
# test script for submission
import os
import subprocess
def main():
	d = [1,2,3,4,5]
	s = [0.1, 0.5, 1]
	pcpt_out = []
	KNN_out = []
	pcpt_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(1) +' additionalTraining.arff additionalTest.arff', shell=True))
	for num in d:
		pcpt_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(2) +' additionalTraining.arff additionalTest.arff 0 ' + str(num), shell=True))
	for num in s:
		pcpt_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(2) +' additionalTraining.arff additionalTest.arff 1 ' + str(num), shell=True))
	KNN_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(3) +' additionalTraining.arff additionalTest.arff', shell=True))
	for num in d:
		KNN_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(4) +' additionalTraining.arff additionalTest.arff 0 ' + str(num), shell=True))
	for num in s:
		KNN_out.append(subprocess.check_output('python Primal_pcpt.py ' + str(4) +' additionalTraining.arff additionalTest.arff 1 ' + str(num), shell=True))
	for element in KNN_out:
		element = element.rstrip('\n')
		print element,
	print ''
	for element in pcpt_out:
		element = element.rstrip('\n')
		print element,
main()