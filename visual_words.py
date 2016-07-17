import sift
import os
from glob import glob
import numpy as np
import scipy.cluster.vq as vq
from pickle import dump, HIGHEST_PROTOCOL
from os.path import exists, isdir, basename, join, splitext

EXTENSIONS = [".pgm"]
datasetpath = 'dataset/'
PRE_ALLOCATION_BUFFER = 1000  # for sift
K_THRESH = 1  #stopping threshold for kmeans
CODEBOOK_FILE = 'codebook.file'
HISTOGRAMS_FILE = 'trainingdata.txt'


def get_imgfiles(path):
	all_files = []
	all_files.extend([join(path, basename(fname))for fname in glob(path + "/*")
					if splitext(fname)[-1].lower() in EXTENSIONS])
	
	return all_files


def extractSift(input_files):
	all_features_dict = {}
	count=0
	for i,fname in enumerate(input_files):
		features_fname = 'sift_output_data/'+fname.split('/')[2].split('.')[0]+'.sift'
		if exists(features_fname) == False:
			print("Calculating sift features for ",fname)
			sift.process_image(fname, features_fname,count)
			count+=1
		locs, descriptors = sift.read_features_from_file(features_fname)
		print(descriptors.shape)
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
		
		data_rows = np.vstack((data_rows,histogram))
	data_rows = data_rows[1:]
	fmt = ''
	for i in range(nwords):
		fmt = fmt + str(i) + ':%f '
	np.savetxt(features_fname, data_rows, fmt)



if __name__ == '__main__':

	path = 'siftDemoV4/sift_input_data'
	all_files = get_imgfiles(path)
	all_features = extractSift(all_files)

	print("Computing visual words via k-means")
	all_features_array = dict2numpy(all_features)
	nfeatures = all_features_array.shape[0]
	nclusters = int(np.sqrt(nfeatures))
	codebook, distortion = vq.kmeans(all_features_array,nclusters,thresh=K_THRESH)
	
	with open(datasetpath+CODEBOOK_FILE,'wb') as f:
		dump(codebook,f,protocol=HIGHEST_PROTOCOL)

	
	np.savetxt(datasetpath+'codebook.txt',codebook)


	print("Compute the visual words histograms for each image")
	all_word_histgrams = {}
	for imagefname in all_features:
		word_histgram = computeHistograms(codebook, all_features[imagefname])
		all_word_histgrams[imagefname] = word_histgram

	print("Write the histograms to file to pass it to the svm")
	writeHistogramsToFile(nclusters,
						  all_files,
						  all_word_histgrams,
						  datasetpath + HISTOGRAMS_FILE)