Build LyndonFactorIndividualMutation.jar from "LyndonFactorisationIndividualMutation"

Run:
python3 gatherData.py [path/to/LyndonFactorisationIndividualMutation.jar] [path/to/genomes/as/faa] [output csv.gz] 0 [max min fitness (0) or stdev fitness (1)]

Run:
python3 processOverTime.py [output of gatherData.py] [output.processedOverTime.dat]
python3 plotOverTime.py [output of processOverTime.py] [output/plot/directory] 0

Run:
python3 processFactorLength.py [output of gatherData.py] [output.processedLength.dat]
python3 plotFactorLength.py [output of processFactorLength.py] [output/plot/directory] 0

Data is from "data.tar.xz/EA balance factor length"
