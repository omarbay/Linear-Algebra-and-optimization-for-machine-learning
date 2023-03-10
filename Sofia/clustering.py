# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import time
t1 = time.time()

import pandas as pd
import numpy as np
#import sklearn
import numpy.random as rnd
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
# from scipy import sparse as sp
# import scipy as sci
# from scipy import io
from sklearn import metrics

# Import dataset
from sklearn.datasets import fetch_openml
X, y = fetch_openml('mnist_784', version=1, return_X_y=True)

#%%
t2 = time.time()
# Convert data to arrays
Xnp = pd.DataFrame.to_numpy(X)
ynp = pd.DataFrame.to_numpy(y)

# Choose number of samples to work with
choose_num_samples = 70000
Xnew = Xnp[:choose_num_samples, :]
ynew = ynp[:choose_num_samples]

# Normalize features
Xnew = Xnew / 255;

#%% The two necessary functions for kMeans
def assign_to_cluster(X, C):
    num_features = np.shape(X)[1]
    #print(num_features)
    K = np.shape(C)[0]
    #print(K)
    repX = X[:,:,np.newaxis]
    repX = np.tile(repX, (1, 1, K)) # Repeat samples K times
    reshC = np.reshape(np.transpose(C), (1, num_features, K))
    diff = repX - reshC;
    dist = np.linalg.norm(diff, ord=2, axis=1)
    idx = np.argmin(dist, axis=1);
    return idx

def update_centroids(X, idx, K):
    num_features = np.shape(X)[1]
    C = np.zeros((K,num_features))
    for idx_c in np.arange(K):
        C[idx_c, :] = np.mean(X[np.where(idx == idx_c)[0], :], axis = 0)
       # print(C)
    return C

#%% Function to find the most frequent number per cluster
# source: https://www.geeksforgeeks.org/frequent-element-array/
def mostFrequent(arr):
    n = len(arr)
    # Insert all elements in Hash.
    Hash = dict()
    for i in range(n):
        if arr[i] in Hash.keys():
            Hash[arr[i]] += 1
        else:
            Hash[arr[i]] = 1
            
    # find the max frequency
    max_count = 0
    res = -1
    for i in Hash:
        if (max_count < Hash[i]):
            res = i
            max_count = Hash[i]
         
    return res, max_count
#%%
K = 10 # Number of clusters
[num_samples, num_features] = np.shape(Xnew)

#%% Initialize centroids
randidx = rnd.permutation(num_samples)[:K]  # randomly
# randidx = np.arange(K)        # take the first K samples as initial centroids
centroids = Xnew[randidx,:] 

#%%
max_iter = 50    # Maximum number of iterations
iter = 0
diff_obj_f = -1
idx_sample = np.arange(num_samples)
obj_f = np.zeros(max_iter)
while iter < max_iter and diff_obj_f < 0:
    idx = assign_to_cluster(Xnew, centroids)
    # print(idx)
    centroids = update_centroids(Xnew, idx, K)

    temp = np.linalg.norm(Xnew - centroids[idx, :], ord=2, axis=1)
    obj_f[iter] = sum(temp**2)
    if iter != 0:
        diff_obj_f = obj_f[iter] - obj_f[iter - 1]
    iter  += 1
    # print(idx)
    
# # Plot resulting centroids
# for idx_c in np.arange(K):
#     Ximage = np.resize(centroids[idx_c, :], (28, 28))
#     imgplot = plt.imshow(Ximage)
#     plt.show()
    
#%%
t3 = time.time()
print('Time elapsed with data loading [s]: ', t3 - t1)
print('Time elapsed without data loading [s]: ', t3 - t2)

#%% Accuracy calculation as in assignment description
m = np.zeros(K)
A = np.zeros(K)
freq_m = np.zeros(K)
for idx_c in np.arange(K):
    freq_m[idx_c] = mostFrequent(ynew[idx == idx_c])[1]
    A[idx_c] = freq_m[idx_c]
    
Acc = sum(A) / num_samples

#%% # Show metrics
print('Accuracy: ', Acc)
print('Completeness: ', metrics.completeness_score(ynew, idx))
print('Homogeneity: ', metrics.homogeneity_score(ynew, idx))