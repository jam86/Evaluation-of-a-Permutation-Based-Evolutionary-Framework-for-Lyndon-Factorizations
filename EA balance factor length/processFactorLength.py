#!/usr/bin/python3

import sys
import gzip
import csv
import numpy as np
import pickle
import re
import itertools

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: %s [input data gz] [output processed file]" % (sys.argv[0]))
		exit()

def cast(l, f):
	for i in range(len(l)):
		if l[i] == '' or l[i] == None:
			l[i] = None
		else:
			l[i] = f(l[i])
	
	return l

bestValuesPerExperiment = {}
with open(sys.argv[1], "rb") as f:
	with gzip.open(f, "rt") as g:
		# genome,protein,experiment,diffData,fitnessData,factorLengths
		csv.field_size_limit(sys.maxsize)
		reader = csv.reader(g)
		next(reader)
		for line in reader:
			if line[2] not in bestValuesPerExperiment.keys():
				bestValuesPerExperiment[line[2]] = []
			
			# we need to store the factor lengths instead of the best 
			# values but still for the best fitness so we cant just
			# use min here
			if line[4] == "[]":
				# there are some problems with missing values
				print("Missing value for fitness data for " + line[0] + " and " + line[1])
				continue
			
			values = itertools.zip_longest([float(x) for x in line[4].replace("[", "").replace("]", "").split(", ")],
				[cast(x.split(", "), int) for x in re.findall(r"\[((?:\d*(?:, )?)+)\]", line[5])])
			bestValue = None
			bestLengths = None
			for value, lengths in values:
				if (bestValue == None or value < bestValue) and lengths[0] != None:
					bestValue = value
					bestLengths = lengths
			
			bestValuesPerExperiment[line[2]].append(bestLengths)

pickle.dump(bestValuesPerExperiment, open(sys.argv[2], "wb"))
