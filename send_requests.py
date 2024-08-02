import requests
import imageio
import json
import argparse

OKBLUE = '\033[94m'
ENDC = '\033[0m'
OKGREEN = '\033[92m'

with open("catalog.json","r") as f:
    catalog = json.load(f)


def preprocess_input_url(l):
    l = l.replace("Ò", "%C3%92").replace("É", "%C3%89").replace("È", "%C3%88")
    l = l.replace("®", "%C2%AE").replace(" ", "+").replace(" ", "%C2%A0")
    return l


def send_request(search_url, viz=False):
    if viz:
        import cv2
    # URL of the Flask server
    url = 'http://127.0.0.1:5000/img_search'

    # first replace special chars
    search_url = preprocess_input_url(search_url)
    input_data = {'url': search_url}

    # send request
    try:
        response = requests.post(url, json=input_data)
        response.raise_for_status()
        response = response.json()

        if 'similar_urls' in response:
            similar_urls = response['similar_urls']
            scores = response['scores']

            if viz:
                # display input image corresponding to search url
                image = imageio.v2.imread(search_url)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow('input', image)
                cv2.waitKey(0)
            else:
                print("\n\n##################################")
                print("      finding similar images")
                print("##################################\n")
                print(OKBLUE + f"search url:  {search_url}\n\n" + ENDC)

            # print rank info + similarity score
            print("top 10 similar items:\n")
            for rank, (l, s) in enumerate(zip(similar_urls, scores)):
                if viz:
                    # display similar results in database
                    image = imageio.v2.imread(l)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    cv2.putText(image, f"rank:  {rank + 1}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(image, "similarity score: " + s, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.imshow('similar', image)
                    cv2.waitKey(0)
                else:
                    print(OKGREEN + f"rank: {rank+1}" + ENDC)
                    print(OKGREEN + "url: " + ENDC, l)
                    print(OKGREEN + "similarity score: " + ENDC, s + "\n")
        else:
            print("\n\n##################################")
            print(f"search url:  {search_url}\n")
            print(response + "\n")   # print error response
    except:
        print("Error sending request! Please check if service is online.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--viz", type=bool, default=False,
                        help="visualize input and matched items, default=FALSE")
    parser.add_argument("--lookup", type=int, default=-1,
                        help="lookup index. Database contains 2652 items. Select from [0, 2651] ")
    parser.add_argument("--url", type=str, default="", help="lookup url. Provide url directly.")
    args = parser.parse_args()

    if args.lookup == -1 and not args.url:
        raise Exception("Please provide either lookup index or url!")

    if args.url:
        send_request(args.url, args.viz)
    elif args.lookup > 2651 or args.lookup < 0:
        raise Exception("Invalid lookup index! Please select from 0 to 2651")
    else:
        send_request(catalog[args.lookup]['url'], args.viz)
