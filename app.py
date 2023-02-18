from revChatGPT.V1 import Chatbot
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
load_dotenv()
import os
import json


app = Flask(__name__)
if(os.getenv("EMAIL") is None or os.getenv("PASSWORD") is None):
    print("Please set your email and password in the .env file")
    exit(1)


@app.route("/chatgpt/", methods=["POST"])
def chat():
    data = request.get_json()
    if data.get("text") is None:
        return jsonify({"error": "Please provide text"})
    res = chatgpt(data.get("text"), data.get("conversation_id"))
    response = Response(jsonify({"text": res[0], "conversation_id": res[1]}))
    response.headers["Content-Type"] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



def chatgpt(str, cid=None):
    chatbot = Chatbot(config={
      "email": os.getenv("EMAIL"),
      "password": os.getenv("PASSWORD")
    })
    prev_text = ""
    result = ""
    for data in chatbot.ask(str, cid):
        message = data["message"][len(prev_text) :]
        result = result + message
        prev_text = data["message"]
    return [result, data["conversation_id"]]


if __name__ == "__main__":
    app.run(debug=True)