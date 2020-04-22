#!/usr/bin/python3

import pickle
import matplotlib.pyplot as plt
import sys
from os import path

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
	"Modified duvals",
	"Modified duvals (3)",
	"Swap poisson",
	"Scramble poisson",
	"Insertion poisson",
	"Modified poisson",
]

def plot(dataPerExperiment):
	valuesFiltered = []
	for _,x in dataPerExperiment.items():
		for x2 in x[0]:
			if x2 < 3000:
				valuesFiltered.append(x2)
	
	ylim = (min([min(x[0]) for _,x in dataPerExperiment.items()]),
		max(valuesFiltered))
	print(ylim)
	
	for experiment, data in dataPerExperiment.items():
		averages, stdevs = data
		plt.errorbar(range(len(averages)), averages)#, yerr=stdevs, ecolor="red")
		plt.ylim(ylim)
		plt.xlabel("Iteration")
		plt.ylabel("Average fitness for all proteins for a single genome")
		ending = ""
		if sys.argv[3] == "1":
			ending = " and SA"
		plt.title("Average fitness over time for a single genome with a single individual\nand " + experiments[int(experiment)] + " mutation" + ending)
		plt.savefig(path.join(sys.argv[2], experiment + ".png"))
		plt.clf()

data = pickle.load(open(sys.argv[1], "rb"))
plot(data)
