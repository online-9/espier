"""
ORB feature detector and binary descriptor
"""
from skimage import data
from skimage.feature import (match_descriptors, corner_harris,corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

img = rgb2gray(data.astronaut())
descriptor_extractor = ORB(n_keypoints=200)

descriptor_extractor.detect_and_extract(img)
keypoints = descriptor_extractor.keypoints
descriptors = descriptor_extractor.descriptors

fig, ax = plt.subplots()
plt.gray()
plt.show()
