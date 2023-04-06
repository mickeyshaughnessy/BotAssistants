
# This is the API server for the conversation platform

# It has a user REST API:

# POST /chat
# request = {
#    "user_id" : <user_id>,
#    "text" : <params_json>
#    }

import json, uuid, redis
from flask import Flask, jsonify, request
from flask_cors import CORS
import utils, handlers, config

redis = redis.StrictRedis()

app = Flask(__name__)
CORS(app)

@app.route("/ping", methods=['GET'])
def ping():
    return json.dumps({"message" : "ok"})

@app.route("/conversation", methods=['POST', 'GET'])
def conversation():
    req = request.get_json()
    resp = handlers.conversation(req)
    return {}

@app.route("/user", methods=['POST', 'GET'])
def user():
    req = request.get_json()
    resp = handlers.user(req)
    return {}

@app.route("/reporting", methods=['POST'])
def reporting():
    req = request.get_json()
    return {}

@app.route("/chat", methods=['POST','GET'])
def chat():
    try:
        req = request.get_json()
    except:
        req = {} 
    resp = handlers.chat(req)
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8010)
