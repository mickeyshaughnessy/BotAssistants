import config, hashlib

def username_to_user_id(username):
    return hashlib.md5((username + config.salt).encode()).hexdigest() 
