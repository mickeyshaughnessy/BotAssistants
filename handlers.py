import requests, redis, time, json
import config, utils, uuid
from prompts import chat as _chat
from prompts import coach as _coach 

redis = redis.StrictRedis()

def conversation(req):
    """ you can append or get conversations"""
    username = req.get('username',"")
    user_id = utils.username_to_user_id(username)
    conversation_id = str(uuid.uuid4())
    redis.hset(config.REDHASH_CONVERSATIONS, conversation_id, "{}")
    return conversation_id

def user(req):
    username = req.get('username',"")
    user_id = utils.username_to_user_id(username)
    
    try:
        record = json.loads(redis.hget(config.REDHASH_USERS, user_id))
    except Exception as e:
        record = {"created_on":"%s" % int(time.time())}
    
    mod = req.get('modification',{})
    if mod: record.update(mod)
     
    redis.hset(config.REDHASH_USERS, user_id, json.dumps(record)) 
    return {} 

def chat(req):

    #chat_history = get_history(request)
    username, _input = req.get('username', 'No user'), req.get('text',"")

    data={
        "prompt" : 
            _chat.CHAT_PREFIX.format(personality="Beth") + 
            #prompts.COACH_SYSTEM.format(available_plugins=["**LTM**"]) +
            _coach.COACH_INPUT.format(user_input=_input,username=username),
    
        "n" : 1, # number of completions
        "model": "text-davinci-003",
        "temperature": 1.1,
        "max_tokens": 200
    }

    print(data)

    headers = {"Authorization": "Bearer %s" % config.openai_api_key, "Content-Type" : "application/json"}
    full_resp = requests.post(config.openai_url, headers=headers, json=data)
    print(full_resp)
    _resp = full_resp.json().get("choices", [])[0].get('text')
    print(_resp)
    return _resp
