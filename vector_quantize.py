from convert_to_pgm import *
import sift
import re
import os
from glob import glob
from os.path import exists, isdir, basename, join, splitext
import numpy as np
import scipy.cluster.vq as vq
import skimage.io
import matplotlib.pyplot as plt 

def get_imgfiles(path):
	all_files = []
	all_files.extend([join(path, basename(fname))for fname in glob(path + "/*")])
	return all_files

def extractSift(input_files,target_folder):
	all_features_dict = {}
	count=0
	for i,fname in enumerate(input_files):
		features_fname = target_folder+'/'+fname.split('/')[2].split('.')[0]+'.sift'
		if exists(features_fname) == False:
			print("Calculating sift features for ",fname)
			sift.process_image(fname, features_fname,count)
			count+=1
		locs, descriptors = sift.read_features_from_file(features_fname)
		all_features_dict[fname] = (locs,descriptors)
	os.chdir('..')
	return all_features_dict


def computeHistograms(codebook,location,descriptors,words_topic,imm):
	key_topics = []
	# assign closest vector from codebook to the descriptor
	code,dist = vq.vq(descriptors,codebook)
	for loc,visual_word in zip(location,code):
		dic = {"loc":(loc[0],loc[1]),"scale":loc[2],"topic":words_topic[visual_word]}
		key_topics.append(dic)
	return key_topics

if __name__ == '__main__':
	
	path = 'siftDemoV4/test_data'
	pcodebook = 'dataset/codebook.txt'
	word_topic = 'words_topic.txt'
	target_folder = 'test_descrptrs'

	# convert images to pgm for sift input
	# convert2pgm(path+'/*')

	fcodebook = open(pcodebook,'r')
	codebook = re.split('\n',fcodebook.read())[:-1]
	
	for el in range(len(codebook)):
		codebook[el] = [float(j) for j in re.split(' ',codebook[el])]

	f = open(word_topic, 'r')
	words_topic = re.split('\n',f.read())[:-1]

	all_files = get_imgfiles(path)
	all_features = extractSift(all_files,target_folder)

	all_img_res = {}
	for img in all_features:
		key_topics = computeHistograms(codebook,all_features[img][0],all_features[img][1],words_topic,img)
		all_img_res[img] = key_topics
	# def color(all_img_res):

top_colors = {'0':'red','1':'green'}

for fimg in all_img_res:
	row,column,scale,topic = [],[],[],[]
	fig,ax = plt.subplots()
	image = skimage.io.imread(fimg)

	for key_point in all_img_res[fimg]:
		row.append(key_point["loc"][0])
		column.append(key_point["loc"][1])
		scale.append(key_point["scale"])
		topic.append(key_point["topic"][0])

	for y,x,r,t in zip(row,column,scale,topic):
		c = plt.Circle((x, y), r, color=top_colors[t], linewidth=2, fill=False)
		ax.add_patch(c)

	ax.imshow(image, interpolation='nearest')
plt.show()