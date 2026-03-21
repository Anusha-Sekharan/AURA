from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

from listener import Listener
from speaker import Speaker
from brain import Brain
from executor import Executor

app = Flask(__name__)
CORS(app) # Allow Electron UI to connect

# Initialize Aura components globally
ear = Listener()
mouth = Speaker()
brain = Brain()
hand = Executor(mouth)

@app.route('/api/chat', methods=['POST'])
def process_chat():
    data = request.json
    text = data.get('message', '')
    
    if not text:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        # Think
        command = brain.process(text)
        
        response_text = command.get("response", "")
        action = command.get("action")
        parameter = command.get("parameter")
        action_result = ""
        
        # We need to run speaking and executing in a background thread 
        # so we don't block the HTTP response from returning immediately
        def run_actions():
            if response_text:
                mouth.speak(response_text)
                
            if action and action != "chat":
                res = hand.execute(action, parameter)
                # the result of the action is handled synchronously below
        
        # Just run action synchronously for the API so the UI gets the result
        if action and action != "chat":
             action_result = hand.execute(action, parameter)
             
        # Speak asynchronously
        if response_text or action_result:
             speak_text = response_text
             if action_result:
                 speak_text += ". " + action_result
                 
             threading.Thread(target=mouth.speak, args=(speak_text,), daemon=True).start()
             
        return jsonify({
            "response": response_text,
            "action": action,
            "action_result": action_result
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on localhost
    app.run(host='127.0.0.1', port=5000, debug=False)
