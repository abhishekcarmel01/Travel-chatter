from flask import Flask, request, jsonify, render_template
import ollama  
from fais_test import travel_embeddings, query_input

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def call_model(prompt):
    try:
        response = ollama.chat(model="orca-mini", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "No response received from the model.")
    except Exception as e:
        print("Error")
        return e

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")
    index, travel_data = travel_embeddings(user_input)
    res=query_input(index, travel_data, user_input)
    #print(f"User input: {user_input}")
    prompt = (f"Generate a detailed travel itinerary for {user_input}. "
              f"Include information about this attraction: {res}")
    bot_response = call_model(prompt)
    return jsonify({'bot_response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
