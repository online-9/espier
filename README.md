# espier

The aim is to automatically learn object categories by utilizing the output from Image search engines. This categorizes objects in an unsupervised way by applying pLSA which is a statistical technique for the analysis of co-occurrence data.
The feature vectors used for this are generated through bag of visual words approach in which the interest regions(found using SIFT here) are vector quantized.
These visual words are then assigned with the most likely topic they belong to using P(w|z)[probability of word's occurrence within a topic]. And the images are assigned with their most likely topic using P(z|d)[probability of topic given the document/image].

----------

### Usage:
    
    1. Scrape images with:
        ```
        python scrape_images.py
        ```

    2. Create Visual bag of words with:
        ```
        python visual_words.py
        ```
       
       This will create a codebook file containing visual word's vectors and a trainingdata file containing histograms of images depicting frequency of each visual word in the image.

    3. Calculate each visual word's "hidden topic" with:
        ```
        python pLSA.py
        ```

        This will make a file containing each word's topic(line index corresponds to word index in codebook).

