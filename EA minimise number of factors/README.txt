Compile LyndonFactorIndividualMutation.jar

Edit line 87 of gatherData.py to set the mutation operator

Run:
python3 gatherData.py [path/to/LyndonFactorisationIndividualMutation.jar] [path/to/genomes/as/faa/files] [output.csv.gz] 0
The number of iterations is set in LyndonFactorIndividualMutation in Application.java at compile time

Run:
python3 processOverTime.py [output of gatherData.py] [output.processed.dat]
python3 plotOverTime.py [output of processOverTime.py] [path/to/plot/directory] 0

Run:
python3 processNumFactors.py [output of gatherData.py] [output.processed.dat]
python3 plotNumFactors.py [output of processNumFactors.py] [path/to/plot/directory] 0

The data we used for the paper is in /data. Processed data is in /numFactors and /overTime
