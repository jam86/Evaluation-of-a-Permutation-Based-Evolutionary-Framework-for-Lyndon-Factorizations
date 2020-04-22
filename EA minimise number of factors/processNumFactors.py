#!/usr/bin/python3

import sys
import gzip
import csv
import numpy as np
import pickle

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: %s [input data gz] [output processed file]" % (sys.argv[0]))
		exit()

# we need to find the best fitness for each protein for each genome
bestValuesPerExperiment = {}
with open(sys.argv[1], "rb") as f:
	with gzip.open(f, "rt") as g:
		# genome,protein,experiment,diffData,fitnessData
		csv.field_size_limit(sys.maxsize)
		reader = csv.reader(g)
		next(reader)
		proteinVals = []
		currentExperiment = None
		for line in reader:
			if line[2] not in bestValuesPerExperiment.keys():
				bestValuesPerExperiment[line[2]] = []
			
			bestValue = min([float(x) for x in line[4].replace("[", "").replace("]", "").split(", ")])
			bestValuesPerExperiment[line[2]].append(bestValue)

pickle.dump(bestValuesPerExperiment, open(sys.argv[2], "wb"))
