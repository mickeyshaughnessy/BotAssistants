import requests, redis, time, json
import config, uuid
from prompts import chat as _chat
from prompts import coach as _coach 
import utils


redis = redis.StrictRedis()

def login(req):
    token = str(uuid.uuid4())
    return {'user_id':'', 'token':token}

def conversations(req):
    user_id = req.get('user_id',"")
   
    action = req.get("action") # one of create, join, share, delete, set_name

    ## share ##
    ## delete ##
    ## set_name ##
    ## create ## 
    conversation_id = str(uuid.uuid4())
    redis.hset(config.REDHASH_CONVERSATIONS, conversation_id, json.dumps({"conversation_id":conversation_id}))
    return conversation_id

    ## join ##
    conversation_id = req.get("conversation_id","")
    conversation = redis.hget(config.REDHASH_CONVERSATIONS, conversation_id)
    if conversation:
        conversation = json.loads(conversation)
    else:
        conversation = {}
    return conversation

def chat(req):

    # first thing, we get the conversation id.
    conversation_id = req.get("conversation_id", int(uuid.uuid4()))
    # if no id, then make one.

    chat_history = utils.get_history(conversation_id)
    transcript = chat_history.get('transcript', "")

    _id, _input = req.get('user_id', 'No user_id'), req.get('text',"")

    _personality="Sober Coach"

    data={
        "prompt" : 
            _chat.CHAT_PREFIX.format(personality=_personality) + 
            _chat.CHAT_BODY.format(transcript=transcript) +
            _coach.COACH_SYSTEM +
            _chat.CHAT_SUFFIX.format(user_input=_input, user_id=_id, personality=_personality),
    
        "n" : 1, # number of completions
        "model": "text-davinci-003",
        "temperature": 1.1,
        "max_tokens": 200
    }

    print(data)

    headers = {"Authorization": "Bearer %s" % config.openai_api_key, "Content-Type" : "application/json"}
    full_resp = requests.post(config.openai_url, headers=headers, json=data)
    #print(full_resp)
    _resp = full_resp.json().get("choices", [])[0].get('text')
    utils.update_transcript(conversation_id, _chat.CHAT_UPDATE.format(
        user_input=_input,
        user_id=_id,
        personality=_personality,
        response=_resp
        )) 
    print(_resp)
    return json.dumps({"response" : _resp})
