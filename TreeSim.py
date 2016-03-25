#! /usr/bin/env python 
#Modified from from https://groups.google.com/forum/#!msg/dendropy-users/yWjmR34ENF4/uhHij1VJnH8J

import numpy as np
import dendropy 
from dendropy import treesim 
from dendropy import seqsim 

def TreeSim(Ne, T1, T2):
	# read the species tree 
	sp_tree = dendropy.Tree.get_from_string("[&R] ((A:{0}, B:{0}):{1},C:{2});".format(T2,T1-T2,T1), "newick") 
	
	# set the number of individuals sampled from each species 
	for leaf in sp_tree.leaf_iter(): 
		leaf.num_genes = 1 # actually number of alleles sampled per species 
	
	# if the branch lengths are NOT in coalescent units 
	#  we will need to set the population sizes of the edges 
	
	for edge in sp_tree.postorder_edge_iter(): 
		#edge.pop_size = 1.0 # 1.0 => branch lengths in coalescent units 
		edge.pop_size = Ne # loop over 1000, 10000,100000,1000000
	
	# Simulate a gene tree within the species tree. 
	# `gene_tree` will be the constrained/censored/truncated gene tree 
	# `mapped_sp_tree` is a *clone* of the original input species tree, 
	# but with the gene tree nodes as attributes of its nodes, so you can see where on the species tree they coalesce etc. 
	gene_tree, mapped_sp_tree = treesim.constrained_kingman(sp_tree) 
	
	# show it! 
	#print(gene_tree.as_string("newick")) 
	#print(gene_tree.as_ascii_plot()) 
	return gene_tree
	
def DNAsim(sitesNum, gene_tree, rateA):	
	# simulate sequences 
	dna = seqsim.generate_hky_characters( 	# check for same as JC
			seq_len=sitesNum, 				# 500
			tree_model=gene_tree, 
			mutation_rate=rateA, 			# 0.0001 to 1
			kappa=1.0, 
			base_freqs=[0.25, 0.25, 0.25, 0.25]) 
	
	# show sequences 
	# can also be saved with: `dna.write_to_path()` 
	#print(dna.as_string("fasta")) 
	return dna
	
if __name__ == '__main__':
	
	geneNum = 100							# Number of genes
	Ne = np.logspace(3,6,4) 				# 1000, 10000,100000,1000000
	Tsplit =  np.linspace(.1,.9,9)			# T2/T1
	rateA = np.logspace(-4,0,5)				# .0001 to 1
	#rateA.append(0)
	rateA = np.insert(rateA,0,0)			# adds in the zero rate
	T1 = np.logspace(0,6,7)					# 1000000
	
	for t1 in T1:
		for n in Ne:
			for tRatio in Tsplit:
				for i in range(geneNum):
					GeneTree = TreeSim(n, t1, tRatio*t1)
					treefile= "T1_"+str(t1)+"/Tree_" + str(n) + "_" +  str(tRatio) + "_" + str(i) + ".nwk"
					f=open(treefile, 'w')
					f.write(GeneTree.as_string("newick"))
					f.close()
					for rate in rateA:		# Only the DNA sequences actually use the mutation rate
						DNA = DNAsim(500, GeneTree, rate)
						sequencefile= "T1_"+str(t1)+"/DNA_" + str(n) + "_" +  str(tRatio) + "_" + str(rate) + "_" + str(i) + ".fsa"
						f=open(sequencefile, 'w')
						f.write(DNA.as_string("fasta"))
						f.close()
					print str(treefile) + " created"
					
					
# dendropy assumes species tree is in generations 
# because we are setting the population size to Ne on the edges
# the final gene tree produced is in coalescent units
# Is T1 really supposed to be in generations?			
