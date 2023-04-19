import sys, requests, json

url = sys.argv[1]
body = json.loads(sys.argv[2])

resp = requests.post(url, json=body)

print json.loads(resp.json())
