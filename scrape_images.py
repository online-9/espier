import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import base64
import re
import glob
import urllib
import os

QUERY = raw_input('Query string: ')
DOWNLOAD_DIR = os.path.dirname(__file__)

target_url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q=%s&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:m" % QUERY

image_xpath = "//img[@class='rg_i']"

driver = webdriver.Firefox()
driver.get(target_url)

# modified from http://sqa.stackexchange.com/questions/3499/how-to-scroll-to-bottom-of-page-in-selenium-ide
def scroll_down():
	# define initial page height for 'while' loop
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		time.sleep(8)
		try:
			driver.find_element_by_id('smb').click()
		except:
			print 'no See More button found...'

		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		else:
			last_height = new_height


def hover(el):
	ActionChains(driver).move_to_element(el).perform()

def right_click_save_as(el):
	ActionChains(driver).move_to_element(el) \
	.context_click(el) \
	.send_keys('V') \
	.perform()

def save_img_src(el, file_no, sleep_time=0.25):
	base = el.get_attribute('src')
	# just guess jpeg, probably no file ext in url...
	file_name_full = 'panda'+"/"+str(file_no)+".jpeg"
	try:
		urllib.urlretrieve(base, file_name_full)
		print 'wrote from url %s' % file_name_full
	except IOError as e:
		print 'Bad URL?', e

	time.sleep(sleep_time)


def dl_base64_img(el, file_no, sleep_time=0.20):
	hover(el)
	time.sleep(0.20)

	base = el.get_attribute('src')
	if not base:
		print 'no img', file_no
		return

	base_clean = base[base.find(','):]
	try:
		base_filetype = re.findall(r'image/(.*);', base)[0]
	except IndexError:
		print 'no img filetype... trying to save src', file_no
		save_img_src(el, file_no)
		return

	file_name_full = 'panda'+"/"+str(file_no)+"."+ base_filetype
	with open(os.path.join(DOWNLOAD_DIR,file_name_full), 'w') as f:
		f.write(base64.decodestring(base_clean))

	print 'wrote %s' % file_name_full
	time.sleep(sleep_time)

if __name__ == "__main__":
	scroll_down()

	prev_file_no = 0
	imgs = driver.find_elements_by_xpath(image_xpath)
	# the first image_xpath returns only 100 images,so repeat find_elements_by_xpath again and again
	while prev_file_no < 1000 and len(imgs) > prev_file_no:
		scroll_down()
		imgs = driver.find_elements_by_xpath(image_xpath)
		print 'new loop. found %i images, prev_file_no was %i' % (len(imgs), prev_file_no)
		for file_no, img_el in enumerate(imgs[prev_file_no:]):
			dl_base64_img(img_el, file_no+prev_file_no)
		prev_file_no = len(imgs)
