import utils, redis, json
import config

redis = redis.StrictRedis()

class User():
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.data = {}

    def post(self, conversation_id, message):
        requests.post("localhost:%s/chat/", json.dumps({
            "message" : message,
            "conversation_id" : conversation_id
        })) 
    

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
        else:
            cur = {}
        return cur 

    def update(self, update={"text":None}):
        current = redis.hget(config.REDHASH_CONVERSATION, self.convo_id)
        if current:
            transcript = json.loads(current).get('transcript')
            if update.get('text'):
                transcript.append(update['text'])
                current['transcript'] = transcript 
        else:
            current = {"transcript" : []}
       
        redis.hset(config.REDHASH_CONVERSATION, self.convo_id, json.dumps(current))
        

if __name__ == "__main__":
    # Put tests here, __main__ only runs when models.py is run from command line
    req = {
        "user_id" : "testuser1",
        "conversation_id" : "testconvo1",
        "action" : "POST testconvo1 {'text' : 'new message!'}",
    }

    user = User(req.get('user_id'))
    convo = Conversation(req.get('conversation_id'))
    
    

