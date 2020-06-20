#!/bin/python3

import sys
import csv
import matplotlib.pyplot as plt
from os import path
import seaborn as sns
import numpy as np
import re
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import networkx as nx

if len(sys.argv) < 4:
	print("Usage: %s [inverse freq and mod duval amino acid orderings] [genome char counts] [output plot]" % (sys.argv[0]))
	exit()

# plot the average position of characters in orderings for all genomes
# with the frequency of the character in the genome as the size of the
# plot point

characterFreqPerGenome = {}
with open(sys.argv[2]) as csvf:
	reader = csv.reader(csvf)
	chars = next(reader)[2:]
	for line in reader:
		genome = line[0].strip().replace("\n", "")
		total = 0
		for i in range(2, len(line)):
			if genome not in characterFreqPerGenome.keys():
				characterFreqPerGenome[line[0].strip().replace("\n", "")] = {}
			if chars[i - 2] not in characterFreqPerGenome[genome].keys():
				characterFreqPerGenome[genome][chars[i - 2]] = 0
			characterFreqPerGenome[genome][chars[i - 2]] += int(line[i])
			total += int(line[i])
		for char, val in characterFreqPerGenome[genome].items():
			characterFreqPerGenome[genome][char] /= float(total)

def getOrdering(line, column, duvalsRegex):
	ordering = line[column]
	if duvalsRegex:
		G = nx.Graph()
		matches = re.search("\(\[(.*?)\]", ordering)
		nodes = matches.group(1).replace(", ", "")
		for node in nodes:
			G.add_node(node)
		edges = [x.group(1) for x in re.finditer(r"(?:\((.,.)\)(?:, )?)+?", ordering)]
		for edgePair in edges:
			begin, end = edgePair.split(",")
			G.add_edge(begin, end)
		ordering = ""
		for edge in nx.algorithms.traversal.edgedfs.edge_dfs(G):
			if ordering == "":
				ordering += edge[0]
			ordering += edge[1]
	
	return ordering

def getAveragePositionsForGenomes(reader, columns):
	averagePositionsPerGenomePerColumn = {}
	positionsPerCharacterPerColumn = {}
	genome = None
	for line in reader:
		if genome != line[0]:
			genome = line[0]
			for column, chars in positionsPerCharacterPerColumn.items():
				if column not in averagePositionsPerGenomePerColumn.keys():
					averagePositionsPerGenomePerColumn[column] = {}
				if genome not in averagePositionsPerGenomePerColumn[column].keys():
					averagePositionsPerGenomePerColumn[column][genome] = {}
				for char, values in chars.items():
					averagePositionsPerGenomePerColumn[column][genome][char] = np.mean(values)
			
			positionsPerCharacterPerColumn = {}
		for column, duvalsRegex in columns:
			i = 0
			for char in getOrdering(line, column, duvalsRegex):
				if column not in positionsPerCharacterPerColumn.keys():
					positionsPerCharacterPerColumn[column] = {}
				if char not in positionsPerCharacterPerColumn[column].keys():
					positionsPerCharacterPerColumn[column][char] = []
				positionsPerCharacterPerColumn[column][char].append(i)
				i += 1
	genome = line[0]
	for column, chars in positionsPerCharacterPerColumn.items():
		if column not in averagePositionsPerGenomePerColumn.keys():
			averagePositionsPerGenomePerColumn[column] = {}
		if genome not in averagePositionsPerGenomePerColumn[column].keys():
			averagePositionsPerGenomePerColumn[column][genome] = {}
		for char, values in chars.items():
			averagePositionsPerGenomePerColumn[column][genome][char] = np.mean(values)
	return averagePositionsPerGenomePerColumn

with open(sys.argv[1]) as csvf:
	reader = csv.reader(csvf)
	next(reader)
	averagePositions = getAveragePositionsForGenomes(reader, [(2, True), (3, False), (6, False)])
	
	for column, genomes in averagePositions.items():
		plotData = {
			"averagePosition": [],
			"genome": [],
			"markers": [],
			"markers2": [],
			"chars": [],
			"alpha": [],
			"size": [],
			"size2": [],
			"scaling": [],
		}
		genomeIndex = len(genomes)
		for genome, chars in genomes.items():
			for char, averagePosition in chars.items():
				plotData["averagePosition"].append(averagePosition)
				plotData["markers"].append("$%s$" % char)
				plotData["markers2"].append("o")
				plotData["genome"].append(genomeIndex)
				plotData["chars"].append(char)
				#characterFreqPerGenome[genome][char] += 1
				#characterFreqPerGenome[genome][char] *= 5
				plotData["size"].append(80 * characterFreqPerGenome[genome][char])
				plotData["size2"].append(400 * characterFreqPerGenome[genome][char])
			genomeIndex -= 1

		fig, ax = plt.subplots(figsize=(6, 4))
		#fig = plt.gcf()
		fig.set_size_inches(8, 6)
		fig.subplots_adjust(left=0.2, bottom=0.2)
		
		axscatter = sns.scatterplot(x="genome", y="averagePosition", data=plotData, hue="chars", style="markers", markers=plotData["markers2"], alpha=0.4, s=plotData["size2"])
		axscatter.legend_.remove()
		axscatter = sns.scatterplot(x="genome", y="averagePosition", data=plotData, hue="chars", style="markers", markers=plotData["markers"], s=plotData["size"])
		axscatter.legend_.remove()
		plt.ylim((4.5, 20))
		plt.xticks(np.arange(0, 100, step=45))
		"""axins = zoomed_inset_axes(axscatter, 2)#, bbox_to_anchor=(60, 10, 40, 40))
		plt.xlim((10, 11))
		plt.ylim((20,30))
		mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
		axscatter = sns.scatterplot(x="averagePosition", y="genome", data=plotData, hue="chars", style="markers", markers=plotData["markers2"], alpha=0.4, s=plotData["size2"])
		axscatter.legend_.remove()
		axscatter = sns.scatterplot(x="averagePosition", y="genome", data=plotData, hue="chars", style="markers", markers=plotData["markers"], s=plotData["size"])
		axscatter.legend_.remove()"""
		plt.ylabel("Average position in alphabet", fontsize=12)
		plt.xlabel("Genome", fontsize=12)
		#plt.title("Average position of characters in Flexi-Duval orderings\nwith the size of each point proportional to the frequency of the\ncharacter in the genome")
		plt.tight_layout()
		plt.savefig(sys.argv[3] + str(column) + ".pdf", dpi=1200)
		plt.clf()



"""genomeData = {}
maxY = 0
with open(sys.argv[1], "r") as csvf:
	reader = csv.reader(csvf, delimiter=',')
	headers = next(reader)
	for line in reader:
		position = 0
		for char in line[2]:
			if char not in genomeData.keys():
				genomeData[char] = {}
			if position not in genomeData[char].keys():
				genomeData[char][position] = 0
			genomeData[char][position] += 1
			if genomeData[char][position] > maxY:
				maxY = genomeData[char][position]
			position += 1

for char, positionCounts in genomeData.items():
	plt.bar(list(positionCounts.keys()), list(positionCounts.values()))
	plt.xlabel("Position")
	plt.ylabel("Count")
	plt.title("Count for character %s for all ordering positions" % (char))
	axes = plt.gca()
	axes.set_ylim([0, maxY])
	outputFile = path.join(sys.argv[2], "Character " + char + " position " + str(position) + ".png")
	plt.savefig(outputFile)
	plt.clf()
	plt.close()"""
