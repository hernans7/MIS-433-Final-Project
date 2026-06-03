from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "CineScope API is running ✅"

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
