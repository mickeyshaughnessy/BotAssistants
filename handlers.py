import requests, redis, time, json
import config, utils, uuid
from prompts import chat as _chat
from prompts import coach as _coach 
from models import User, Conversation

redis = redis.StrictRedis()

def login(req):
    token = str(uuid.uuid4())
    return {'user_id':'', 'token':token}

def authenticate(action, user, conversation):
    pass
 
def manage(req):
    user_id = req.get('user_id')
    conversation_id = req.get('conversation_id')
    user, conversation =  models.User(user_id), models.Conversation(conversation)
    action = req.get('action') # action is json object describing the action (modifiying conversation, modifying user data)
    authed = authenticate(action, user, conversation)

def chat(req):

    #chat_history = get_history(request)

    user_id, _input = req.get('user_id', 'No user_id'), req.get('text',"")

    data={
        "prompt" : 
            _chat.CHAT_PREFIX.format(personality="Beth") + 
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
