import urllib.request
import urllib.parse
import json

with open("valentino_links.csv") as f:
    lines = f.readlines()

catalog = []
cnt = 0
for ind, l in enumerate(lines[1:]):
    l = l.strip('\n')
    try:
        if l.startswith('"') and l.endswith('"'):
            l = l.strip('"')
        elif l.endswith('"'):
            # second half of a single line
            continue
        elif l.startswith('"'):
            # handle url split into 2 lines
            l += lines[ind+2].strip('\n')
            l = l.strip('"')

        l = l.replace("Ò","%C3%92").replace("É", "%C3%89").replace("È", "%C3%88")
        l = l.replace("®", "%C2%AE").replace(" ", "+").replace(" ", "%C2%A0")
        urllib.request.urlretrieve(l, f"imgs/img_{ind:04d}.jpg")
        catalog.append({"id": cnt, "name": f"img_{ind:04d}.jpg", "url": l})
        cnt += 1
    except:
        print(ind,l)

print("downloaded:", cnt)
with open('catalog.json', 'w') as f:
    json.dump(catalog, f, indent=4)




