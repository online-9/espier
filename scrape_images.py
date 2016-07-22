from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import base64
import re
import glob
import urllib
import os

class ScrapeImages(object):
	''' Scrapes Google image search results for multiple queries
	 ''' 

	def __init__(self):
		self.DOWNLOAD_DIR = os.path.dirname(__file__)
		self.image_xpath = "//img[@class='rg_i']"
		self.driver = webdriver.Firefox()
		
	def target_url(self,query):
		return "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q=%s&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:m" % query
		
	def scrape(self,query):
		# Scrape all results returned from current page
		self.driver.get(self.target_url(query))
		self.scroll_down
		prev_file_no = 0
		imgs = self.driver.find_elements_by_xpath(self.image_xpath)
		# the first image_xpath returns only 100 images,so repeat find_elements_by_xpath again and again
		while prev_file_no < 1000 and len(imgs) > prev_file_no:
			self.scroll_down
			imgs = self.driver.find_elements_by_xpath(self.image_xpath)
			print('new loop. found %i images, prev_file_no was %i' % (len(imgs), prev_file_no))
			for file_no, img_el in enumerate(imgs[prev_file_no:]):
				self.save_img(img_el,file_no+prev_file_no,foldername=query)
			prev_file_no = len(imgs)


	def create_folder(self,foldername):
		# Create folders for corresponding queries
		if not os.path.exists(foldername):
			os.makedirs(os.path.join(self.DOWNLOAD_DIR,foldername))

	def read_queries(self,filename):
		# Retrieve image queries from query file
		with open(filename,'r') as q:
			query_list = [line.strip().split() for line in q.readlines()]
		return query_list

	def run(self,filename):
		# Scrapes over all queries in the loop 
		query_list = self.read_queries(filename)
		for query in query_list:
			print(query)
			# images corresponding to every query will be stored in a folder with the same name
			self.create_folder(foldername=query[0])
			self.scrape(query[0])

	# modified from http://sqa.stackexchange.com/questions/3499/how-to-scroll-to-bottom-of-page-in-selenium-ide
	@property
	def scroll_down(self):
		# define initial page height for 'while' loop
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(8)
			try:
				self.driver.find_element_by_id('smb').click()
			except:
				print('no See More button found...')
			new_height = self.driver.execute_script("return document.body.scrollHeight")

			if new_height == last_height:
				break
			else:
				last_height = new_height

	def hover(self,el):
		# Hovers to input element
		ActionChains(self.driver).move_to_element(el).perform()

	def right_click_save_as(self,el):
		# ActionChains queues up these tasks to perform right click
		ActionChains(self.driver).move_to_element(el).context_click(el).send_keys('V').perform()

	def save_img_src(self,el,file_no,foldername,sleep_time=0.25):
		# Retrieve from source url
		base = el.get_attribute('src')
		# just guess jpeg,no file ext in url
		file_name = foldername+"/"+str(file_no)+".jpeg"
		try:
			urllib.request.urlretrieve(base, file_name)
			print('wrote ',file_name)
		except IOError as e:
			print('save from image source error',e)
		time.sleep(sleep_time)

	def save_img(self,el,file_no,foldername,sleep_time=0.25):
		# Hovers to current image and save it
		self.hover(el)
		time.sleep(0.25)

		base = el.get_attribute('src')
		if not base:
			print('no img', file_no)
			return

		base_clean = base[base.find(',')+1:]
		try:
			base_filetype = re.findall(r'image/(.*);', base)[0]
		except IndexError:
			print('no image extension,try to save from src', file_no)
			self.save_img_src(el,file_no,foldername)
			return

		file_name = foldername+"/"+str(file_no)+"."+ base_filetype
		with open(os.path.join(self.DOWNLOAD_DIR,file_name), 'wb') as f:
			x = base64.b64decode(base_clean)
			f.write(x)
			

		print('wrote ',file_name)
		time.sleep(sleep_time)

if __name__ == "__main__":

	# create a queries.txt 
	obj = ScrapeImages()
	obj.run('queries.txt')
