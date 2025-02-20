from flask import Flask, request, jsonify, render_template
import ollama  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def call_model(prompt):
    try:
        response = ollama.chat(model="orca-mini", messages=prompt)
        return response.get("text", "No response received from the model.")
    except Exception as e:
        print("Error")
        return e

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    print(f"User input: {user_input}")
    prompt = f"Generate a detailed travel itinerary based on this input : {user_input}."
    bot_response = call_model(prompt)
    return jsonify({'bot_response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
