# wgt_network_single_a02.py
# Version a02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# April 21st 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots a directed network graph (e.g. A --> is a subclass of --> B) from edgelist 'data\wiki_edgelist.txt'
# Displays using parameters from 'config/config_nw.txt'
# Writes 'data\wgt_network__nodeList.txt' with nodes and degrees (k)
# Writes analysis files to 'results\'
# Writes gexf files to 'gexf\'
# Writes image to 'networks\'
# Added 'maxDeg' metric and 'isolated nodes' counter
# Also renders an undirected version of the network to facilitate cluster/clique analysis

# Run AFTER cleaning wiki_edgelist.py (this generates `data\wiki_edgelist.txt')

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Import packages
import os
import resource
import numpy as np
import networkx as nx
import community
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import clique
from datetime import datetime

versionNumber = ("a02")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# Create 'data' subdirectories if necessary
if not os.path.exists("data"):
	os.makedirs("data")

if not os.path.exists("data/nodelists"):
	os.makedirs("data/nodelists")

# Create 'gexf' subdirectories if necessary
if not os.path.exists("gexf"):
	os.makedirs("gexf")

# Create 'results' subdirectories if necessary
if not os.path.exists("results"):
	os.makedirs("results")

if not os.path.exists("results/analysis"):
	os.makedirs("results/analysis")

