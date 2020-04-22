#!/usr/bin/python3

import pickle
import sys
import numpy as np
from scipy.stats import ks_2samp

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: %s [max min diff dat] [stdev dat]" % (sys.argv[0]))
		exit()

def plot(dataPerExperiment):
	smallestDiffMaxMin = None
	smallestDiffMaxMinOperator = None
	for experiment, data in dataPerExperiment.items():
		# data is a list of list of int
		flatDataForPlot = []
		maxs = []
		mins = []
		#modes = []
		stdevs = []
		for values in data:
			if values == None:
				continue
			for value in values:
				if value != "":
					flatDataForPlot.append(int(value))
			maxs.append(max(values))
			mins.append(min(values))
			stdevs.append(np.std(values))
			# we can't use mode since there are multiple most common
			#modes.append(mode(values))	
	
	return stdevs
	
maxmindata = pickle.load(open(sys.argv[1], "rb"))
stdevdata = pickle.load(open(sys.argv[2], "rb"))
maxminstdevs = plot(maxmindata)
stdevstdevs = plot(stdevdata)

confidence = 0.05
ks = ks_2samp(maxminstdevs, stdevstdevs)
# H0 - there is no significant difference between max min diff and stdev fitness stdevs for each protein
print("max min diff - stdev: stdevs ks: %f" % (ks[1]))
if ks[1] < confidence:
	print("significant")
else:
	print("not significant")
