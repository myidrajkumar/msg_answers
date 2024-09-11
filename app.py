from flask import Flask, render_template, request, jsonify
import uuid
from finanace_answers import answer_finance_questions
from hr_answers import answer_hr_questions
from operation_answers import answer_operation_questions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token', methods=['GET'])
def get_token():
    session_id = str(uuid.uuid4())
    return jsonify({'token': session_id})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    field = data.get('field')  
    question = data.get('question')
    session_id = data.get('token')
    
    if field == '1':  
        answer = answer_hr_questions(session_id, question)
    elif field == '2':  
        answer = answer_operation_questions(session_id, question)
    elif field == '3': 
        answer = answer_finance_questions(session_id, question)
    else:
        answer = "Invalid field selected."

    return jsonify({'content': answer})

if __name__ == '__main__':
    app.run(debug=True)