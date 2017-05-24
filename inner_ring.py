# Need to extract all edges that are inside a square, rougly representing the C-Ring of Linkoping.
# edges are exported to a file using BaseX to only include the needed information.
# output is a weight-file to use with SUMO
# ugly regexes.
#
# Anders Rassner
# 
import sys, os, re

def check_if_inner(text, weight): # weight is a float, text is a line like <edge id=":100038_7" shape="4702.04,8269.45 4706.38,11178.50" length="11.44" speed="11.11"/>
    edge_id = re.findall(r"<edge.+(?= shape)",text) 
    shape = re.findall(r"[-+shape\=]?\d*\.\d+|[-+shape\=]\d+",text)
    length = re.findall(r"(?<=length\=\")+\d*\.\d+",text)
    speed = re.findall(r"(?<=speed\=\")+\d*\.\d+",text)
    x = float(shape[0])
    y = float(shape[1])
    traveltime = float(length[0])/float(speed[0])
    if x > 4406 and x < 5904 and y > 8271 and y < 9717:
        result = "    " + edge_id[0] + " traveltime=\"" + str(weight*traveltime) + "\"/>"
    else:
        result = ""
    
    return result
    
    #if x > 4406 AND x < 5904 AND y > 8271 AND y < 9717:

inputfile = open('link_big4_edges.txt')
outputfile = open('link_big4_inner_edges.txt', 'w')
weight = 1.5 #weight traveltime 50% higher

outputfile.writelines("<meandata>\n  <interval begin=\"0\" end=\"3600\" id=\"whatever\">\n")

#for i in inputfile.next()
for line in inputfile:
    result = check_if_inner(line,weight)
    if result != "":
        #print result
        outputfile.writelines(result + "\n")

outputfile.writelines("  </interval>\n</meandata>")
inputfile.close()
outputfile.close()
