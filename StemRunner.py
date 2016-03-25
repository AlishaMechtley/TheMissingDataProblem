from __future__ import division
import numpy as np
import sys
import re
import subprocess
import dendropy

#try:
#	k = sys.argv[1]									# k is the number of trees to extract
#except:
#	k=2 #K is the number of trees
#	print "Files with 2 trees will be chosen"


#######################################
# To Run STEM 2.0 on each file, ex. Ne_1000.0t_0.1k_2.tre
# Replace the following part of MySettings.txt
# files:
#   TreeNameHere.tre: 1.00
# with the name of the next tree
# files:
#   Ne_1000.0t_0.1k_2.tre: 1.00
#######################################


def isSpTreeCorrect(filename):

		# tree = dendropy.Tree.get_from_string("[&R] ((B, C), A);", "newick")
		tree = dendropy.Tree.get_from_path(filename, 'newick')
		node=tree.find_node_with_taxon_label("Species1").sister_nodes()[0].get_node_str()
		if node == "Species2":
			return True
		else:
			return False

def runStem(k, Ne, tRatio, reps):
	goodCount=0
	badCount=0
	for r in xrange(reps):	#there are 100 files from each Ne	
		filename = "MySettings.txt"
		f=open(filename,'r')
		lines = f.readlines()
		f.close()
		f=open(filename,'w')
		for line in lines:
			#if line.strip().startswith("Ne_"): 
			#	line.replace("Ne_*", "Ne_" +  str(n) + "t_" + str(t) + "k_" + str(k) + ".tre")	# reformat rate multiplier for STEM?
			match = re.search("(Ne_.*)", line)
			if match is not None:
				treeName = "Ne_{0}t_{1}k_{2}reps_{3}.tre".format(Ne,tRatio,k,r)
				line=line.replace(match.group(1), treeName+": 0.00001" )
				print "match.group(1) is " + match.group(1) + " is replaced with "
				print treeName
			f.write(line)
		f.close()
	
		# To run STEM command line
		subprocess.call("java -jar stem.jar MySettings.txt", shell=True)
		
		if isSpTreeCorrect("boot.tre"):
			goodCount = goodCount+1
		else:
			badCount+=1
	print("Good: {0} Bad: {1}".format(goodCount, badCount))
	return goodCount, badCount
		
if __name__== '__main__':
	Ne = np.logspace(3,6,4) 						#1000.0, 10000.0,100000.0,1000000.0		
	tRatio=np.linspace(.1,.9,9)
	reps=100
	#####T1 set to 100,000#####
	K= [2,4,8,16,32,64]
	for k in K:
		matrix = np.zeros((tRatio.size, Ne.size))
		for col,n in enumerate(Ne):
			for row,t in enumerate(tRatio):			#Get the trees from each tRatio
				gcount, bcount = runStem(k,Ne,tRatio,reps)
				matrix[row,col] = (gcount*100)/(gcount+bcount)	
		#save matrix for this k
		Nefile = "k_" + str(k) + "T1_100000" + ".txt"
		f=np.savetxt(Nefile, matrix.astype(int), fmt='%d')

##########Note###############
# Running the program with Run=1
# produces a file called boot.tre with the best tree
# Running the program with Run=2
# produces a file called search.tre with the best trees and their liklihoods
#############################