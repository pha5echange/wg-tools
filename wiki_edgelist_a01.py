# wiki_edgelist_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# jmg*AT*phasechange*DOT*info
# April 19th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/wg-tools

# Cleans up wiki genre data
# Reads .txt file and uses only `item' and `is subset of' components to generate unweighted, undirected edgelist

# import packages
import os
import sys
import resource
from datetime import datetime

fileName = ("wiki_edgelist_a01.py")
versionNumber = ("a01")

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
logPath = os.path.join("logs", str(runDate) + '_' + str(startTime) + '_' + 'wiki_edgelist_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open edgeList file for data output
edgeListPath = os.path.join("data", 'wiki_edgeList_' + versionNumber + '.txt')
edgeList = open(edgeListPath, 'w')

# open rawdata inputFile for reading
inputPath = os.path.join("rawdata", 'wiki_genres_graph.txt')
inputFile = open (inputPath, 'r')

for line in inputFile:

	item, itemLabel,_image,_subclassOf, _subclassOfLabel = line.split(",")
	cleanItemLabel = itemLabel.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")
	cleanSubclassOfLabel = _subclassOfLabel.replace(" ", "_").replace("'","").replace(",","").replace("u'","").replace("(","").replace(")","").strip("\n")

	# check for empty item string
	if cleanItemLabel:

		# check for empty subclass string
		if not cleanSubclassOfLabel:
			cleanSubclassOfLabel = cleanItemLabel

		edgeList.write(str(cleanItemLabel) + ',' + str(cleanSubclassOfLabel) + '\n')

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
