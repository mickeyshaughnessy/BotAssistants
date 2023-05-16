import requests, redis, time, json
import config, uuid
from prompts import chat as _chat
from prompts import coach as _coach 
import utils


redis = redis.StrictRedis()

def login(req):
    token = str(uuid.uuid4())
    return {'user_id':'', 'token':token}

def conversation(req):
    ## create, update, or fetch a conversation ##
    ## the idea is users have privileges to do operations on conversations

    """ you can append or get conversations"""
    user_id = req.get('user_id',"")
    #user_id = utils.user_id_to_user_id(user_id)
    
    ## create ## 
    conversation_id = str(uuid.uuid4())
    redis.hset(config.REDHASH_CONVERSATIONS, conversation_id, "{}")
    return conversation_id

#def user(req):
#    user_id = req.get('user_id',"")
#    user_id = utils.user_id_to_user_id(user_id)
#    
#    try:
#        record = json.loads(redis.hget(config.REDHASH_USERS, user_id))
#    except Exception as e:
#        record = {"created_on":"%s" % int(time.time())}
#    
#    mod = req.get('modification',{})
#    if mod: record.update(mod)
#     
#    redis.hset(config.REDHASH_USERS, user_id, json.dumps(record)) 
#    return {} 

def chat(req):

    # first thing, we get the conversation id.
    conversation_id = req.get("conversation_id", int(uuid.uuid4()))
    # if no id, then make one.

    chat_history = utils.get_history(conversation_id)
    transcript = chat_history.get('transcript', "")

    user_id, _input = req.get('user_id', 'No user_id'), req.get('text',"")

    data={
        "prompt" : 
            _chat.CHAT_PREFIX.format(personality="Beth") + 
            _chat.CHAT_BODY.format(transcript=transcript)
            #prompts.COACH_SYSTEM.format(available_plugins=["**LTM**"]) +
            _coach.COACH_INPUT.format(user_input=_input,user_id=user_id),
    
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
