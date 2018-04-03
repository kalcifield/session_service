from flask import Flask, request, jsonify
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


@app.route('/api/session/load', methods=['POST'])
def load_session():
    session_id = request.json["sessionId"]
    db = Dynamodb()
    user_id = db.load(session_id)
    return jsonify({"userId": user_id})


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
