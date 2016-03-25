import numpy as np
import subprocess
import os

Ne = np.logspace(3,6,4)
Tsplit =  np.linspace(.1,.9,9)
K= [2,4,8,16,32,64]


jobNum = 0								# fileName.tgz starts with zero
treeDirectory =  "RandomlyChosenTrees_T1_100k/"
os.chdir(treeDirectory)

for k in K:
	for n in Ne:
		for t in Tsplit:
					#There are 6*4*9 = 216 args to be run, each using a separate zipped input file
					#Take files from 0 to 99 for each parameter set and zip them together in files 1.zip to 215.zip
					
					treefile= "Ne" + str(n) + "_t" + str(t) +  "_k" + str(k) + "_rep*.tre"
					command= "tar -czf " + str(jobNum) + ".tar.gz " + treefile
					subprocess.call(command, shell=True)
					jobNum+=1
					
					#print "arguments = " + str(tRatio) + " " + str(n) + " " + str(k)
					#print "queue"
					
os.chdir("../..")