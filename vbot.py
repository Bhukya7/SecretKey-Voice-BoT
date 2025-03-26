from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

def initialize_openai():
    """Initialize OpenAI client"""
    try:
        api_key = os.getenv("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")
        if not api_key:
            # raise ValueError("OPENAI_API_KEY not found in .env file")
        return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"OpenAI Initialization Error: {e}")
        return None

client = initialize_openai()

def get_secretkey_response(question):
    """Get response from either predefined answers or OpenAI"""
    predefined_responses = {
        "what should we know about your life story": "I'm SecretKey, an AI assistant created to help with information and tasks.",
        "what's your #1 superpower": "My superpower is processing information quickly to give you accurate answers.",
        "what are the top 3 areas you'd like to grow in": "1) Better understanding of emotions 2) Creative problem solving 3) Technical knowledge",
        "what misconception do people have about you": "That I'm just a simple chatbot, when I'm actually quite sophisticated!",
        "how do you push your boundaries": "By constantly learning from new interactions and challenges."
    }
    
    question_lower = question.lower()
    for key in predefined_responses:
        if key in question_lower:
            return predefined_responses[key]
    
    try:
        if not client:
            return "I'm having trouble connecting to my knowledge base."
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are SecretKey, a helpful AI assistant. Keep responses under 2 sentences."},
                {"role": "user", "content": question}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return "I'm having some technical difficulties. Could you ask again?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'response': 'Please ask a question!'})
    
    if "stop" in question.lower() or "exit" in question.lower():
        return jsonify({'response': 'Goodbye! I\'m stopping now.', 'stop': True})
        
    response = get_secretkey_response(question)
    return jsonify({'response': response, 'stop': False})

if __name__ == "__main__":
    app.run(debug=True)
