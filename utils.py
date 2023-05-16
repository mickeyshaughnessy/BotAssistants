import json, redis, config, hashlib

redis = redis.StrictRedis()

#def username_to_user_id(username):
#    return hashlib.md5((username + config.salt).encode()).hexdigest()
# keep it vanilla

def get_history(conversation_id):
    history = redis.hget(config.REDHASH_CONVERSATION, "conversation_%s" % conversation_id)
    if history:
        history = json.loads(history)
    else:
        history = {}
    return history

def update_transcript(conversation_id, update):
    # when a client connects it creates or loads a conversation
    history = redis.hget(config.REDHASH_CONVERSATION, "conversation_%s" % conversation_id)
    if history:
        history = json.loads(history)
    else:
        history = {"users" : [], "transcript" : ""}

    history['transcript'] += update 
    history = json.dumps(history)
    redis.hset(config.REDHASH_CONVERSATION, "conversation_%s" % conversation_id, history)
