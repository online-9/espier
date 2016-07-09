""" 
Python module for use with David Lowe's SIFT code available at:
http://www.cs.ubc.ca/~lowe/keypoints/
adapted from the matlab code examples.

http://www.janeriksolem.net/2009/02/sift-python-implementation.html
"""

import os
from numpy import *
import pylab


def process_image(imagename, resultname):
	""" process an image and save the results in a .key ascii file"""
	
	#check if linux or windows 
	if os.name == "posix":
		cmmd = "./sift <"+imagename+">"+resultname
	else:
		cmmd = "siftWin32 <"+imagename+">"+resultname
	
	os.system(cmmd)
	print 'processed', imagename
	
def read_features_from_file(filename):
	""" read feature properties and return in matrix form"""
	
	f = open(filename, 'r')
	header = f.readline().split()
	
	num = int(header[0]) #number of features
	featlength = int(header[1]) #length of the descriptor
	if featlength != 128: #should be 128
		raise RuntimeError, 'Keypoint descriptor length invalid (should be 128).' 
		
	locs = zeros((num, 4))
	descriptors = zeros((num, featlength));        

	#parse the .key file
	e = f.read().split() #split the rest into individual elements
	pos = 0
	for point in range(num):
		#row, col, scale, orientation of each feature
		for i in range(4):
			locs[point,i] = float(e[pos+i])
		pos += 4
		
		#the descriptor values of each feature
		for i in range(featlength):
			descriptors[point,i] = int(e[pos+i])
		#print(descriptors[point])    
		pos += 128
	
		#normalize each input vector to unit length
		descriptors[point] = descriptors[point] / linalg.norm(descriptors[point])
		#print(descriptors[point])
	f.close()
	
	return locs,descriptors

	
def plot_features(im,locs):
	""" show image with features. input: im (image as array), 
		locs (row, col, scale, orientation of each feature) """
	
	pylab.gray()
	pylab.imshow(im)
	pylab.plot([p[1] for p in locs],[p[0] for p in locs],'ob')
	pylab.axis('off')
	pylab.show()
