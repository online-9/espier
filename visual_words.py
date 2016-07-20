import sift
import os
import numpy as np
import scipy.cluster.vq as vq
from convert_to_pgm import *
from glob import glob
from pickle import dump,HIGHEST_PROTOCOL
from os.path import exists, isdir,basename,join,splitext

EXTENSIONS = [".pgm"]
PRE_ALLOCATION_BUFFER = 1000  # for sift
K_THRESH = 1  #stopping threshold for kmeans
CODEBOOK_FILE = 'codebook.txt'
HISTOGRAMS_FILE = 'trainingdata.txt'


def get_imgfiles(path):
	all_files = []
	all_files.extend([join(path, basename(fname))for fname in glob(path + "/*")
					if splitext(fname)[-1].lower() in EXTENSIONS])
	
	return all_files

def extractSift(input_files):
	all_features_dict = {}
	count = 0
	for i,fname in enumerate(input_files):
		# path to store resulting sift files
		features_fname = 'sift_output/'+fname.split('/')[2].split('.')[0]+'.sift'
		if count == 0:
			os.chdir('siftDemoV4')
		print("Calculating sift features for ",fname)
		sift.process_image(fname,features_fname,count)
		count+=1
		locs, descriptors = sift.read_features_from_file(features_fname)
		all_features_dict[fname] = descriptors
	os.chdir('..')
	return all_features_dict


def dict2numpy(dic):
	nkeys = len(dic)
	array = np.zeros((nkeys*PRE_ALLOCATION_BUFFER,128))
	pivot = 0
	for key in dic.keys():
		value = dic[key]
		nelements = value.shape[0]
		while pivot + nelements > array.shape[0]:
			padding = np.zeros_like(array)
			array = np.vstack((array,padding))
		array[pivot:pivot + nelements] = value
		pivot += nelements
	array = np.resize(array,(pivot, 128))
	return array


def computeHistograms(codebook,descriptors):
	# assign closest vector from codebook to the descriptor
	code,dist = vq.vq(descriptors,codebook)
	# histogram depicting no. of descriptors(translated to codebook words) for each word
	visual_words_histogram,bin_edges = np.histogram(code,bins=range(codebook.shape[0] + 1),normed=True)

	return visual_words_histogram


def writeHistogramsToFile(nwords,fnames,all_word_histgrams,features_fname):
	data_rows = np.zeros(nwords)  # +1 for the category label
	for fname in fnames:
		histogram = all_word_histgrams[fname]
		if (histogram.shape[0] != nwords):  # scipy deletes empty clusters
			nwords = histogram.shape[0]
			data_rows = np.zeros(nwords)
			print('nclusters have been reduced to '+str(nwords))
		# stack histograms of all images in single training data file
		data_rows = np.vstack((data_rows,histogram))
	data_rows = data_rows[1:]
	fmt = ''
	for i in range(nwords):
		fmt = fmt + str(i) + ':%f '
	np.savetxt(features_fname, data_rows, fmt)


# (put the downloaded Sift Folder in current directory)
def pre_process(path):
	os.mkdir('siftDemoV4/sift_input')
	os.mkdir('siftDemoV4/sift_output')
	# sift takes pgm images
	convert2pgm(path+'/*','siftDemoV4/sift_input/')
	# to store codebook and image histograms
	os.mkdir('dataset')


def run(img_datapath):
	pre_process(img_datapath)
	all_files = get_imgfiles('siftDemoV4/sift_input')
	all_features = extractSift(all_files)

	print("Computing visual words via k-means")
	all_features_array = dict2numpy(all_features)
	nfeatures = all_features_array.shape[0]
	# no. of visual words
	nclusters = int(np.sqrt(nfeatures))
	codebook, distortion = vq.kmeans(all_features_array,nclusters,thresh=K_THRESH)

	datasetpath = 'dataset/'
	np.savetxt(datasetpath+CODEBOOK_FILE,codebook)

	print("Computing the visual words histograms for each image")
	all_word_histgrams = {}
	for imagefname in all_features:
		word_histgram = computeHistograms(codebook, all_features[imagefname])
		all_word_histgrams[imagefname] = word_histgram

	writeHistogramsToFile(nclusters,all_files,all_word_histgrams,datasetpath + HISTOGRAMS_FILE)

if __name__ == '__main__':
	# path to scraped images folder
	run('img-data')
