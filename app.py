from flask import Flask, render_template, request, jsonify
import uuid
from hr_answers import answer_hr_questions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    answer = get_answer(question)
    return answer

def get_answer(question):
    sessionid = uuid.uuid4()
    return (answer_hr_questions(sessionid, question))


if __name__ == '__main__':
    app.run(debug=True)