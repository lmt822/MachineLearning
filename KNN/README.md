# COMP135
## KNN Implementation
### Mengtian Li
#### Sept. 28 2015

##### File names and how to run:
###### plot.sh
	sh plot.sh data_path
	/* Run the J48 algorithm to data files provided
	/* Generate weka_J48.txt file as data file to plot
###### gnuscript
	sh gnuscript
	/* By editing the code to change the data file names
	/* As well as graph titles etc. Generate conf file
	/* Run load 'conf' in GNU to generate the png
###### pyscript
	sh pyscript data_path
	/* By editing the code to set parameters, which
	/* algorithm to use, which output file to generate
	/* Run all data file in data_path and generate 	/* output files with accuracy
###### KNN.py
	/* Use pyscript to run
	/* Implementation of regular linear time KNN 	/* algorithm
###### KNN relief feature_selection.py
 	/* Use pyscript to run
	/* Implementation of feature selection relief
	/* algorithm

###### KNN relief weighted_dist.py
 	/* Use pyscript to run
	/* Implementation of weighted distance relief
	/* algorithm
###### mscript
	sh mscript
	/* Perform the experiment for m when m=100,...1000 for 94 features data
	/* Manually change the first column to 100,...1000
###### Report.doc
