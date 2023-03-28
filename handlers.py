import requests
import config
from prompts import chat as _chat
from prompts import coach as _coach 

def chat(req):

    #chat_history = get_history(request)
    username, _input = req.get('username', 'No user'), req.get('input', "Football is")

    data={
        "prompt" : 
            _chat.CHAT_PREFIX.format(personality="Beth") + 
            #prompts.COACH_SYSTEM.format(available_plugins=["**LTM**"]) +
            _coach.COACH_INPUT.format(user_input=_input),
    
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
