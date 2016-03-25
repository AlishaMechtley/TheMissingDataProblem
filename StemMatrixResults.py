
import numpy as np

#collect results of correctTreeCounter and store into a matrix.
	
	
def getMatrix(k):
	treeVector = []
	Ne = np.logspace(3,6,4) 						# 1000.0, 10000.0,100000.0,1000000.0
	tRatio = np.linspace(.1,.9,9)
	
	for t in tRatio:
		for n in Ne:

			#read cells, percent correct ML Trees
			Nefile = "k" + str(k) + "_Ne" + str(n) + "_tRatio" + str(t) + ".txt"
			try:
				f=open(Nefile, 'r')
				line = f.readline()
				f.close()
				#Store into vector
			except:
				line="nd"
			treeVector.append(line)

	#resize and print the matrix
	print "treeVector is " + str(treeVector)
	treeVector=np.array(treeVector)
	print "numpy treeVector is " + str(treeVector)
	print "treeVector.size is " + str(treeVector.size)
	treeVector.resize([9,4])
	print treeVector
	treeFileOut = "K_" + str(k) + ".txt"
	fout=open(treeFileOut, 'w')
	np.savetxt(fout, treeVector, delimiter='\t',fmt='%s')
	fout.close()
	
if __name__== '__main__':
	K= [2,4,8,16,32,64]
	
	#K=[2,4]
	for k in K:
		getMatrix(k)
		