#!/usr/bin/env python
from __future__ import division
import sys
import re
import subprocess
import shutil
import glob
import os


sys.path+=['./DendroPy-3.12.0-py2.6.egg']
import dendropy



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
	errCount=0
	for r in xrange(reps):	#there are 100 files from each Ne	
		filename = "MySettings.txt"
		f=open(filename,'r')
		lines = f.readlines()
		f.close()
		f=open(filename,'w')
		for line in lines:
			match1 = re.search("(  theta:.*)", line)
			match2 = re.search("(  Ne.*)", line)
			theta=(4*float(Ne))
			if match1 is not None:
				line=line.replace(match1.group(1), "  theta: "+ str(theta))
			if match2 is not None:
				treeName = "  Ne{0}_t{1}_k{2}_rep{3}.tre".format(Ne,tRatio,k,r)
				#scale = 1/(4*float(Ne))
				scale = 1
				line=line.replace(match2.group(1), treeName+":" + " " + str(scale) )
				#print "match.group(1) is " + match.group(1) + " should be replaced with " + str(treeName) 
			f.write(line)
			
		f.close()
	
		# To run STEM command line
		subprocess.call("java -jar stem.jar MySettings.txt", shell=True)
		try:
			if isSpTreeCorrect("search.tre"):
				goodCount = goodCount+1
			else:
				badCount+=1
			
			shutil.move("search.tre", "Ne{0}_t{1}_k{2}_rep{3}.search".format(Ne,tRatio,k,r))
			
		except IOError:
			errCount+=1
		
		
	print("Good: {0} Bad: {1}".format(goodCount, badCount))
	return goodCount, badCount, errCount
		
if __name__== '__main__':
	try:
		#Do all tRatios, Then select another Ne do all tRatios, Once all Ne's are done pick new K
		tRatio = sys.argv[1]							# np.linspace(.1,.9,9)
		Ne = sys.argv[2]								#1000.0, 10000.0,100000.0, or 1000000.0
		k = sys.argv[3]									# k is the number of trees to extract
	except:
		print "Error choosing k, n, or tRatio"

	subprocess.call("tar -xzf *.tar.gz", shell=True)
	reps=100
	#####T1 set to 100,000#####
	#Produce file with name of matrix cell
	gcount, bcount, ecount = runStem(k,Ne,tRatio,reps)
	try:
		cell=(gcount*100)/(gcount+bcount)
	except ZeroDivisionError:
		cell=-1		#no .search file was successfully parsed
		
	#print cell
	Nefile = "k" + str(k) + "_Ne" + str(Ne) + "_tRatio" + str(tRatio) + ".txt"
	f=open(Nefile, 'w')
	f.write(str(int(cell)))
	f.close()
	
	if ecount>0:
		errfile = "k" + str(k) + "_Ne" + str(Ne) + "_tRatio" + str(tRatio) + ".err"
		e=open(errfile, 'w')
		e.write(str(int(ecount)))
		e.close()
	
	searchFiles = "StemSearchTrees_" + "Ne{0}_t{1}_k{2}.tgz".format(Ne,tRatio,k)
	subprocess.call("tar -czf " + searchFiles + " *.search", shell=True)
	rmFiles = glob.glob("*.search") + glob.glob("*.tre")
	for rmFile in rmFiles:			#remove all .search files (since they are in tar.gz) and .tre files 
		os.remove(rmFile)

##########Note###############
# Running the program with Run=1
# produces a file called boot.tre with the best tree
# Running the program with Run=2
# produces a file called search.tre with the best trees and their liklihoods
# This takes on the order of 100 times longer for STEM to run.
#############################


