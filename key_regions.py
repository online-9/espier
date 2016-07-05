from skimage.feature import blob_dog
from math import sqrt
from skimage.color import rgb2gray

def diff_of_gaussian(image):
	image_gray = rgb2gray(image)
	blobs_dog = blob_dog(image_gray, min_sigma=3, max_sigma=30, threshold=.1)
	#radius of blob is sqrt(2)*sigma
	for sigma in blobs_dog:
		sigma[2]=sigma[2]*sqrt(2)

	for blob in blobs_dog:
		y, x, r = blob
		c = plt.Circle((x, y), r, color='green', linewidth=2, fill=False)
		ax.add_patch(c)

def harris(image):
	corners = corner_peaks(corner_harris(image), min_distance=1)
	for corner in corners:
	    y,x=corner[0],corner[1]
	    c = plt.Circle((x, y), 4, color='green', linewidth=2, fill=False)
	    ax.add_patch(c)

def interst_regions(image):
	fig,axes = plt.subplots()
	ax = axes[0]
	ax.imshow(image, interpolation='nearest')
	diff_of_gaussian(image)
	harris(image)
	plt.show()	
