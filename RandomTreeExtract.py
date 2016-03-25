from __future__ import division
import numpy as np
import random
import dendropy
import glob
import sys
import os


#try:
#	k = sys.argv[1]									# k is the number of trees to extract
	#reps = sys.argv[2]								# reps is the number of times to extract k trees
#except:
#	k=64 #K is the number of trees to extract
#	print "64 trees will be chosen randomly 100 times"

def getTrees(k=2, reps=100, randNums):
	tRatio=np.linspace(.1,.9,9)
	Ne = np.logspace(3,6,4) 						# 1000.0, 10000.0,100000.0,1000000.0
	#randNums = np.random.random_integers(1,99,k)	# Picks k random numbers between 1 and 99 with replacement
	
	#T1 = np.logspace(0,6,7)						# 1.0 to 1 million
	t1=100000.0
	
	
	K= [2,4,8,16,32,64]
	for k in K:
		for r in xrange(reps):	#make 100 files
			# go into each T1 directory
			# for t1 in T1:								# Loop over files T1_1 to T1_1000000
				# or set T1 to a value. We use just 100,000
			#get all trees with the same Ne
			for n in Ne:
				for row,t in enumerate(tRatio):			#Get k trees from each tRatio
					treeVector = []
					#treefile= "Tree_" + str(n) + "_" +  str(t) + "_" + str(i) + ".nwk"
					for i in randNums:
						filename = "T1_"+str(t1)+"/Tree_" + str(n) + "_" +  str(t) + "_" + str(i) + ".nwk"
						#print "T1_"+str(t1)+"/Tree_" + str(n) + "_" +  str(t) + "*" + str(i) + ".nwk"
						#print "filenames are " + str(filenames) 
						fin=open(filename,'r')
						line=fin.readline()
						line=line.replace("[&R]","")	# reformat rate multiplier for STEM
						line=line.replace("'","")
						line=line.replace(":0.0;",";")	# Remove the 0.0 branch length at the end
						treeVector.append(line)
						fin.close()
						#save the k trees into a file
					
					try:
						treeDirectory = "RandomlyChosenTrees_T1_100k/"
						os.mkdir(treeDirectory)
					except OSError:
						pass #directory already exists
					treeFileOut = treeDirectory + "Ne" + str(n) + "_t" + str(t) +  "_k" + str(k) + "_rep" +  str(r) + ".tre"
					fout=open(treeFileOut, 'w')
					fout.writelines(treeVector)
					fout.close()
			
			
			#with open(filename) as f: # automatically closes input file as soon as it's done
			#	fileData=f.readlines()

		
if __name__== '__main__':

	#K= [2,4,8,16,32,64]
	randNums = random.random_integers(0, 100, 126)		# Picks k random numbers between 1 and 99 with replacement
	getTrees(100, randNums)		#reps=100

	#for k in K:
		#getTrees(k, 100, randNums)		#reps=100