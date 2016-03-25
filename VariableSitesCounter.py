#Alisha Rossi
#Fall 2012
import glob
import numpy

####### PUT THIS IN A T FOLDER TO RUN ####

#function opens a file, looks at three sequences on a per nuc. basis
# returns: 
# 1) the number of invariable sites 
# 2) number of sites with 2 differences
# 3) number of sites with 3 differences 
# 4) sites w/correct split (A and B same)
# 5) sites with incorrect split (#2-#4)


def VarSiteCount(filename):
	try:
		f=open(filename, 'r')
		lines=f.readlines()	
		seqA=lines[1].strip()
		seqB=lines[4].strip()
		seqC=lines[7].strip()
		f.close()
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	except ValueError:
		print "Could not convert data to an integer."
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

	invCount=0
	twoDiffCount=0
	threeDiffCount=0
	corrSplitCount=0

	# go site by site through the three sequences
	for nucA,nucB,nucC in zip(seqA,seqB,seqC):
		if nucA==nucB:
			if nucB==nucC: 				# GGG, All three same 
				invCount+=1
			else:						# GGT, correct split 
				twoDiffCount+=1
				corrSplitCount+=1
		else:							# nucA!=nucB
			if nucA==nucC:				# GTG, incorrect split
				twoDiffCount+=1
			else:
				if nucB==nucC: 			# GTT, incorrect split
					twoDiffCount+=1
				else: 					# AGT, All three diff
					threeDiffCount+=1
	return invCount, twoDiffCount, threeDiffCount, corrSplitCount, twoDiffCount-corrSplitCount


if __name__== '__main__':
	Tsplit =  numpy.linspace(.1,.9,9)		# T2
	rateA = numpy.logspace(-4,0,5)			# .0001 to 1
	rateA=numpy.insert(rateA,0,0)
	Ne = numpy.logspace(3,6,4) 				#1000, 10000,100000,1000000
	
	for n in Ne:
		# create a 9x5 matrix for each thing we are counting
		invCount=numpy.zeros((Tsplit.size, rateA.size)) 
		twoDiffCount=numpy.zeros((Tsplit.size, rateA.size))
		threeDiffCount=numpy.zeros((Tsplit.size, rateA.size))
		corrSplitCount=numpy.zeros((Tsplit.size, rateA.size))
		incorrSplitCount=numpy.zeros((Tsplit.size, rateA.size))
		
		#loop over t-split and mutation rate and take sum
		#loop over Ne = 1000000
		
		for row,tsplit in enumerate(Tsplit):
			for col,rate in enumerate(rateA): 
				filenames = glob.glob('DNA_' + str(n) + '_' + str(tsplit) + '_' + str(rate) + '_*.fsa')
				for filename in filenames:
					invFileCount, twoDiffFileCount, threeDiffFileCount, corrSplitFileCount, incorrSplitFileCount = VarSiteCount(filename)	
					#average all 21 
					invCount[row][col]+=invFileCount
					twoDiffCount[row][col]+=twoDiffFileCount
					threeDiffCount[row][col]+=threeDiffFileCount
					corrSplitCount[row][col]+=corrSplitFileCount
					incorrSplitCount[row][col]+=incorrSplitFileCount
					
		numpy.savetxt("counts/invCount_" + str(n) +".txt", invCount/500,fmt="%i") #500: divide by 100 genes, divide by 500, multiply by 100 and truncate 
		numpy.savetxt("counts/twoDiffCount_" + str(n) +".txt", twoDiffCount/500,fmt="%i") #turn to int
		numpy.savetxt("counts/threeDiffCount_" + str(n) +".txt", threeDiffCount/500, fmt="%i")
		numpy.savetxt("counts/corrSplitCount_" + str(n) +".txt", corrSplitCount/500, fmt="%i")
		numpy.savetxt("counts/incorrSplitCount_" + str(n) +".txt", incorrSplitCount/500,fmt="%i")
		
		
	