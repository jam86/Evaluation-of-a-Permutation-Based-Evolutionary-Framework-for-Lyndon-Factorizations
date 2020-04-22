#!/bin/python3

# Compute the lyndon factors for the ordering from the output of the
# modified duvals and with an ordering based on the freq of each char
# sorted in reverse and an ordering based on the freq of each char in
# a protein sorted in reverse

import sys
import csv
from os import path
import collections
import subprocess
from multiprocessing import Pool as ThreadPool, cpu_count

if len(sys.argv) < 6:
	print("Usage: %s [genome char counts] [genomesOrderingDuvals.csv] [genome directory] [DuvalsModifiedAlgorithm.jar] [output file]" % (sys.argv[0]))
	exit()

genomeCharCounts = {}
proteinCharCountsPerGenome = {}
with open(sys.argv[1], "r") as csvf:
	reader = csv.reader(csvf, delimiter=',')
	alphabet = next(reader)[2:]
	for line in reader:
		if line[0] not in genomeCharCounts.keys():
			genomeCharCounts[line[0]] = {}
			proteinCharCountsPerGenome[line[0]] = {}
		if line[1].strip() not in proteinCharCountsPerGenome[line[0]].keys():
			proteinCharCountsPerGenome[line[0]][line[1].strip()] = {}
		
		index = 0
		for key in alphabet:
			if key not in genomeCharCounts[line[0]].keys():
				genomeCharCounts[line[0]][key] = 0
			if key not in proteinCharCountsPerGenome[line[0]][line[1].strip()].keys():
				proteinCharCountsPerGenome[line[0]][line[1].strip()][key] = 0
			genomeCharCounts[line[0]][key] += int(line[index + 2])
			proteinCharCountsPerGenome[line[0]][line[1].strip()][key] += int(line[index + 2])
			index += 1

freqOrderings = {}
for genome, counts in genomeCharCounts.items():
	sortedCounts = collections.OrderedDict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))
	ordering = ""
	for char, _ in sortedCounts.items():
		ordering += char
	freqOrderings[genome] = ordering
	
for genome, proteinData in proteinCharCountsPerGenome.items():
	for protein, counts in proteinData.items():
		sortedCounts = collections.OrderedDict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))
		ordering = ""
		for char, _ in sortedCounts.items():
			ordering += char
		proteinCharCountsPerGenome[genome][protein] = ordering

def compute(readerLine):
	cachedGenome = None
	readData = {}
	if readerLine[0] != cachedGenome:
		genomePath = path.join(sys.argv[3], readerLine[0] + "_protein.faa")
		f = None
		try:
			f = open(genomePath)
		except:
			genomePath = path.join(sys.argv[3], readerLine[0] + ".fna")
			f = open(genomePath)
		
		readBuffer = ""
		reading = False
		readData = {}
		proteinName = ""
		for line in f:
			if line.startswith(">"):
				if reading:
					readData[proteinName] = readBuffer
				else:
					reading = True
				readBuffer = ""
				proteinName = line[1:].strip()
			else:
				readBuffer += line
		readData[proteinName] = readBuffer

		f.close()
		cachedGenome = readerLine[0]

	if readerLine[1].strip() not in readData.keys() or readerLine[1].strip() not in proteinCharCountsPerGenome[readerLine[0]].keys():
		print(readerLine[1].strip() + " Missing from " + readerLine[0])
		return None
	else:
		proteinData = readData[readerLine[1].strip()]
		duvalsOrdering = readerLine[2]

		process = subprocess.Popen(["java", "-jar", sys.argv[4], "graph", duvalsOrdering, "/dev/stdin"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		process.stdin.write(proteinData.encode("utf-8"))
		process.stdin.close()
		process.wait()
		duvalsOrderingFactors = process.stdout.read().decode("utf-8").strip()

		process = subprocess.Popen(["java", "-jar", sys.argv[4], "order", freqOrderings[readerLine[0].strip()], "/dev/stdin"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		process.stdin.write(proteinData.encode("utf-8"))
		process.stdin.close()
		process.wait()
		genomeFreqOrderingFactors = process.stdout.read().decode("utf-8").strip()
		
		#print(proteinCharCountsPerGenome[readerLine[0]].keys())
		process = subprocess.Popen(["java", "-jar", sys.argv[4], "order", proteinCharCountsPerGenome[readerLine[0]][readerLine[1]], "/dev/stdin"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		process.stdin.write(proteinData.encode("utf-8"))
		process.stdin.close()
		process.wait()
		proteinFreqOrderingFactors = process.stdout.read().decode("utf-8").strip()

		return [readerLine[0].strip(), readerLine[1].strip(), duvalsOrdering, freqOrderings[readerLine[0].strip()], duvalsOrderingFactors, genomeFreqOrderingFactors, proteinCharCountsPerGenome[readerLine[0]][readerLine[1]], proteinFreqOrderingFactors]

with open(sys.argv[5], "w") as csvfw:
	writer = csv.writer(csvfw)
	writer.writerow(["genome", "protein", "duvals_ordering", "freq_genome_ordering", "duvals_ordering_factors", "freq_genome_ordering_factors", "protein_freq_ordering", "protein_freq_ordering_factors"])
	
	with open(sys.argv[2], "r") as csvf:
		reader = csv.reader(csvf, delimiter=',')
		next(reader)

		pool = ThreadPool(cpu_count())
		results = pool.map(compute, reader)	
		pool.close()
		pool.terminate()

		for result in results:
			if result != None:
				writer.writerow(result)
