"""
Fast and easy script for deleting unnecessary duplicate files in a directory
"""

BAR_LENGTH = 75

import os
import sys
import hashlib

def progressBar(filesScanned, totalFiles):
	filledLength = int(round(BAR_LENGTH * filesScanned / float(totalFiles)))
	percents = round(100.0 * filesScanned / float(totalFiles), 1)
	bar = '#' * filledLength + '-' * (BAR_LENGTH - filledLength)
	sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', ", %d Files scanned" % (filesScanned)))
	sys.stdout.flush()

def findDups(directoryName):
	if not os.path.isdir(directoryName):
		print "Invalid directory %s" % (directoryName)
		return

	filesHashes = []
	duplicates = []
	filesInDir = [fileName for fileName in os.listdir(directoryName) if not os.path.isdir("%s\\%s" % (directoryName, fileName))]
	filesAmount = len(filesInDir)
	for i, foundFileName in enumerate(filesInDir):
		with open("%s\\%s" % (directoryName, foundFileName), "rb") as openedFile:
			fileHash = hashlib.sha256(openedFile.read()).hexdigest()
			if fileHash in filesHashes:
				duplicates.append(foundFileName)
			else:
				filesHashes.append(fileHash)
		progressBar(i+1, filesAmount)
	print
	return duplicates

def delDups(duplicates, directoryName):
	if len(duplicates) == 0:
		print "No unnecessary files were found"
		return

	userAns = raw_input("Found %d unnecessary files\nDo you wish to remove them? (y/n) " % len(duplicates))
	if userAns == "y":
		for dupFile in duplicates:
			os.remove("%s\\%s" % (directoryName, dupFile))
			print "Removed %s\\%s" % (directoryName, dupFile)
	elif userAns == "n":
		print "Bye bye"
		return
	else:
		print "Invalid input"
		return

def main():
	if len(sys.argv) != 2:
		print "Usage: %s <directory name>" % (sys.argv[0])
		return

	duplicates = findDups(sys.argv[1])
	if duplicates == None:
		return
	delDups(duplicates, sys.argv[1])

if __name__ == "__main__":
	main()