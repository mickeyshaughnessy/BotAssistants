import redis, config, hashlib

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

def update_history(update, user_id, conversation_id):
    # when a client connects it creates or loads a conversation
    history = redis.hget(config.REDHASH_CONVERSATION, "conversation_%s" % conversation_id)
    if history:
        history = json.loads(history)
    else:
        history = {"users" : [user_id], "transcript" : ""}


    history['transcript'] += "User_%s" % user_id + update.get('input')
    history.update(update)
    history = json.dumps(history)
    redis.hset(config.REDHASH_CONVERSATION, "conversation_%s" % conversation_id, history)
