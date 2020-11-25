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

# set path
path = "C:/Users/Sophia/Documents/Social Transmission Study/Analysis of drawings/"
os.chdir(path)
print(path)

# define similarity function
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


# path to folder with all images
img_path = 'data/resized/'


# Import the csv file with image names
drawings_source_copy = pd.read_csv('data/csv_files/drawings_source_copy.csv')

# make the image path column to a list
image_orig_list = drawings_source_copy[["Orig_ID"]]
image_orig_list = image_orig_list["Orig_ID"].tolist()

# make the image ID column to a list
image_copy_list = drawings_source_copy[["Copy_ID"]]
image_copy_list = image_copy_list["Copy_ID"].tolist()

# prepare empty list to be filled with image names
drawings_orig = []
drawings_copy = []

# loop to append images to the lists
for i in range(len(image_copy_list)):
    drawings_orig.append(img_path + image_orig_list[i] + ".png")
    drawings_copy.append(img_path + image_copy_list[i] + ".png")


# prepare panda to write logs
columns = ['Drawing_ID', 'Orig_ID', 'MSE']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)


# loop through all images in the two lists and compare them row by row
for i in range(len(drawings_orig)):
    
    # read images
    original = cv2.imread(drawings_orig[i])
    contrast = cv2.imread(drawings_copy[i])
    
    # run similarity measure
    MSE = compare_images(original, contrast)
    
    # drawing ID's
    Drawing_ID = drawings_copy[i]
    Orig_ID = drawings_orig[i] 
    
    # write output to pandas
    DATA = DATA.append({
        'Drawing_ID': Drawing_ID,
        'Orig_ID': Orig_ID,
        'MSE': MSE
    }, ignore_index=True)

# save pandas
logfilename = "data/csv_files/similarity_data_all.csv"

DATA.to_csv(logfilename)            
