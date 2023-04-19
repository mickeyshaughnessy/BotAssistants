from googlesearch import search   

query = "Denver bounce house rental"

links = []
for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
    links.append(j)

for l in links:
    print(l) 
