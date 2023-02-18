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


@app.route("/chatgpt/", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    data = request.get_json()
    if data.get("text") is None:
        err_resp = Response("Please provide a text to chat with")
        err_resp.headers['Access-Control-Allow-Origin'] = '*'
        return err_resp
    res = chatgpt(data.get("text"), data.get("conversation_id"))
    response = Response(JSON.stringify(res[0]))
    response.headers['conversation_id'] = res[1]
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['content-type'] = 'application/json'
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