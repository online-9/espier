# espier
Unsupervised object recognition

Usage:
1. Scrape images with:
	python scrape_images.py
2. Create Visual bag of words with:
	python visual_words.py
   This will create a codebook file containing visual word's vectors and a trainingdata file containing histograms of images depicting frequency of each visual word in the image.
3. Calculate each visual word's "hidden topic" with:
	python pLSA.py
   This will make a file containing each word's topic(line index corresponds to word index in codebook).
