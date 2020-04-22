#!/bin/python3

import sys
import csv
from os import listdir, path
import subprocess
from multiprocessing import Pool as ThreadPool
import re

if len(sys.argv) < 3:
	print("Usage: %s [path to genomes] [output file csv]" % (sys.argv[0]))
	exit()

def getOrdering(inputFile):
	genomePath = path.join(sys.argv[1], inputFile)
	process = subprocess.Popen(["java", "-jar", "DuvalsFactoring.jar", genomePath], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdoutdata, stderrdata = process.communicate()
	orderingDataList = stdoutdata.decode("utf-8").strip().split("\n")
	
	returnData = []
	for orderingData in orderingDataList:
		output = orderingData.split("\0")
		proteinName = output[0]
		factors = output[1]
		returnData.append([path.splitext(path.basename(inputFile))[0].replace("_protein", ""), proteinName, factors, -1])
	
	return returnData

with open(sys.argv[2], "w") as csvf:
	writer = csv.writer(csvf)
	writer.writerow(["genome", "protein", "factors", "eggnog_category"])
	
	files = []
	for f in listdir(sys.argv[1]):
		if not f.endswith(".gz"):
			files.append(f)
	pool = ThreadPool(12)
	results = pool.map(getOrdering, files)	
	pool.close()
	pool.terminate()

	for resultList in results:
		for result in resultList:
			writer.writerow(result)
