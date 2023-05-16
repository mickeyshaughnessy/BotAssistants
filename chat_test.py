import requests, time

user_id = '123'

while True:
    chat = input("User_%s: " % user_id)
    #resp = requests.post("http://127.0.0.1:8010/reporting", json={"input" : chat, "user_id":user_id})
    #resp = requests.post("http://3.89.10.143:8010/chat", json={"text" : chat, "user_id":user_id})
    resp = requests.post("http://0.0.0.0:8010/chat", json={"text" : chat, "user_id":user_id, "conversation_id":69})
    print(resp.text)
    time.sleep(1)
