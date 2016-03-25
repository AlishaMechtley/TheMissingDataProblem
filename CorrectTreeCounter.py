from __future__ import division
import numpy as np
import dendropy
import glob

# count the number of trees with the correct orientation: A with B and C apart 
# ((A,B),C)  or  (C,(A,B)) or  ((B,A),C) or (C,(B,A))
# symmetric_difference(other_tree) Returns the symmetric_distance or sum of splitsin one but not in both.

def getTreeCounts(T1, T, Ne):
	goodTreeCount=0
	badTreeCount=0
	
	filenames = glob.glob("T1_"+str(T1)+"/Tree_" + str(Ne) + "_" +  str(T) + "*.nwk")
	#filenames = glob.glob('*.nwk')
	
	for filename in filenames:
		# tree = dendropy.Tree.get_from_string("[&R] ((B, C), A);", "newick")
		tree = dendropy.Tree.get_from_path(filename, 'newick')
		node=tree.find_node_with_taxon_label("A_01").sister_nodes()[0].get_node_str()
		if node == "'B_01'":
			goodTreeCount+=1
			#print "good"
		else:
			badTreeCount+=1
			#print "bad"
	return goodTreeCount, badTreeCount
				


if __name__== '__main__':
	goodTreeCount=0
	badTreeCount=0
	tRatio=np.linspace(.1,.9,9)
	Ne = np.logspace(3,6,4) 				#1000, 10000,100000,1000000
	T1 = np.logspace(0,6,7)					# 1 to 1 million
	
	# Loop over files T1_1 to T1_1000000
	#once I'm in a file get all trees with the same Ne
	for n in Ne:
		matrix = np.zeros((tRatio.size, T1.size))
		for col,t1 in enumerate(T1):
			for row,t in enumerate(tRatio):
				print t1,t,n
				gcount, bcount = getTreeCounts(t1, t, n)
				# Make matrix of T1 vs T 
				matrix[row,col] = (gcount*100)/(gcount+bcount)
		#save matrix for this Ne
		Nefile = "Ne_" + str(n) + ".txt"
		f=np.savetxt(Nefile, matrix.astype(int), fmt='%d')

	
######### Meeting Notes ##############	
# find the number of times that the gene tree is correct for the species tree
# graph of T2 vs Ne, percent of times that gene tree matches species tree, 100 reps
# top left corner should be the best. Takes longer for higher Ne and T2

#If all are same, change T1 to something larger (like 1000) and then T2 accordingly (multiply by T1)

#(c,(a,b)) or (c,(b,a)) is correct tree

'''
% gene trees that match the species tree
separate Ne for each table
make a table with T1 vs T2/T1 and 
T1 1, 10, 100, 1000... 1mill
.1 to .9
'''
	
