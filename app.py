from flask import Flask, request, jsonify, render_template
import ollama  
from fais_test import travel_embeddings, query_input
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def extract(user_input):
    extract_prompt=("Extract the following details from the user's travel request: destination, budget "
        "(e.g., 'luxury', 'budget-friendly'), duration (e.g., '5 days'), and trip type "
        "(e.g., 'family vacation', 'adventure trip').\n"
        "Return the output in JSON format with keys: 'destination', 'budget', 'duration', 'trip_type'.\n"
        f"User prompt: \"{user_input}\""
        )
    response=call_model(extract_prompt)
    try:
        details = json.loads(response)
    except Exception as e:
        details = {
            "destination": "Unknown",
            "budget": "Unknown",
            "duration": "Unknown",
            "trip_type": "Unknown"
        }
    return details

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
    details=extract(user_input)
    index, travel_data = travel_embeddings(details['destination'])
    res=query_input(index, travel_data, details['destination'])
    #print(f"User input: {user_input}")
    prompt=(f"Generate a detailed travel itinerary for a {details['trip_type']} in {details['destination']} "
           f"for {details['duration']} with a {details['budget']} budget."
           f"Include the following attractions: {res}."
           )
    bot_response=call_model(prompt)
    return jsonify({'bot_response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
