import utils, redis, json
import config

redis = redis.StrictRedis()

class User():
    def __init__(self, user_id=None):
        pass

class Conversation():
    def __init__(self, conversation_id=None):
        if conversation_id:
            self.load(conversation_id) 
        else:
            conversation_id = str(uuid.uuid4())
            self.transcript = []
            self.save()

    def load(self, convo_id):
        res = redis.hget(config.REDHASH_CONVERSATION, convo_id)
        if res:
            cur = json.loads(res)

    def save(self, convo_id):
        current = redis.hget(config.REDHASH_CONVERSATION, self.convo_id)
        
    ## create, update, or fetch a conversation ##
    ## the idea is users have privileges to do operations on conversations

    ## create ##
    redis.hset(config.REDHASH_CONVERSATIONS, conversation_id, "{}")
    return conversation_id

if __name__ == "__main__":
    # Put tests here, __main__ only runs when models.py is run from command line
    req = {
        "user_id" : "testuser1",
        "conversation_id" : "testconvo1",
        "action" : "POST testconvo1",
    }

    user = User(req.get('user_id'))
    convo = Conversation(req.get('conversation_id'))
    

