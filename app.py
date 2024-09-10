from flask import Flask, render_template, request, jsonify
import uuid
from finanace_answers import answer_finance_questions
from hr_answers import answer_hr_questions
from operation_answers import answer_operation_questions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    print(data)
    field = data.get('field')  
    question = data.get('question')

    if field == '1':  
        answer = answer_hr_questions(uuid.uuid4(), question)
    elif field == '2':  
        answer = answer_operation_questions(uuid.uuid4(), question)
    elif field == '3': 
        answer = answer_finance_questions(uuid.uuid4(), question)
    else:
        answer = "Invalid field selected."

    return jsonify({'content': answer})


if __name__ == '__main__':
    app.run(debug=True)