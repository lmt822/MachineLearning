# Assuming your shell is bash, you can directly "source" this file.
# Otherwise, adjust the syntax to set environment variables CLASSPATH 
# and WEKADATA to the corresponding values.
# Argument: Path to data file 
#!/bin/bash
export CLASSPATH=/r/aiml/ml-software/weka-3-6-11/weka.jar:$CLASSPATH
export WEKADATA=$1
FILES=$1/*
#Get File names with feature no. stored in X
i=0
j=0
for f in $FILES
do
case $f in
	*train_norm.arff) 
		fname=`basename $f`
		TRAIN[i]=$fname
		X[i]=$(echo $fname | grep -o -E '[0-9]+' | head -1 | sed -e 's/^0\+//')
		let i+=1;;	
	*test_norm.arff) 
		fname=`basename $f`
		TEST[j]=$fname
		let j+=1;;
esac
done
i=0
#Assume the number of test is the same as the number of train data
#Get Accuracy in Y
for data in "${TRAIN[@]}"
do
ACCU[i]=$(java weka.classifiers.trees.J48 -t $WEKADATA/$data -T $WEKADATA/${TEST[i]} | grep "Correctly Classified Instances")
let i+=1
done
#process for Accuracy
i=0
for accu in "${ACCU[@]}"
do
Y[i]=$(echo $accu | cut -d " " -f 11)	
echo "${Y[i]}"
let i+=1
done
#Prepare data file to draw
i=0
for X in "${X[@]}"
do
echo "${X[i]}  ${Y[i]}"
let i+=1
done > weka_J48.txt