# Create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# Open file for writing log
logPath = os.path.join("logs", str(runDate) + '_' + str(startTime) + '_' + 'wgt_network_single_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "Wiki Single-Network Thing | Version " + versionNumber + " | Starting...")
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Wiki Single-Network Thing | Version " + versionNumber + '\n' + '\n')

# Open file to write list of nodes
nodeListPath = os.path.join("data/nodelists", 'wgt_network_' + versionNumber + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file for writing gexf
gexfPath = os.path.join("gexf", 'wgt_network_' + versionNumber + '.gexf')
gexfFile = open(gexfPath, 'w')

# Open file for analysis results
anPath = os.path.join("results/analysis", 'wgt_network_' + versionNumber + '_analysis.txt')
anFile = open(anPath, 'w')

# Open file to write image
nwImgPath = os.path.join("networks", 'wgt_network_' + versionNumber + '_nw.eps')
nwImg = open (nwImgPath, 'w')

anFile.write ('\n' + "==========================================================================" + '\n' + '\n')
anFile.write ("Wiki Single-Network Thing | Version " + versionNumber + '\n' + '\n')

# Uncomment the line below to facilitate optional self-loop removal
#selfLoopIP = int(input ("Enter 1 here to remove self-loop edges: "))
# Auto-remove self-loops - comment out the line below if self-loop removal is optional
selfLoopIP = 1

# Read the edgelist and generate graph
print ('\n' + "Importing Edge List... ")
inputPath = os.path.join("data", 'wiki_edgelist.txt')
edgeList = open (inputPath, 'r')
wikiDiGraph = nx.read_edgelist(edgeList, delimiter=',', create_using=nx.DiGraph())

# Calculate basic graph statistics
print ('Calculating various things...' + '\n')
nodes = nx.number_of_nodes(wikiDiGraph)
edges = nx.number_of_edges(wikiDiGraph)
density = nx.density(wikiDiGraph)
nodeList = nx.nodes(wikiDiGraph)
nodeList.sort()
selfLoopTotal = wikiDiGraph.number_of_selfloops()
connections = edges - selfLoopTotal

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print
print (str(nodeList))

runLog.write ('Network Properties: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n' + '\n')
runLog.write (str(nodeList))

anFile.write ('Network Properties: ' + '\n' + '\n')
anFile.write ('Nodes: ' + str(nodes) + '\n')
anFile.write ('Edges: ' + str(edges) + '\n')
anFile.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
anFile.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
anFile.write ('Density: ' + str(density) + '\n' + '\n')
anFile.write (str(nodeList))

# Remove self-loops
selfLoopCount = 0
if selfLoopIP == 1:
	print ('\n' + 'Checking for and removing self-loops...' + '\n')
	runLog.write('\n' + '\n' + 'Checking for and removing self-loops...' + '\n')
	for u,v in wikiDiGraph.edges():
		if u == v:
			wikiDiGraph.remove_edge(u,v)
			print ('removed self-loop ' + str(u))
			selfLoopCount += 1
	
	if selfLoopCount == 1:
		print ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edge.')
		runLog.write ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edge.' + '\n')

	if selfLoopCount > 1:
		print ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edges.')
		runLog.write ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edges.' + '\n')
else:
	print ('Self-loops intact.' + '\n')
	runLog.write('\n' + 'Self-loops intact.' + '\n')

# Count isolates
isolateCount = 0
for i in nodeList:
	if nx.is_isolate(wikiDiGraph,i):
		isolateCount += 1

# Recalculate basic graph statistics
print ('Recalculating various things...' + '\n')
edges = nx.number_of_edges(wikiDiGraph)
density = nx.density(wikiDiGraph)
selfLoopTotal = wikiDiGraph.number_of_selfloops()

print ('Nodes: ' + str(nodes))
print ('Isolated nodes:' + str(isolateCount))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Density: ' + str(density))
print

runLog.write ('Recalculated Network Properties: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

anFile.write ('Recalculated Network Properties: ' + '\n' + '\n')
anFile.write ('Nodes: ' + str(nodes) + '\n')
anFile.write ('Isolated nodes:' + str(isolateCount) + '\n')
anFile.write ('Edges: ' + str(edges) + '\n')
anFile.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
anFile.write ('Density: ' + str(density) + '\n')

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list with degree...' + '\n')
for i in nodeList:
	nodeDegree = wikiDiGraph.degree(i)
	nodeListOP.write(str(i) + ',' + str(nodeDegree) +'\n')
	print ("Node " + str(i) + " degree: " + str(nodeDegree))

nodeListOP.close()

# Write gexf file for use in Gephi
print ("Writing gexf file... " + '\n')
runLog.write('\n' + "Writing gexf file... " + '\n')
nx.write_gexf(wikiDiGraph, gexfFile)
gexfFile.close()

# Plot and display graph
# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('Reading layout config file...' + '\n')

# Open and read 'config_nw.txt'
nwConfigPath = os.path.join ("config", 'config_nw.txt')
nwConfig = open(nwConfigPath, 'r').readlines()

# Remove the first line
firstLine = nwConfig.pop(0)

for line in nwConfig:
	n_size, n_alpha, node_colour, n_text_size, text_font, e_thickness, e_alpha, edge_colour, l_pos, e_text_size, edge_label_colour = line.split(",")
	
node_size = int(n_size)
node_alpha = float(n_alpha)
node_text_size = int(n_text_size)
edge_thickness = int(e_thickness)
edge_alpha = float(e_alpha)
label_pos = float(l_pos)
edge_text_size = int(e_text_size)

print ('Laying out graph...' + '\n')

#nx.draw(wikiDiGraph)
graph_pos = nx.spring_layout(wikiDiGraph)
nx.draw_networkx_nodes(wikiDiGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(wikiDiGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
#nx.draw_networkx_labels(wikiDiGraph, graph_pos, font_size = node_text_size, font_family = text_font)
#nx.draw_networkx_edge_labels(wikiDiGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_color = edge_label_colour, font_size = edge_text_size, font_family = text_font)

# write image file
print ('Writing image file...' + '\n')
plt.savefig(nwImg, format = 'eps', bbox_inches='tight')
nwImg.close()

# display graph
print ('Displaying graph...' + '\n')
plt.show()

# Render undirected version of wikiDiGraph to facilitate final analysis of graph characteristics
print('\n' + "Rendering undirected version to facilitate final analysis of graph characteristics... ")
runLog.write('\n' + "Rendering undirected version to facilitate final analysis of graph characteristics... " + '\n')
wikiGraph = wikiDiGraph.to_undirected()

# Analysis
print ('\n' + 'Analysing undirected graph...' + '\n')
print ('Maximal degree... ' + '\n')
degreeSeq = sorted(nx.degree(wikiGraph).values(),reverse=True)
maxDeg = max(degreeSeq)
print ('Maximal degree: ' + str(maxDeg) + '\n')
anFile.write ('Maximal degree: ' + str(maxDeg) + '\n')
print ('Average clustering coefficient...' + '\n')
avClustering = nx.average_clustering(wikiGraph)
print ('Connected components...' + '\n')
connectComp = [len(c) for c in sorted(nx.connected_components(wikiGraph), key=len, reverse=True)]
print ('Find cliques...' + '\n')
cl = nx.find_cliques(wikiGraph)
cl = sorted(list(cl), key = len, reverse = True)
print ('Number of cliques: ' + str(len(cl)) + '\n')
cl_sizes = [len(c) for c in cl]
print ('Size of cliques: ' + str(cl_sizes))

print ('\n' + 'Undirected Network Properties: ' + '\n')
print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Density: ' + str(density))
print ('Maximal degree: ' + str(maxDeg))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Number of cliques: ' + str(len(cl)))
print ('Connected Components: ' + str(connectComp))
print
print (str(nx.info(wikiGraph)))
print

runLog.write ('\n' + 'Undirected Network Properties: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Maximal degree: ' + str(maxDeg) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')
runLog.write ('\n' + str(nx.info(wikiGraph)) + '\n')

anFile.write ('\n' + 'Undirected Network Properties' + '\n' + '\n')
anFile.write ('Date of run: {}'.format(runDate) + '\n')
anFile.write ('Nodes: ' + str(nodes) + '\n')
anFile.write ('Edges: ' + str(edges) + '\n')
anFile.write ('Density: ' + str(density) + '\n')
anFile.write ('Maximal degree: ' + str(maxDeg) + '\n')
anFile.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
anFile.write ('Number of cliques: ' + str(len(cl)) + '\n')
anFile.write ('Connected Components: ' + str(connectComp) + '\n')
anFile.write ('\n' + str(nx.info(wikiGraph)))
anFile.close()

# End timing of run
endTime = datetime.now()

print
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))

runLog.write ('\n' + '\n' + 'Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()
