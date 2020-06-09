#!/usr/bin/python3

import sys
import csv
import numpy as np
from statistics import mode

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: %s [input data]" % (sys.argv[0]))
		exit()

factorCounts = []
with open(sys.argv[1], "r") as f:
	# genome,protein,factors
	csv.field_size_limit(sys.maxsize)
	reader = csv.reader(f)
	next(reader)
	for line in reader:
		factorCounts.append(len(line[2][1:-1].split(", ")))
print("%s&%d&%d&%d&%f $\pm$ %f\\\\" % ("Duval's", max(factorCounts), min(factorCounts), mode(factorCounts), np.mean(factorCounts), np.std(factorCounts)))
