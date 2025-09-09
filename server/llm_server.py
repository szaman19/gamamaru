from flask import Flask, request, jsonify
from ollama import Client

model = Client()

app = Flask(__name__)

system_prompt = """You are a helpful writing assistant and editor. 
You will be provided with text a user is writing.
Your job is to help the user write and edit the text."
You should fix any spelling or grammar mistakes and write in a clear and concise manner."""

@app.route('/gen_text', methods=['POST'])
def chat():
    
    user_message = None
    try:
      user_message = request.json.get('text')
    except Exception as e:
      return jsonify({"error": "Invalid input"}), 400
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    prompt = f"{system_prompt}\n\nUser Text: {user_message}\n\nEdited Text:"
    response = model.generate(
        model="gpt-oss:20b",
        prompt=prompt,
    )
    response_text = response.get("choices", [{}])[0].get("text", "").strip()
    return jsonify({"completed_text": response_text})

if __name__ == '__main__':
    app.run(debug=True)
