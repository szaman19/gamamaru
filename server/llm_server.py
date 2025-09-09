from flask import Flask, request, jsonify
from ollama import Client
from flask_cors import CORS

model = Client()

app = Flask(__name__)
CORS(app)

system_prompt = """You are a helpful writing assistant and editor. 
You will be provided with text a user is writing.
Your job is to help the user write and edit the text."
You should fix any spelling or grammar mistakes and rewrite the text in a clear and concise manner.
Don't add any new information that is not in the original text. 
Use the Article Goal given by the user to guide your edits. 
Parts of the text that are correct should be left unchanged.
If the user provides a specific instruction, follow that instruction.
"""


@app.route("/gen_text", methods=["POST"])
def chat():

    user_message = None
    try:
        assert request.is_json
        assert request.json is not None
        assert "text" in request.json
        user_message = request.json.get("text")
    except Exception as e:
        return jsonify({"error": "Invalid input"}), 400

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    prompt = f"{system_prompt}\n\n{user_message}\n\nEdited Text:"
    response = model.generate(
        model="gpt-oss:20b",
        prompt=prompt,
    )
    response_text = None
    try:
        assert response is not None
        response_text = response["response"]
    except Exception as e:
        return jsonify({"error": "No response from model"}), 500
    if not response_text:
        return jsonify({"error": "Empty response from model"}), 500

    print(f"User Message: {user_message}")
    print(f"Response Text: {response_text}")
    return jsonify({"completed_text": response_text})


if __name__ == "__main__":
    app.run(debug=True)
