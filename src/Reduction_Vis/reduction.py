# import python packages
from collections import Counter
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import MDS

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as clrs
from scipy.cluster.hierarchy import dendrogram, linkage

# add to python environment the directory above the one the file is in (src)
import sys
import os
sys.path.append(os.path.dirname(__file__) + r"/..") 

#import OEIS files
import features as ftr


def main():
	features = ftr.read_features_file()
	general_field_names = ["name", "length"]
	feature_names = [name for (name, typ) in features[0].dtype.descr if name not in general_field_names]
	#feature_names = ["var","mean"]

	names = features[["name"]]
	X = ftr.extract_features(features, feature_names)
	X = X[0:1000,:]

	labels = np.asarray([i%100 for i in range(X.shape[0])])

	# pca(names, X)
	# tsne(names,X)
	hirerch_clustering(names,X,labels)
	#mds(names,X)

def clean(X,names,labels):
	if labels is None:
		labels = np.asarray([0 for i in range(X.shape[0])])
	idxs = np.isfinite(X).all(axis=1)

	return X[idxs], names[idxs], labels[idxs]

def color_dendogram(D, labels):
	""" gets linkage matrix and labels and returns a function that for each ids returns a color"""
	# label_num = len(set(labels))
	colors = []
	for label in labels:
		colors.append(Counter([label]))
	for row in D:
		left = colors[int(row[0])]
		right = colors[int(row[1])]

		colors.append(left + right)

	pallete = rainbow_colors(labels)
	def colorer(idx):
		return clrs.rgb2hex(pallete[colors[idx].most_common(1)[0][0]])
	return colorer

def hirerch_clustering(names,X,labels=None,similarity='cosine'):
	
	X,names,labels = clean(X,names,labels)

	D = linkage(X, 'average', similarity)
	plt.figure()
	print(D)
	colors = color_dendogram(D, labels)
	dendrogram(D,  leaf_rotation=90., link_color_func=colors, leaf_font_size=8., labels=names)
	plt.show()


def dim_red(names,X,model,title,labels=None):
	
	X,names,labels = clean(X,names,labels)	
	X_ts = model.fit_transform(X)
	plt_scatter(names, X_ts, title, labels)
	return X_ts

def mds(names, X, labels=None):
	dim_red(names,X,MDS(n_components=2), "MDS Analysis", labels)


def tsne(names, X, labels=None):
	"""runs a TSNE analysis"""
	dim_red(names,X,TSNE(n_components=2), "TSNE Analysis", labels)
	

def pca(names, X, labels=None):	
	"""runs a PCA analysis on features"""
	dim_red(names,X,PCA(n_components=2),"PCA Analysis", labels)
	#print(model.explained_variance_ratio_)

def rainbow_colors(labels):
	"""creates colors, each corresponding to a unique label"""
	cls = set(labels)

	return dict(zip(cls, cm.rainbow(np.linspace(0, 1, len(cls)))))

def plt_scatter(names, X, title, labels=None):
	if labels is None:
		labels = np.asarray([0 for i in range(X.shape[0])])

	colors = rainbow_colors(labels)
	plt.figure()
	for c,l in colors.iteritems():
		idx = labels == c
		plt.scatter(X[idx,0], X[idx,1], c=l)

	plt.title(title)

	plt.show()


if __name__ == '__main__':
	main()