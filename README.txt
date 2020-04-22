Evaluation of a Permutation-Based Evolutionary Framework for Lyndon Factorizations

This is the code repository for the paper (info).

We use data from NCBI RefSeq (https://www.ncbi.nlm.nih.gov/genome/browse#!/prokaryotes/) in amino acid format.
From the NCBI genome list, FTP URLs are shown to download the files. The amino acid format files end in "_protein.faa.gz".

Data we have produced using these genomes is inside of the directories containing the code which produced them.
The list of genomes we used for the testing of the minimisation of the number of Lyndon factors is in testingGenomeListForMinimizationOfNumberOfFactors.
The list of genomes we used for testing the balance fitness functions is in testingGenomesForBalanceFitnessFunctions.
The name of the genome we used for finding the mutation operator to use for the EA is in trainingGenome.

In our code, ModifiedDuvals was the working name of Flexi-Duval. Similarly, ModifiedDuvalsOperator refers to the LF-inspired operator.
