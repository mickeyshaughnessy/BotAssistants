import sys, requests, json

url = sys.argv[1]
if len(sys.argv > 1):
    params = json.loads(sys.argv[2])
else:
    params = {}

resp = requests.get(url, params=params)

print json.loads(resp.json())
