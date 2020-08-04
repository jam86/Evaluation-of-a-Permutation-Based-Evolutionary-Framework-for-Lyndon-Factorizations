Evaluation of a Permutation-Based Evolutionary Framework for Lyndon Factorizations
[![DOI](https://zenodo.org/badge/3896389)](https://zenodo.org/badge/latestdoi/3896389)

This is the code repository for the paper (DOI and conference link to come).

We use data from NCBI RefSeq (see prokaryotes.csv) in amino acid format.
From the NCBI genome list, FTP URLs are shown to download the files. The amino acid format files end in "_protein.faa.gz".

Data is available at http://hdl.handle.net/2160/b51cb7f3-63b3-4634-8b45-a8dc458444b4.
The list of genomes we used for the testing of the minimisation of the number of Lyndon factors and balancing the length of Lyndon factors is in testingGenomeList.
The name of the genome we used for finding the mutation operator to use for the EA is in trainingGenome.

In our code, ModifiedDuvals was the working name of Flexi-Duval. Similarly, ModifiedDuvalsOperator refers to the LF-inspired operator.

NCBI have reduced the number of reference genomes https://ncbiinsights.ncbi.nlm.nih.gov/2020/02/14/assembly-changes/.
