#!/bin/python3

# Get a count for the characters used in each protein in a genome and store as a CSV for use in other programs

import sys
import csv
from os import path, chdir
import glob

if len(sys.argv) < 3:
	print("Usage: %s [directory containing fasta files] [output file]" % (sys.argv[0]))
	exit()

def getCount(data):
	counts = {}

	for char in data:
		if char not in counts.keys():
			counts[char] = 0
		counts[char] += 1
	
	return counts

with open(sys.argv[2], "w") as csvf:
	writer = csv.writer(csvf)
	labels = ["genome", "protein"]

	genomeData = {}
	chdir(sys.argv[1])
	foundChars = []
	foundFiles = []
	for type in ("*.faa", "*.fna"):
		foundFiles.extend(glob.glob(type))
	for file in foundFiles:
		genome = path.splitext(path.basename(file))[0].replace("_protein", "")
		if genome not in genomeData:
			genomeData[genome] = []

		f = open(file)
		readBuffer = ""
		reading = False
		protein = ""
		dataCounts = {}
		for line in f:
			if line.startswith(">"):
				if reading:
					dataCounts[protein] = getCount(readBuffer)
					for char in dataCounts[protein].keys():
						if not char in foundChars:
							foundChars.append(char)
				protein = line.replace(">", "")
				readBuffer = ""
				reading = True
			else:
				readBuffer += line.replace("\n", "")

			counted = getCount(readBuffer)
			dataCounts[protein] = getCount(readBuffer)
			for char in dataCounts[protein].keys():
				if not char in foundChars:
					foundChars.append(char)
		f.close()
		genomeData[genome] = dataCounts

	foundChars.sort()
	labels += foundChars
	writer.writerow(labels)
	for genome, data in genomeData.items():
		for protein, counts in data.items():
			data = []
			for char in foundChars:
				if char in counts.keys():
					data.append(counts[char])
				else:
					data.append(0)
			writer.writerow([genome, protein] + data)
