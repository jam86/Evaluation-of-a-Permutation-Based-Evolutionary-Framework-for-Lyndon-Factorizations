#!/bin/python3

# collect data for difference of fitness changes for mutation operators
# using a single individual

import sys
import subprocess
from multiprocessing import Pool as ThreadPool, cpu_count
import gzip
from os import listdir, path, unlink
import csv
import numpy as np
import pickle

def compute(inputData):
	_file, experiment = inputData
	
	process = subprocess.Popen(["java", "-jar", sys.argv[1], str(experiment), "0", "0", "0", "0", _file, "0", sys.argv[4], "1"], stdout=subprocess.PIPE)
	stdoutdata, stderrdata = process.communicate()
	gaFitnessOutput = stdoutdata.decode("utf-8").strip().split("\n")
	
	outputData = []
	proteinNumber = 0
	ys_diff = []
	ys_fitness = []
	xs = []
	x = 0
	reading = False
	
	readData = {}
	proteinName = ""
	for line in gaFitnessOutput:
		if line.startswith(">"):
			if reading:
				if proteinName not in readData.keys():
					readData[proteinName] = []
				readData[proteinName].append((ys_diff, ys_fitness, xs))
			else:
				reading = True
			ys_diff = []
			ys_fitness = []
			xs = []
			x = 0
			proteinName = line[1:].strip()
		else:
			split = line.split(":")
			ys_diff.append(abs(float(split[1])))
			ys_fitness.append(float(split[2]))
			xs.append(x)
			x += 1
	if proteinName not in readData.keys():
		readData[proteinName] = []
	readData[proteinName].append((ys_diff, ys_fitness, xs))

	#print(readData)

	pickle.dump((path.basename(_file).replace("_protein.faa", ""), experiment, readData), open(path.join("/tmp/", path.basename(_file).replace("_protein.faa", "")), "wb"))

	return path.basename(_file).replace("_protein.faa", "")

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage: %s [LyndonFactorisationIndividualMutation.jar] [genome directory] [output file] [use SA 1/0?]" % (sys.argv[0]))
		exit()
	
	experiments = [
		"Swap",
		"Swap 3",
		"Scramble",
		"Scramble 3",
		"Insertion",
		"Insertion 3",
		"Modified duvals",
		"Modified duvals 3",
		"Swap poisson",
		"Scramble poisson",
		"Insertion poisson",
		"Modified poisson",
	]
	
	files = [path.join(sys.argv[2], x) for x in listdir(sys.argv[2])]
	with open(sys.argv[3], "wb") as f:
		with gzip.open(f, 'wt') as g:
			writer = csv.writer(g)
			writer.writerow(["genome", "protein", "experiment", "diffData", "fitnessData"])
			
			for experiment in [5]:#range(len(experiments)):
				chunkSize = int(len(files)/12)
				if chunkSize < 1:
					chunkSize = 1
				chunks = np.array_split(files, chunkSize)
				for chunkFiles in chunks:
					pool = ThreadPool(cpu_count())
					resultFiles = pool.map(compute, zip(chunkFiles, [experiment] * len(chunkFiles)))
					pool.close()
					pool.terminate()
					for resultFile in resultFiles:
						result = pickle.load(open(path.join("/tmp", resultFile), "rb"))
						unlink(path.join("/tmp", resultFile))

						#for result in results:
						genome = result[0]
						experiment = result[1]
						for protein, proteinValues in result[2].items():
							for valueData in proteinValues:
								#print(valueData[0], valueData[1])
								writer.writerow([genome, protein, experiment, valueData[0], valueData[1]])
