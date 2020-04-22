#!/usr/bin/python3

import pickle
import matplotlib.pyplot as plt
import sys
from os import path
import numpy as np
from statistics import mode

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

def plot(dataPerExperiment):
	ending = ""
	if sys.argv[3] == "1":
		ending = " and SA"
	
	print("operator & max & min & mode & mean +- stdev")
	for experiment, data in dataPerExperiment.items():
		plt.hist(data, bins="auto")
		plt.title("Histogram of " + experiments[int(experiment)] + " mutation ordering factor counts " + ending)
		plt.ylabel("Count")
		plt.xlabel("Number of factors")
		plt.savefig(path.join(sys.argv[2], experiment + ".png"))
		plt.clf()
		
		#print("mean " + experiments[int(experiment)] + " %f, stdev %f" % (np.mean(data), np.std(data)))
		#print("max " + experiments[int(experiment)] + " %f / min %f" % (max(data), min(data)))
		#print("mode " + experiments[int(experiment)] + " %f" % mode(data))
		
		print("%s&%d&%d&%d&%f $\pm$ %f\\\\" % (experiments[int(experiment)], max(data), min(data), mode(data), np.mean(data), np.std(data)))
		

data = pickle.load(open(sys.argv[1], "rb"))
plot(data)
