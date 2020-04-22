#!/usr/bin/python3

from os import listdir, path
import sys
import random
from shutil import copyfile

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: %s [input directory] [training directory] [testing directory]" % (sys.argv[0]))
		exit()

	files = []
	for f in listdir(sys.argv[1]):
		if not f.endswith(".gz"):
			files.append(f)
	random.shuffle(files)

	for i in range(30):
		copyfile(path.join(sys.argv[1], files[i]), path.join(sys.argv[2], files[i]))
	for i in range(len(files) - 30):
		i += 30
		copyfile(path.join(sys.argv[1], files[i]), path.join(sys.argv[3], files[i]))
