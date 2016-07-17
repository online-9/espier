import re 
import collections
import numpy as np 
import random

class ReadData(object):
	def __init__(self):
		return   

	# Store documents in a list in the form {words:frequencies}
	def documents(self,datafile):
		data = []
		with open(datafile,"r") as docs:
			content = docs.read()

		lines = content.split('\n')
		for doc in lines:
			words = doc.split()
			word_freq = {w.split(':')[0]:float(w.split(':')[1]) for w in words}
			data.append(word_freq)

		return data

	# List of all unique words
	def vocabulary(self,vocab_file):
		with open(vocab_file,"r") as words:
			vocab = words.read()
		vocab = re.split("\n",vocab)

		return vocab


class E_Step(object):
	"""Update parameters for the E-Steps of pLSA"""
	def __init__(self):
		return
		
	# E step to update P(d|z)
	def update_p_dz(self,p_wz,p_dz,p_z,docs,ntopic):
		# Intialize to store new prob. values
		new_p_dz = np.zeros((len(docs),ntopic))

		for d in  range(len(docs)):   
			items = list(docs[d].items())  
			# Shuffle to not keep the same sampling order always
			random.shuffle(items)
			for itm in items:
				[w,ft] = list(itm)
				# p(z|d,w)
				p_z_wd = p_z * p_dz[d,:] * p_wz[w,:]
				p_z_wd = p_z_wd/sum(p_z_wd)
				# n(d,w) * p(z|d,w)
				new_p_dz[d,:] += ft * p_z_wd

		row_sum = new_p_dz.sum(axis=0) 
		new_p_dz = new_p_dz/row_sum[np.newaxis,:]

		return new_p_dz
		
	
	# E-Step to update p(w|z) 
	def update_p_wz(self,p_wz,p_dz,p_z,docs,ntopic,nword):
		new_p_dw = np.zeros((nword,ntopic))
		for d in  range(len(docs)):
			items = list(docs[d].items())
			random.shuffle(items)
			for itm in items:
				[w,ft] = list(itm)
				# p(z|d,w)
				p_z_wd = p_z * p_dz[d,:] * p_wz[w,:]
				p_z_wd = p_z_wd/sum(p_z_wd)
				# sum_d=0^1 [ n(d,w) * p(z|d,w) ]
				new_p_dw[w,:] += ft * p_z_wd
		 
		row_sum = new_p_dw.sum(axis=0) 
		new_p_dw = new_p_dw/row_sum[np.newaxis,:]

		return new_p_dw
 

	# E-Step to update p(z)
	def update_p_z(self,p_wz,p_dz,p_z,docs,ntopic):
		p_z_new = np.zeros(ntopic)
		total_count = 0
		for d in  range(len(docs)):
			items = list(docs[d].items())
			random.shuffle(items)
			for itm in items:
				[w,ft] = list(itm)
				#Calculate p(z|d,w)
				p_z_wd = p_z * p_dz[d,:] * p_wz[w,:]
				p_z_wd = p_z_wd/sum(p_z_wd)
				# sum_d sum_w n(d,w) * p(z|d,w)
				total_count += ft
				p_z_new +=  ft * p_z_wd
								
		p_z_new = p_z_new/total_count

		return p_z_new

	
class Inference(object):
	"""returns classified topic"""
	def __init__(self):
		return
		
	# list of topic corresponding to the document's index
	def doc_vs_topics(self,p_dz):
		for index,top_prob_dis in enumerate(p_dz):
			# assign the topic with max prob. from prob. distribution list for the doc
			topic = np.where(top_prob_dis == max(top_prob_dis))[0]
			p_dz[index] = topic

		return p_dz
			
	# list of topic corresponding to the visual word's index
	def word_vs_topics(self,p_wz):
		for index,top_prob_dis in enumerate(p_wz):
			# assign the topic with max prob. from prob. distribution list for the word
			topic = np.where(top_prob_dis == max(top_prob_dis))[0]
			p_wz[index] = topic

		return p_wz[:,0]
