from revChatGPT.V1 import Chatbot
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
import os


app = Flask(__name__)
if(os.getenv("EMAIL") is None or os.getenv("PASSWORD") is None):
    print("Please set your email and password in the .env file")
    exit(1)


@app.route("/chatgpt/", methods=["POST"])
def chat():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data provided"}), 400
    if data["text"] is None:
        return jsonify({"error": "No text provided"}), 400
    if data["text"] == "":
        return jsonify({"error": "Empty text provided"}), 400
    res = chatgpt(data["text"], data["conversation_id"])
    return jsonify({
        "response": res[0],
        "conversation_id": res[1]
    }), 200



def chatgpt(str, cid=None):
    chatbot = Chatbot(config={
      "email": os.getenv("EMAIL"),
      "password": os.getenv("PASSWORD")
    })
    prev_text = ""
    result = ""
    for data in chatbot.ask(
        str,
    ):
        message = data["message"][len(prev_text) :]
        result = result + message
        prev_text = data["message"]
    return [result, data["conversation_id"]]


if __name__ == "__main__":
    app.run(debug=True)