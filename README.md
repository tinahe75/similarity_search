## Image search

### Saving images

Please see `save_images.py`.
This script goes through the csv and downloads the images. 

Note that there are some special cases:
- special chars are handled via replacement. I referenced URL encoding online for the special chars I saw in the data
- split lines: some links are split into two lines, those are joined together
- one faulty line: there is a single faulty entry, where the url is incorrect. I manually fixed it by checking against other url patterns.



### Calculating embeddings

Please see the colab notebook. 
I used pretrained CLIP for image embeddings of dimension 512. 
I calculated embeddings for the images in order and saved the output in a npy file. 
Because all inputs/outputs are from a fixed pool of images, I can pre-compute all the embeddings. 
This way, my Docker doesn't even need PyTorch, only numpy is enough.


### Web server 

This is implemented in `service.py`.
The docker image automatically runs this script. 
The web server uses Flask. There is a single API for img_search.  
The query url's embedding is compared against the rest of the embeddings, and the indices with max cosine similarity are recorded.
The API call will return the top 10 most similar images' URL and their similarity scores.

If the url is invalid (not in the database), an error msg will be returned.

### Docker container

Steps for building the Docker container: 

```
cd similarity_search
docker compose build
docker compose up -d
```
After this, you can directly send requests.

### Send requests 

I provide another script for testing calling the API. 
To see the args for this script, run:
 ```docker exec -it image_similarity python send_requests.py -h```
 
Input can either be a url or an index (0 to 2651).
For example:

Lookup via index:
```docker exec -it image_similarity python send_requests.py --lookup 18```

Lookup via url:

 ```docker exec -it image_similarity python send_requests.py --url https://valentino-cdn.thron.com/delivery/public/thumbnail/valentino/5ffe4ba9-62f5-47d8-9942-954eccc406cf/ihqstx/std/500x0/VLOGO-SIGNATURE-METAL-AND-SWAROVSKI®-CRYSTAL-BRACELET?quality=80"&"size=35"&"format=auto```

(Note that if the url contains special chars like '&', you may need to replace certain things for the cmd line to parse it correctly)

The script prints out the top 10 ranked similar items, with their urls and scores.

I added an option to visualize the input and output images, but this option doesn't seem to work within Docker. 
Therefore the `--viz` flag is defaulted to FALSE. But if running locally, this flag can be enabled to visualize how good the matches are. 


