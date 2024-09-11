from flask import Flask, render_template, request, jsonify
import uuid
from answers_handling import answer_questions
from send_mail import send_email
from vector_stores import get_session_history


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
    department = data.get('department')
    
    if field in ['1', '2', '3']:
        answer = answer_questions(session_id, question, department)
    else:
        answer = "Invalid field selected."
    
    return jsonify({'content': answer})


@app.route('/raiseconcernmail', methods=['POST'])
def raise_concern():
    try:
        data = request.json
        department = data.get('department')
        session_id = data.get('token')
        sender = 'admin@techinterrupt.com'
        if department == 'Finance':
            receiver = 'finance@techinterrupt.com'
            subject = 'Finance Query'
        elif department == 'Human Resources':
            receiver = 'hr@techinterrupt.com'
            subject = 'HR Query'
        elif department == 'Operations':
            receiver = 'operations@techinterrupt.com'
            subject = 'Operations Query'
        send_email(sender, receiver, subject, get_session_history(session_id))
        return jsonify({'success': True, 'message': 'Concern raised successfully'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)