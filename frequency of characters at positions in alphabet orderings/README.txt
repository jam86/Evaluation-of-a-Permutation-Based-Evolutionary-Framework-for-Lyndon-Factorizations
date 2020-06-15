Plot orderings found from DFS in flexi-duval (modified duval) orderings
with the points proportional to the freq of characters in the whole
genome.

Need data for char counts for genomes and inverse freq amino acid freq
orderings (genome and protein) to run.

Plot output is named after the column in the inverse freq data file
Col 2 is mod duval, 3 is protein and 6 is genome

Run computeLyndonFactorsForInverseFreqAndModifiedDuvals.py from "comparison of lyndon factor lengths"
Run countCharsInGenomes.py from "count characters in genomes"

Run:
python3 analysis\ by\ char.py [output of computeLyndonFactorsForInverseFreqAndModifiedDuvals.py] [output of countCharsInGenomes.py] [basename of output plots]


Running "analysis by char.py" requires seaborn version 0.9.0, using version 0.10.0 will error. Matplotlib was 3.1.2 when testing.

Data:
inverseFreqAndModifiedDuvalsFactors.csv, testingGenomeCharCounts.csv
from "data.tar.xz/comparison of lyndon factor lengths"
