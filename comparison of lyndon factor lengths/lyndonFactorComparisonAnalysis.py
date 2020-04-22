#!/bin/python3

# calculate counts for lyndon factors produced from
# computeLyndonFactorsForInverseFreqAndModifiedDuvals.py to compare
# freq and modified duvals

import sys
import csv
from scipy.stats import ks_2samp, wilcoxon
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

from statsmodels.stats.multitest import multipletests

from statistics import mode

if len(sys.argv) < 5:
	print("Usage: %s [factors csv] [existing ga factors csv] [new ga factors csv] [testing Duvals Amino Acid Factors] [output csv]" % (sys.argv[0]))
	exit()

def calculateCountAndLength(factors):
	split = factors.split(sep)
	length = 0
	lengths = []
	counts = []
	for factor in split:
		lengths.append(len(factor))
		length += len(factor)
	counts.append(len(split))
	
	return (len(split), length, lengths, counts)

with open(sys.argv[1]) as csvf:
	reader = csv.reader(csvf)
	headers = next(reader)
	statsPerGenome = {}
	counts = {
		"duval": [],
		"genome": [],
		"protein": [],
		"ga": [],
		"nga": []
	}
	numberOfFactors = {
		"modduval": [],
		"genome": [],
		"protein": [],
		"ga": [],
		"nga": [],
		"duval": []
	}
	
	count = 0
	countBad = 0
	duvalsLengths = []
	genomeLengths = []
	proteinLengths = []
	gaLengths = []
	ngaLengths = []
	for line in reader:
		if not line[0] in statsPerGenome.keys():
			statsPerGenome[line[0]] = {}
			statsPerGenome[line[0]]["duvalFactorCount"] = 0
			statsPerGenome[line[0]]["genomeFreqCount"] = 0
			statsPerGenome[line[0]]["genomeFactorLen"] = 0
			statsPerGenome[line[0]]["duvalFactorLen"] = 0
			statsPerGenome[line[0]]["proteinFactorCount"] = 0
			statsPerGenome[line[0]]["proteinFactorLen"] = 0
			statsPerGenome[line[0]]["gaFactorCount"] = 0
			statsPerGenome[line[0]]["gaFactorLen"] = 0
			statsPerGenome[line[0]]["ngaFactorCount"] = 0
			statsPerGenome[line[0]]["ngaFactorLen"] = 0
			statsPerGenome[line[0]]["count"] = 0
		duvalsFactColumn = 4
		genomeFreqColumn = 5
		proteinFreqColumn = 7
		sep = ", "
		
		duvals = calculateCountAndLength(line[duvalsFactColumn])
		statsPerGenome[line[0]]["duvalFactorCount"] += duvals[0]
		statsPerGenome[line[0]]["duvalFactorLen"] += duvals[1]
		
		genome = calculateCountAndLength(line[genomeFreqColumn])
		statsPerGenome[line[0]]["genomeFreqCount"] += genome[0]
		statsPerGenome[line[0]]["genomeFactorLen"] += genome[1]
		
		protein = calculateCountAndLength(line[proteinFreqColumn])
		statsPerGenome[line[0]]["proteinFactorCount"] += protein[0]
		statsPerGenome[line[0]]["proteinFactorLen"] += protein[1]
		
		statsPerGenome[line[0]]["count"] += 1

		counts["duval"].append(duvals[0])
		counts["genome"].append(genome[0])
		counts["protein"].append(protein[0])
		
		numberOfFactors["modduval"] += (duvals[3])
		numberOfFactors["genome"] += (genome[3])
		numberOfFactors["protein"] += (protein[3])
		
		duvalsLengths += duvals[2]
		genomeLengths += genome[2]
		proteinLengths += protein[2]

		if genome[0] < protein[0]:
			countBad += 1
			print(line[1])
		count += 1
	
	"""with open(sys.argv[2]) as gacsvf:
		gareader = csv.reader(gacsvf)
		next(gareader)
		for galine in gareader:
			gaFactColumn = 3
			
			ga = calculateCountAndLength(galine[gaFactColumn])
			statsPerGenome[galine[0]]["gaFactorCount"] += ga[0]
			statsPerGenome[galine[0]]["gaFactorLen"] += ga[1]
			
			counts["ga"].append(ga[0])
			gaLengths += ga[2]

	with open(sys.argv[3]) as ngacsvf:
		ngareader = csv.reader(ngacsvf)
		next(ngareader)
		for ngaline in ngareader:
			ngaFactColumn = 3
			
			nga = calculateCountAndLength(ngaline[ngaFactColumn])
			statsPerGenome[ngaline[0]]["ngaFactorCount"] += nga[0]
			statsPerGenome[ngaline[0]]["ngaFactorLen"] += nga[1]
			
			counts["nga"].append(nga[0])
			ngaLengths += nga[2]"""
	
	print("Total %d with %d where genome factor count is less than the protein factor count" % (count, countBad))
	data = {
		"genomes": [],
		"duval": [],
		"protein": [],
		"genome": [],
		#"ga": [],
		#"nga": [],
		"blank": []
	}
	for genome, stats in statsPerGenome.items():
		data["genomes"].append(genome)
		data["duval"].append(stats["duvalFactorLen"] / float(stats["duvalFactorCount"]))
		data["genome"].append(stats["genomeFactorLen"] / float(stats["genomeFreqCount"]))
		data["protein"].append(stats["proteinFactorLen"] / float(stats["proteinFactorCount"]))
		#data["ga"].append(stats["gaFactorLen"] / float(stats["gaFactorCount"]))
		#data["nga"].append(stats["ngaFactorLen"] / float(stats["ngaFactorCount"]))
		data["blank"].append("")
		
		#print("%s: Duvals: %d with avg len: %f, genomeFreq %d with avg len %f: , Total lines: %d, Protein: %d with avg len %f" % (genome, stats["duvalFactorCount"], stats["duvalFactorLen"] / float(stats["duvalFactorCount"]), stats["genomeFreqCount"], stats["genomeFactorLen"] / float(stats["genomeFreqCount"]), stats["count"], stats["proteinFactorCount"], stats["proteinFactorLen"] / float(stats["proteinFactorCount"])))
	
	# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.ks_2samp.html
	confidence = 0.05
	pvals = []
	
	ks = ks_2samp(counts["duval"], counts["protein"])
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the protein average ordering
	print("duval - protein ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	pvals.append(ks[1])
	
	ks = ks_2samp(counts["duval"], counts["genome"])
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the genome average ordering
	print("duval - genome ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	pvals.append(ks[1])
	
	ks = ks_2samp(counts["protein"], counts["genome"])
	# H0 - there is no significant difference between the average factor length of the protein average ordering and the genome average ordering length
	print("protein - genome ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	pvals.append(ks[1])
	
	# bonferroni for each set of tests
	bf = multipletests(pvals, alpha=confidence, method="bonferroni")
	print("BF corrected values: ")
	print(bf)
	
	#------------------------------------------------------------
	#------------------------------------------------------------
	
	# again for factor length instead of number of factors
	ks = ks_2samp(duvalsLengths, proteinLengths)
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the protein average ordering
	print("duval - protein ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	ks = ks_2samp(duvalsLengths, genomeLengths)
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the genome average ordering
	print("duval - genome ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	ks = ks_2samp(proteinLengths, genomeLengths)
	# H0 - there is no significant difference between the average factor length of the protein average ordering and the genome average ordering length
	print("protein - genome ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	print("wilcoxon test")
	
	#------------------------------------------------------------
	#------------------------------------------------------------
		
	wc = wilcoxon(counts["duval"], counts["protein"])
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the protein average ordering
	print("duval - protein wc: %f" % (wc[1]))
	if wc[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	wc = wilcoxon(counts["duval"], counts["genome"])
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the genome average ordering
	print("duval - genome wc: %f" % (wc[1]))
	if wc[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	wc = wilcoxon(counts["protein"], counts["genome"])
	# H0 - there is no significant difference between the average factor length of the protein average ordering and the genome average ordering length
	print("protein - genome wc: %f" % (wc[1]))
	if wc[1] < confidence:
		print("significant")
	else:
		print("not significant")
	
	#------------------------------------------------------------
	#------------------------------------------------------------

	"""ks = ks_2samp(duvalsLengths, ngaLengths)
	# H0 - there is no significant difference between the duvals average factor length and the average factor length of the new ga ordering length
	print("duval - new ga ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")

	ks = ks_2samp(ngaLengths, gaLengths)
	# H0 - there is no significant difference between the new ga ordering length and the existing ga ordering length
	print("new ga - ga ks: %f" % (ks[1]))
	if ks[1] < confidence:
		print("significant")
	else:
		print("not significant")"""
	
	print("mean duval %f, stdev %f" % (np.mean(counts["duval"]), np.std(counts["duval"])))
	print("mean protein %f, stdev %f" % (np.mean(counts["protein"]), np.std(counts["protein"])))
	print("mean genome %f, stdev %f" % (np.mean(counts["genome"]), np.std(counts["genome"])))
	print("max duval %f / min %f" % (max(counts["duval"]), min(counts["duval"])))
	print("max protein %f / min %f" % (max(counts["protein"]), min(counts["protein"])))
	print("max genome %f / min %f" % (max(counts["genome"]), min(counts["genome"])))
	print("mode duval %f" % mode(counts["duval"]))
	print("mode genome %f" % mode(counts["genome"]))
	print("mode protein %f" % mode(counts["protein"]))

	with open(sys.argv[-1], 'w') as outf:
		writer = csv.writer(outf)
		writer.writerow(list(data.keys())[:-1])
		for i in range(len(data[list(data.keys())[0]])):
			outbuf = []
			for j in data.keys():
				outbuf.append(data[j][i])
			writer.writerow(outbuf)
	
	for x in ["duval", "protein", "genome"]:
		plt.clf()
		plt.hist(data[x], bins="auto")
		if x == "duval":
			x = "modified duval"
		plt.title("Histogram of " + x + " ordering average per genome factor lengths")
		plt.ylabel("Count")
		plt.xlabel("Factor length")
		plt.savefig("averageLength" + x + ".eps")
		
	for x in ["modduval", "protein", "genome"]:
		plt.clf()
		plt.hist(numberOfFactors[x], bins="auto")
		if x == "duval":
			x = "modified Duval's"
		plt.title("Histogram of " + x + " ordering number of factors")
		plt.ylabel("Count")
		plt.xlabel("Number of factors")
		plt.savefig("numberOfFactors" + x + ".eps")
	plt.clf()
	#for x in ["duval", "protein", "genome"]:
	#	label = x
	#	if x == "duval":
	#		label = "modified Duval's"
	
	with open(sys.argv[4], "r") as f:
		duvalreader = csv.reader(f)
		next(duvalreader)
		for line in duvalreader:
			numberOfFactors["duval"].append(len(line[2].split(", ")))
	print("mean origduval %f, stdev %f" % (np.mean(numberOfFactors["duval"]), np.std(numberOfFactors["duval"])))
	print("max origduval %f / min %f" % (max(numberOfFactors["duval"]), min(numberOfFactors["duval"])))
	print("mode origduval %f" % mode(numberOfFactors["duval"]))

	
	max_num = 17
	plt.hist([numberOfFactors[x] for x in ["modduval","genome","protein","duval"]], label=["Modified Duval's", "Genome", "Protein", "Duval's Algorithm"], histtype='bar', bins=np.arange(max_num)-0.5, stacked=False)
	#plt.hist([x for _,x in numberOfFactors.items()], label=["Modified Duval's", "Genome", "Protein"], histtype='bar', bins="auto", rwidth=10, stacked=False)
	ax = plt.gca()
	ax.minorticks_on()
	#ax.tick_params(axis='x', which='minor', bottom=False)
	ax.tick_params(axis='x', which='minor', direction='out')
	plt.legend()
	plt.title("Histogram of number of Lyndon factors for each ordering method")
	plt.ylabel("Count")
	plt.xlabel("Number of Lyndon factors")
	plt.tight_layout()
	plt.ylim((0, 250000))
	#plt.xlim((0,16))
	plt.savefig("numberOfFactorsAll.eps")

	maxValue = 0
	for x, values in [("duval", duvalsLengths), ("protein", proteinLengths), ("genome", genomeLengths)]:
		for val in values:
			if maxValue < val:
				maxValue = val
	for x, values in [("duval", duvalsLengths), ("protein", proteinLengths), ("genome", genomeLengths)]:
		plt.clf()
		sns.distplot(values, hist=False, kde=True)
		plt.title("Gaussian probability density of " + x + " ordering factor length distribution")
		plt.ylabel("Probability density")
		plt.xlabel("Factor length")
		plt.savefig("factorGPD" + x + ".eps")

	for x, values in [("duval", duvalsLengths), ("protein", proteinLengths), ("genome", genomeLengths)]:
		plt.clf()
		plt.hist(values, bins="auto")
		plt.title("Histogram of " + x + " ordering factor length distribution")
		plt.ylabel("Count")
		plt.xlabel("Factor length")
		plt.savefig("factorDist" + x + ".eps")
