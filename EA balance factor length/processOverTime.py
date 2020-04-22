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

data = {}
plottingGenome = None
with open(sys.argv[1], "rb") as f:
	with gzip.open(f, "rt") as g:
		# genome,protein,experiment,diffData,fitnessData
		csv.field_size_limit(sys.maxsize)
		reader = csv.reader(g)
		next(reader)
		for line in reader:
			if line[4] == "[]":
				# there are some problems with missing values
				print("Missing value for fitness data for " + line[0] + " and " + line[1])
				continue
			if plottingGenome == None:
				plottingGenome = line[0]
			if line[2] not in data.keys():
				data[line[2]] = []
			if line[0] == plottingGenome:
				data[line[2]].append([float(x) for x in line[4].replace("[", "").replace("]", "").split(", ")])

# there are many proteins per genome, we only want a single line to plot
# take avg and stdev at each point
averagedData = {}
for experiment, valuesPerProtein in data.items():
	averageData = []
	stdevData = []
	for i in range(max([len(x) for x in data[experiment]])):
		dataAcrossProteinsAtIndex = []
		for values in valuesPerProtein:
			if i < len(values):
				dataAcrossProteinsAtIndex.append(values[i])
		averageData.append(np.mean(dataAcrossProteinsAtIndex))
		stdevData.append(np.std(dataAcrossProteinsAtIndex))
	averagedData[experiment] = (averageData, stdevData)

pickle.dump(averagedData, open(sys.argv[2], "wb"))
