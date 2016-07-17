import glob
import os
from PIL import Image

path = 'sift_input_data/*'

for img in glob.glob(path):
	Image.open(img).convert('L').save(img)
	target_img = img.split('.')[0]
	Image.open(img).save(target_img+'.pgm')
	os.remove(img)
