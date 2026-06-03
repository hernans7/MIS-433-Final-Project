from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
 
app = Flask(__name__)
CORS(app)  # allows your frontend to call this server
 
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
 
@app.route("/")
def home():
    return "CineScope API is running ✅"
 
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
 
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
 
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
 
    return jsonify({"response": message.content[0].text})
 
if __name__ == "__main__":
    app.run(debug=True)
