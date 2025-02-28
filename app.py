from flask import Flask, request, jsonify, render_template
import ollama  
from chroma import travel_embeddings, query_input
import json
from dotenv import load_dotenv
import os
from flask_session import Session
import spacy 

nlp = spacy.load("en_core_web_sm")

load_dotenv()
SECRET_KEY=os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
app.config('SECRET_KEY')=SECRET_KEY
app.config('sESSION_TYPE')='filesystem'
Session(app)

@app.route('/')
def home():
    Session['history']=[]
    Session['travel_data']=[]
    return render_template('index.html')

def initial_prompt(res):
    return( "You are a travel assistant that will build travel iternaries based on user's needs"
           f"Include the following attractions: {res}."
           )
def extract(user_input):
    doc=nlp(user_input)
    dest=[ent.text for ent in doc.ents if ent.label_=="GPE"]
    return dest[0]
def build_prompt(conv_history,user_prompt):
    history="\n".join(conv_history)
    prompt=f"{history}\nUser: {user_prompt}\nBot:"
    return prompt

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
    conv_history = Session.get('history', [])
    travel_data = Session.get('travel_data', [])
    if not travel_data or user_input.lower().find(travel_data['destination'].lower()) == -1:
        travel_data = extract(user_input)
        Session['travel_data']=travel_data
        collec=travel_embeddings(travel_data['destination'])
        res=query_input(collec, user_input)
        conv_history.append(f"System: {initial_prompt(res)}")
    #print(f"User input: {user_input}")
    full_prompt=build_prompt(conv_history, user_input)
    bot_response=call_model(full_prompt)
    conv_history.append(f"User: {user_input}\nBot: {bot_response}")
    Session['history']=conv_history
    return jsonify({'bot_response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
