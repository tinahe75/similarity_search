from flask import Flask, jsonify, request
import json
import numpy as np

url_to_id = dict()
id_to_url = dict()
K = 10   # top K most similar

with open("catalog.json", "r") as f:
    catalog = json.load(f)

for elem in catalog:
    url_to_id[elem['url']] = elem['id']
    id_to_url[elem['id']] = elem['url']

catalog_embeddings = np.load("catalog_embeddings.npy")


def compute_similarity(ind):
    q = catalog_embeddings[ind]
    res = catalog_embeddings @ q.T   # dot product to measure similarity
    indices_of_top_n = np.argsort(res)[-1-K:-1][::-1]
    most_similar = []
    scores = []
    for i in indices_of_top_n:
        # print(res[i])
        # print(id_to_url[i])
        most_similar.append(id_to_url[i])
        scores.append(str(res[i]))
    return most_similar, scores


app = Flask(__name__)


@app.route('/img_search', methods=['POST'])
def get_similar_image_urls():
    try:
        print("received", request.json['url'])
        query_url = request.json['url']
        query_id = url_to_id[query_url]
        similar_urls, scores = compute_similarity(query_id)
        return jsonify({'similar_urls': similar_urls, 'scores': scores})
    except:
        return jsonify({'error': 'Invalid input url!'})


if __name__ == '__main__':
    app.run(debug=True)
