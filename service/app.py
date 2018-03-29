from flask import Flask, render_template, url_for, request, jsonify
import json
from session_generator import SessionGenerator
from database import Dynamodb

with open("../config.json") as json_data:
    config = json.load(json_data)

app = Flask(__name__)


@app.route('/api/session/create', methods=['POST'])
def create_session():
    user_id = request.json["userId"]
    session_id = SessionGenerator.generate_session_id(user_id)
    db = Dynamodb()
    db.save_session(user_id, session_id)
    return jsonify({"sessionId": session_id})


# Create an endpoint that receives {sessionId: x} as a json, and responds with {userId: 1} as a json. (/api/session/load)
# Implement and test session loading - load the item,
# if (exists, obviously, and) it is created in the last 8 hours, and lastUsed in the last 5 minutes
# - return null otherwise.
@app.route('/api/session/load', methods=['POST'])
def load_session():
    session_id = request.json["sessionId"]
    db = Dynamodb()
    user_id = db.load(session_id)
    return jsonify({"userId": user_id})


# Create an endpoint that receives {sessionId: x} as a json, and responds with {success: true} as a json. (/api/session/renew)
# Implement and test session renewing - update lastUsed if the session is still valid (based on lastUsed and created).
@app.route('/api/session/renew', methods=['POST'])
def renew_session():
    session_id = request.json["sessionId"]
    db = Dynamodb()
    response_bool = db.renew(session_id)
    return jsonify({"success": response_bool})


@app.route('/api/session/delete', methods=['POST'])
def delete_session():
    session_id = request.json["sessionId"]
    db = Dynamodb()
    response_bool = db.delete(session_id)
    return jsonify({"success": response_bool})


if __name__ == '__main__':
    app.run(host=config["host"], port=config["port"], debug=True)
