Build DuvalsModifiedAlgorithm.jar

Run countCharsInGenomes.py from the "count chars in genomes" directory
python3 countCharsInGenomes.py [directory of faa files] [output file.csv]

Run:
python3 computeLyndonFactorsForInverseFreqAndModifiedDuvals.py [genome char counts] [genome directory] [path/to/DuvalsModifiedAlgorithm.jar] [output file.csv]

Run calculateOrderingForGenomesDuvals.py from "duvals factoring"

Run:
python3 lyndonFactorComparisonAnalysis.py [output of computeLyndonFactorsForInverseFreqAndModifiedDuvals.py] 0 0 [output of calculateOrderingForGenomesDuvals.py] [output.csv] > [output.txt]
