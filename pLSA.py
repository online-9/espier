import collections
import numpy as np
from aide import *
import matplotlib.pyplot as plt 
import sys , getopt

class pLSA(object):
	
	def __init__(self,datafile,vocabfile):
		self.datafile = datafile
		self.vocabfile = vocabfile

	def log_likelihood(self,p_wz,p_dz,p_z,docs):
		L = 0
		for d in range(len(docs)):                                    
			for w,ft in docs[d].items():                
				L += ft * np.log10( sum(p_z * p_dz[d,:] * p_wz[w,:]))

		return L

	def train(self,Z):
		max_iteration = 100
		beta = 0.001

		data = ReadData()
		docs = data.documents(self.datafile)
		vocab = data.vocabulary(self.vocabfile)
		print("%s document processed \n %s diffrent words \n" % (len(docs),len(vocab)))
		
		# Randomly initialize probabilities
		# p(w|z)
		p_wz  = np.random.rand(len(vocab),Z)  
		row_sum = p_wz.sum(axis=1) 
		p_wz = p_wz/row_sum[:,np.newaxis]

		# p(d|z)
		p_dz  = np.random.rand(len(docs), Z) 
		row_sum = p_dz.sum(axis=1)
		p_dz = p_dz/row_sum[:,np.newaxis]

		# p(z)
		p_z   = np.random.rand(Z) 
		p_z = p_z/sum(p_z)

		convergence = 0
		iteration = 0
		likelihood = 0
		likelihood_values = []

		e = E_Step()

		# M-step 
		print("Estimating probabilities")
		while((convergence == 0) and iteration < max_iteration):
			p_wz = e.update_p_wz(p_wz,p_dz,p_z,docs,Z,len(vocab))
			p_dz = e.update_p_dz(p_wz,p_dz,p_z,docs,Z)
			p_z  = e.update_p_z(p_wz,p_dz,p_z,docs,Z)

			likelihood_new = self.log_likelihood(p_wz,p_dz,p_z,docs)    

			# Converge when log likelihood stops changing a lot
			if(abs(likelihood-likelihood_new) <= beta):
				convergence = 1

			iteration +=1
			likelihood_values.append(likelihood_new)
			print("Iteration : %s \t likelihood : %s" % (iteration,likelihood_new))
			likelihood = likelihood_new

		res_prob  = open("words_prob.txt","w")
		for l in p_wz:
			res_prob.write("%s\n" % " ".join(str(l)))
		res_prob.close()

		i = Inference()
		results = i.word_vs_topics(p_wz)
		print("Writting results to file results.txt\n")
		res_topic = open("words_topic.txt","w")
		for x in results:
			res_topic.write("%s\n" % " ".join(str(x)))

		res_topic.close()


if __name__ == '__main__':
	docs = 'dataset/data.txt'
	vocab = 'dataset/codebook.txt'
	model = pLSA(docs,vocab)
	model.train(5)


