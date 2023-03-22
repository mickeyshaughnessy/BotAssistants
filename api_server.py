# This is the API server for the conversation platform

# It has a user REST API:

# POST /chat
# request = {
#    "user_id" : <user_id>,
#    "text" : <params_json>
#    }

import json
import redis
from flask import Flask, jsonify, request
from flask_cors import CORS
#import handlers

redis = redis.StrictRedis()

app = Flask(__name__)
CORS(app)

@app.route("/ping", methods=['GET'])
def ping():
    return json.dumps({"message" : "ok"})

@app.route("/chat", methods=['POST','GET'])
def chat():
    try:
        req = request.get_json()
    except:
        pass
    #resp = handlers.chat(req)
    resp = json.dumps({"message" : "ok chat"}) 
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8010)
