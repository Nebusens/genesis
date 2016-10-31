import argparse
import os 
import math
from svgpathtools import svg2paths
import numpy as np
import shutil
import getpass
import sys

parser = argparse.ArgumentParser(description='Genesis CLI')
parser.add_argument('-c', '--convert', help="Convert .svg to .ini")
parser.add_argument('-r', '--reference', type=int, help="Reference in meters")
parser.add_argument('-e', '--height', type=float, help="Building height in meters")
parser.add_argument('-s', '--simulate', action="store_true", help="Simulate .ini (output.ini default)")
args = parser.parse_args()

def readSVG( filedir ):
	paths, attributes = svg2paths(filedir)
	
	listPoints = []
	listSegments = []
	
	for x in range(len(attributes)):
		if('points' in attributes[x]):
			polyline = attributes[x]['points'].split()
			listPoints.extend(polyline)		
			file = os.path.splitext(os.path.basename(filedir))[0].upper()
			for y in range(len(polyline)-1):
				listSegments.append([file, polyline[y], polyline[y+1]])

	listPoints = sorted(set(listPoints))

	return listPoints, listSegments

def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

ref = 1
if args.reference:
	ref = args.reference

height = 3.0
if args.height:
	height = args.height

if args.convert:
	onlysvgs = [os.path.join(args.convert, f) for f in os.listdir(args.convert) if f.endswith(".svg")]

	if any("reference.svg" in s for s in onlysvgs):
		indices = [i for i, s in enumerate(onlysvgs) if 'reference.svg' in s]		
		listPoints, listSegments = readSVG(onlysvgs[indices[0]])
		onlysvgs.remove(onlysvgs[indices[0]])

		p0 = np.array(listPoints[0].split(',')).astype(np.float)
		p1 = np.array(listPoints[1].split(',')).astype(np.float) 

		ref = distance(p0, p1)/ref;	
		
		listAllPoints = []
		listAllSegments = []
																																								
		for item in onlysvgs:
			listPoints, listSegments = readSVG(item)
			listAllPoints.extend(listPoints)		
			listAllSegments.extend(listSegments)
				
		listAllPoints = sorted(set(listAllPoints))		

		for x in range(len(listAllSegments)):
			for y in range(2):
				for z in range(len(listAllPoints)):
					if(listAllSegments[x][y+1] == listAllPoints[z]):
						listAllSegments[x][y+1] = z
						break

		for x in range(len(listAllPoints)):
			p = np.array(listAllPoints[x].split(','))
			listAllPoints[x] = ["%.3f" % (float(p[0])/ref), "%.3f" % (float(p[1])/ref)]

		fo = open("output.ini", "wb")
		fo.write("[info]\n")
		fo.write("npoints = " + str(len(listAllPoints)) + "\n")
		fo.write("nsegments = " + str(len(listAllSegments)) + "\n")
		fo.write("nsubsegments = " + str(0) + "\n\n")
		fo.write("[points]\n")

		for x in range(len(listAllPoints)):
			fo.write(str((x+1)*-1) + " = (" + str(listAllPoints[x][0]) + ", " + str(listAllPoints[x][1]) + ")\n")	

		fo.write("\n[segments]\n")

		for x in range(len(listAllSegments)):
			fo.write(str(x+1) + " = {'name': '" + listAllSegments[x][0] +"', 'transition': False, 'connect': [" + str((listAllSegments[x][1]+1)*-1) + ", " + str((listAllSegments[x][2]+1)*-1) + "], 'offset': 0, 'z': [0.0, " + str(height) + "]}\n")

		fo.write("\n[display]\n")
		fo.close()

		print ('File .ini created')				
	else:
		print ('reference.svg not found')
		exit()

if args.simulate:

	user = getpass.getuser();

	srcfile = './output.ini'
	pdir = '/home/' + user + '/pylayers_project'
	dstroot = pdir + '/struc/ini'
	
	if (os.path.isdir(pdir)):
		print ('Project exit in default directory.\nYou can delete the actual project. Choice yes/no')
		yes = set(['yes','y', 'si', ''])
		no = set(['no','n'])

		choice = raw_input().lower()
		if choice in yes:
			shutil.rmtree(pdir)
		elif choice in no:
			print ('Use actual project')
		else:
			print ('Please respond with \'yes\' or \'no\'')
			os._exit(1)

	from tvtk.api import tvtk
	from pylayers.gis.layout import *

	assert not os.path.isabs(srcfile)
	dstdir =  os.path.join(dstroot, os.path.dirname(srcfile))

	shutil.copy(srcfile, dstdir)

	L = Layout('output.ini')
	
	#Necesary if call show3 first time
	L = Layout('output.ini')
	
	L._show3()
	