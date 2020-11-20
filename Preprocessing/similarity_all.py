# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:29:15 2017

@author: semkt
"""

# import the necessary packages
#from skimage.measure import structural_similarity as ssim
import numpy as np
import pandas as pd
import cv2
import glob
import re
import os
import json

path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/"
os.chdir(path)
print(path)


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype(float) - imageB.astype(float)) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar" the two images are
    return err


def compare_images(imageA, imageB):
	# compute the mean squared error index for the images
    m = mse(imageA, imageB)
    return m

#for c in chain:
 #   for g in generation:
  #      if c_1 == c_2 & g_1 == g_2-1:
            #orig = copy

### load the images -- the originals and copies to compare

# path to folder with all images
path = 'data/resized/'


# Import the csv file with image names
drawings_source_copy = pd.read_csv('data/drawings_source_copy.csv')
print(drawings_source_copy)


# make the image path column to a list
image_orig_list = drawings_source_copy[["Orig_ID"]]
image_orig_list = image_orig_list["Orig_ID"].tolist()

print(image_orig_list)

# make the image ID column to a list
image_copy_list = drawings_source_copy[["Copy_ID"]]
image_copy_list = image_copy_list["Copy_ID"].tolist()


drawings_orig = []
drawings_copy = []

for i in range(len(image_copy_list)):
    drawings_orig.append(path + image_orig_list[i] + ".png")
    drawings_copy.append(path + image_copy_list[i] + ".png")


# index for labels
idx = len(path)-1
print(idx)

#print(drawings_orig)
#print(drawings_copy)

# prepare panda to write logs
columns = ['Drawing_ID', 'Orig_ID', 'MSE']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)


# loop through originals and copies to compare and measure similarity 
for orig in range(len(drawings_orig)):
    original = cv2.imread(drawings_orig[i])
    contrast = cv2.imread(drawings_copy[i])
    print(type(original))
            
            # convert the images to grayscale
            #original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            #contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
            
            # run similarity measures
    MSE = compare_images(original, contrast)#, SSIM
    Drawing_ID = drawings_copy[i]
    Orig_ID = drawings_orig[i] 
            # get id label
            
            # write output to pandas
    DATA = DATA.append({
        'Drawing_ID': Drawing_ID,
        'Orig_ID': Orig_ID,
        'MSE': MSE
    }, ignore_index=True)

#print(DATA)

# save pandas
logfilename = "logfiles/similarity_data_all.csv"

DATA.to_csv(logfilename)            
