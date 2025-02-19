from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input")  
    print(f"User input: {user_input}")
    bot_response = f"You said: {user_input}"

    return jsonify({'bot_response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
