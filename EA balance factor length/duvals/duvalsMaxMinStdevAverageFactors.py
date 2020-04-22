#!/usr/bin/python3

import sys
import csv
import numpy as np

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: %s [input data]" % (sys.argv[0]))
		exit()

maxs = []
mins = []
stdevs = []
with open(sys.argv[1], "r") as f:
	# genome,protein,factors
	csv.field_size_limit(sys.maxsize)
	reader = csv.reader(f)
	next(reader)
	for line in reader:
		values = [len(x) for x in line[2][1:-1].split(", ")]
		
		maxs.append(max(values))
		mins.append(min(values))
		stdevs.append(np.std(values))
	
	print("%s&%f&%f&%f\\\\" % ("Duval's", np.mean(maxs), np.mean(mins), np.mean(stdevs)))
