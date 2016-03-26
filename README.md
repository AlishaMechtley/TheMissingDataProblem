 Summary of Work on the Missing Data Problem
=============================================

## How To Run:

1) Place all the scripts in your space on the cluster

2) Run the Condor Submission Script using Condor.


## Summary of programs and results

This program was designed to find the area of parameter space that is going to be a problem for missing data. Because there is a lot of missing data in the mitochondrial genomes that I produce, I wanted to compare my missing data against the simulated results.

I chose Condor because it is essentially free for me to use in my department. A well known problem with condor is that it does not try to rerun a process when it fails. 
My analysis was no different. It resulted in a lot of cases where there are no results. This requires an additional program to find which ones failed (using glob or re over multiple files) and rerun those analyses.
I decided not write a program to do this because it would take too long to run such an anlysis. I am currently working on a way to do the analysis with ETE using Amazon Web services.
The goal is so to fill in the complete matrix in 20 minutes or less for only a slight monetary cost.

The results of the early Condor based implementation are as follows.


### Species and Gene Tree Simulation (TreeSim.Py)

Workflow of the simulation study can be generalized as follows: 
```
1) Generate species trees.
2) Generate gene trees from species trees. 
3) Generate sequence data from the gene trees.
4) Estimate the maximum likelihood gene trees from the sequence data, reconstruct the species trees from the estimated gene trees and compare to step 1. 
5) Repeat step 4 with missing data.
```
To simulate species trees, I gave DendroPy the species tree specifications in newick format: 

*(1:T2,  2:T2): T1-T2, 3:T1)*

where T1 ranges from 1 to 1,000,000 (e.g., 10000, 20000, ..., 90000,1000000) and T2 is calculated as T1 multiplied by a ratio for 9 different ratios, 0.1 through 0.9 (i.e., T2 = 10,000, 20,000, … , 90,000). 

To begin, I set the number of individuals sampled from each species to be 1 and the number of genes to be 1. The population size, Ne, is given in generations and varies exponentially with a base of 10 (Ne= 1000, 10000, 100000, 1000000). Then, I created a gene tree from the species tree using DendroPy’s constrained Kingman function.

The parameter space can be easily understood just by looking at the condorSubmissionScript. The parameter settings were generated with print statements in a terminal because there is really no excuse for typing anything more than 20 times if you are a programmer. ;)

### Counting Variable Sites (VariableSitesCounter.Py)

To begin, I first created matrices to determine a suitable range of population sizes to study where Ne designates effective population size. Then I looked for the following: 
```
1) number of invariable sites 
2) number of sites with 2 differences (including both correct and incorrect split)
3) number of sites with 3 differences 
4) sites w/correct split (A and B same)
5) sites with incorrect split (#2 - #4)
```

The results of the matrices of variable sites led us to decide that a T1-value of 100,000 was a good place to start for using condor. 

### Randomly Choosing Trees (RandomTreeExtract.py)

There are 100 trees simulated for each ratio (0.1 through 0.9). There are 2, 4, 8, 16, 32, and 64 trees randomly chosen from the 100 (with duplication) for each ratio (See RandomTreeExtract.py).

### STEM 
### (Single use: StemRunner.Py, StemMatrixResults.py, and CorrectTreeCounter.py) 
### (Running Parallel in Condor: CondorStemRunner.py, StemMatrixResults.py, and CondorTreeCounter.Py)

STEM is a program for inferring maximum likelihood species trees from a collection of estimated gene trees under the coalescent model using a simulated annealing algorithm. Trees must be rooted and satisfy a molecular clock. The parameter controlling the rate of cooling, beta, is specified in the settings ﬁle. Beta must be a number between 0 and 1. I chose 0.0005. Theta is the value of θ = 4Neµ to be used to make the correspondence between gene trees branch lengths and species tree branch lengths. I chose θ = 1.  According to Hommaller, Knowles, and Kubatko, 2013 (in press), This value affects the likelihood score but not the selection of the best ML trees. The STEM algorithm terminates when  a suﬃcient number of trees have been proposed from the current tree without any of them resulting in acceptance, or the search is alternating between a collection of high-likelihood trees that are separated from one another by a single rearrangement, and a suﬃcient number of iterations have passed since any alternative trees have been accepted.

The settings used are as follows

```
properties:
  run: 2           #0=user-tree, 1=MLE, 2=search
  theta: 1
  num_saved_trees: 15
  beta: 0.0005
  seed: 3435893
species:
  Species1: A_01
  Species2: B_01
  Species3: C_01
files:
  Ne1000.0_t0.1_k2_rep99.tre: 0.001
```
Note: Might Change number of saved trees to a larger number.)

To Run STEM 2.0 on a file (e.g., ```Ne_1000.0t_0.1k_2.tre```) the program StemRunner.py replaces part of MySettings.txt file (i.e., files: TreeNameHere.tre: 1.00) with the name of the next tree (files: Ne_1000.0t_0.1k_2.tre: 1.00). Running the program with Run=1 produces a file called boot.tre with the best tree.
Running the program with Run=2 produces a file called search.tre with the best trees and their likelihoods. This takes on the order of 100 times longer for STEM to run. I have used Run=2, but I still need to decide how to check if the tree is the likeliest or not (Use only the one with the highest ML score. What if there are two with the same score? What if the second highest score is the correct tree and it is very close to the highest score?

Note: Want to redo with two, four, and possibly 8.

### Results
Stem was run on all 100 reps of each parameter setting. 
The program opens each tree file and runs STEM then checks the output to see if it has the correct branching (species 1 and species 2 match).

Files like k2_Ne1000.0_tRatio0.1.txt contain a number

- 100 is 3 bytes
- -1 is 2 bytes and produces an err file (Stem crashed so it couldn’t get a count)
- 0 is 1 byte 

### Error
All the files in the error folder show up as 0 and look empty.

### Log 
Log files are all different, talk about how many times rerun before failed or successful
Question: Is there a way to reduce the size of the log files? Perhaps I'll tell stem not to output percentages.

### Output 
Output files contains the .out files which are either 265.2 or 0 MB. 

The matrices have the Ne values from left to right and the ratios from top to bottom (for example, the top left corner is the result of Ne=1000 and ratio=0.1).

The random tree selector did not select trees randomly (they are all the same) and will need to be fixed. Check for logic bug or rounding error.

