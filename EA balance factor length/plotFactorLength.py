#!/usr/bin/python3

import pickle
import matplotlib.pyplot as plt
import sys
from os import path
import numpy as np

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: %s [input data] [output plot directory] [SA? 0/1]" % (sys.argv[0]))
		exit()

experiments = [
	"Swap",
	"Swap (3)",
	"Scramble",
	"Scramble (3)",
	"Insertion",
	"Insertion (3)",
	"LF-inspired",
	"LF-inspired (3)",
	"Swap poisson",
	"Scramble poisson",
	"Insertion poisson",
	"LF-inspired poisson",
]

"""def mode(data):
	counts = {}
	for val in data:
		if val not in counts.keys():
			counts[val] = 0
		counts[val] += 1
	highestValue = 0
	highestKeys = []
	for k, v in counts.items():
		if v > highestValue:
			highestValue = v
			highestKeys = []
			highestKeys.append(k)
		elif v == highestValue:
			highestKeys.append(k)
	
	return highestKeys"""

def plot(dataPerExperiment):
	ending = ""
	if sys.argv[3] == "1":
		ending = " and SA"
	
	print("operator & max average & min average & average mean $\pm$ stdev")
	smallestDiffMaxMin = None
	smallestDiffMaxMinOperator = None
	for experiment, data in dataPerExperiment.items():
		# data is a list of list of int
		flatDataForPlot = []
		maxs = []
		mins = []
		#modes = []
		stdevs = []
		means = []
		for values in data:
			if values == None:
				continue
			for value in values:
				if value != "":
					flatDataForPlot.append(int(value))
			maxs.append(max(values))
			mins.append(min(values))
			stdevs.append(np.std(values))
			means.append(np.mean(values))
			# we can't use mode since there are multiple most common
			#modes.append(mode(values))
		
		plt.hist(flatDataForPlot, bins="auto")
		plt.title("Histogram of " + experiments[int(experiment)] + " mutation ordering factor lengths " + ending)
		plt.ylabel("Count")
		plt.xlabel("Length of factors")
		plt.savefig(path.join(sys.argv[2], experiment + ".png"))
		plt.clf()
		
		#print("mean " + experiments[int(experiment)] + " %f, stdev %f" % (np.mean(data), np.std(data)))
		#print("max " + experiments[int(experiment)] + " %f / min %f" % (max(data), min(data)))
		#print("mode " + experiments[int(experiment)] + " %f" % mode(data))
		
		meanMax = np.mean(maxs)
		meanMin = np.mean(mins)
		diffMaxMin = meanMax - meanMin
		#print("diff max min is %f for %s" % (diffMaxMin, experiments[int(experiment)]))
		if smallestDiffMaxMin == None or diffMaxMin < smallestDiffMaxMin:
			smallestDiffMaxMin = diffMaxMin
			smallestDiffMaxMinOperator = experiments[int(experiment)]
		print("%s&%f&%f&%f $\pm$ %f\\\\" % (experiments[int(experiment)], meanMax, meanMin, np.mean(means), np.mean(stdevs)))
	print("smallest diff max min is %f for %s" % (smallestDiffMaxMin, smallestDiffMaxMinOperator))
	
data = pickle.load(open(sys.argv[1], "rb"))
plot(data)

