# wiki_edgelist_a03.py
# Version a03
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# jmg*AT*phasechange*DOT*info
# May 10th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/wg-tools

# Cleans up wiki genre data
# Reads .txt file and uses `item' (genre), and `is subset of', `is influenced by', `is based on', and `is inspired by' (properties) to generate unweighted edgelist

# import packages
import os
import sys
import resource
from datetime import datetime

fileName = ("wiki_edgelist_a02.py")
versionNumber = ("a03")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# open file for writing log
logPath = os.path.join("logs", 'wiki_edgelist_' + versionNumber + '_' + str(runDate) + '_' + str(startTime) + '_log.txt')
runLog = open(logPath, 'a')

# open edgeList file for data output
edgeListPath = os.path.join("data", 'wiki_edgeList_' + versionNumber + '.txt')
edgeList = open(edgeListPath, 'w')

# open rawdata inputFile for reading
inputPath = os.path.join("rawdata", 'wiki_genres_data.txt')
inputFile = open (inputPath, 'r')

for line in inputFile:

	itemLabel, item, subclassOf, influencedBy, basedOn, inspiredBy = line.split(",")
	cleanItemLabel = itemLabel.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")
	cleanSubclassOf = subclassOf.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")
	cleanInfluencedBy = influencedBy.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")
	cleanBasedOn = basedOn.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")
	cleanInspiredBy = inspiredBy.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")

	# check for empty item string
	if cleanItemLabel:

		# check for empty subclass string
		if not cleanSubclassOf:
			cleanSubclassOf = cleanItemLabel

		edgeList.write(str(cleanItemLabel) + ',' + str(cleanSubclassOf) + '\n')

		if not cleanInfluencedBy: 
			cleanInfluencedBy = cleanItemLabel

		edgeList.write(str(cleanItemLabel) + ',' + str(cleanInfluencedBy) + '\n')

		if not cleanBasedOn: 
			cleanBasedOn = cleanItemLabel

		edgeList.write(str(cleanItemLabel) + ',' + str(cleanBasedOn) + '\n')

		if not cleanInspiredBy: 
			cleanInspiredBy= cleanItemLabel

		edgeList.write(str(cleanItemLabel) + ',' + str(cleanInspiredBy) + '\n')

# close inputFile
inputFile.close()

'''
# Remove duplicates
lines = open(edgeListPath, 'r').readlines()
lines_set = set(lines)
out = open(edgeListPath, 'w')

for line in sorted(lines_set):
	out.write(line)
'''

# close edgeList
edgeList.close()

# end timing of run
endTime = datetime.now()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('File: ' + fileName) 
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))

# write to log
runLog.write ('Run Information' + '\n' +'\n')
runLog.write ('File: ' + fileName + '\n')
runLog.write ('Version: ' + versionNumber +'\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()
