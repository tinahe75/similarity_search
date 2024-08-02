### image saving ###

Please see save_images.py.
This script goes through the csv and downloads the images. 

Note that there are some special cases:
- special chars are handled via replacement. I referenced URL encoding online for the special chars I saw in the data
- split lines: some links are split into two lines, those are joined together
- one faulty line: there is a single faulty entry, where the url is incorrect. I manually fixed it by checking against other url patterns.



### calculating embeddings ###

Please see the colab notebook. 
I used pretrained CLIP for image embeddings of dimension 512. 
I calculated embeddings for the images in order and saved the output in a npy file. 
Because all inputs/outputs are from a fixed pool of images, I can pre-compute all the embeddings. 
This way, my Docker doesn't even need PyTorch, only numpy is enough.


### web server ###

This is implemented in service.py.
The docker image automatically runs this script. 
The web server uses Flask. There is a single API for img_search.  
The query url's embedding is compared against the rest of the embeddings, and the indices with max cosine similarity are recorded.
The API call will return the top 10 most similar images' URL and their similarity scores.

If the url is invalid (not in the database), an error msg will be returned.



### send requests ###

I provide another script for testing calling the API. 
To see the args for this script, run:
 docker exec -it image_similarity python send_requests.py -h

Input can either be a url or an index (0 to 2651).

I added an option to visualize the input and output images, but this option doesn't seem to work within Docker. 
Therefore the viz flag is defaulted to FALSE. But if running locally, this flag can be enabled to visualize how good the matches are. 

