import glob
import os
from PIL import Image
import re

# path = 'siftDemoV4/sift_input_data/*'
def convert2pgm(i_path,o_path):
	for img in glob.glob(i_path):
		Image.open(img).convert('L').save(img)
		target_img = re.split('[./]',img)[1]
		print(target_img)
		Image.open(img).save(o_path+target_img+'.pgm')
