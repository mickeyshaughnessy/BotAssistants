import requests, time, config

user_id = '123'
conversation_id = 9

while True:
    chat = input("User_%s: " % user_id)
    #resp = requests.post("http://127.0.0.1:8010/reporting", json={"input" : chat, "user_id":user_id})
    #resp = requests.post("http://3.89.10.143:8010/chat", json={"text" : chat, "user_id":user_id})
    resp = requests.post("http://0.0.0.0:%s/chat" % config.api_port, json={"text" : chat, "user_id":user_id, "conversation_id":conversation_id})
    print(resp.text)
    time.sleep(1)
