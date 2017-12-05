from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle
import scipy

with open('fasttext_dict_train_int.pkl') as f:
	glove_dict_train = pickle.load(f)

def is_subseq(x, y):
	it = iter(y)
	return all(c in it for c in x)


def getOutput(output_vector,each_inp):

	words   = []
	vectors = []

	for x in glove_dict_train.keys():
		words.append(x)
		vectors.append(glove_dict_train[x])

	#print len(glove_dict_train



	vectors = np.array(vectors)
	nbrs = NearestNeighbors(n_neighbors=50, algorithm='auto').fit(vectors)
	distances, indices = nbrs.kneighbors([each_inp[0]])
	input_word1 = words[indices[0][0]]
	distances, indices = nbrs.kneighbors([each_inp[1]])
	input_word2 = words[indices[0][0]]

	distances, indices = nbrs.kneighbors([output_vector])

	for i in indices[0]:
		z = input_word1 + input_word2
		if is_subseq(words[i],z) == True and words[i] != input_word1 and words[i] != input_word2:
		# if words[i] != input_word1 and words[i] != input_word2:
			return words[i]

	#print words[indices[0][0]]
	return words[indices[0][0]]


def getClosest(output_vector):
	words   = []
	vectors = []

	for x in glove_dict_train.keys():
		words.append(x)
		vectors.append(glove_dict_train[x])

	#print len(glove_dict_train)

	vectors = np.array(vectors)
	nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(vectors)
	distances, indices = nbrs.kneighbors([output_vector])

	return words[indices[0][0]]
