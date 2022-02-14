from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "my secret key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#Store survey answers in list
responses = []

@app.route('/')
def index():
    """Show homepage to start survey."""
    return render_template('index.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)
 
@app.route('/questions/<int:q_number>')
def show_question(q_number):
    """Show the current question."""
    question = satisfaction_survey.questions[q_number]
    return render_template('question.html', title=satisfaction_survey.title, question=question, q_number=q_number)

@app.route('/answers', methods=['POST'])
def submit_answer():
    """Add answer to responses list and redirect."""
    q_number = int(request.form['q_number'])
    ans = list(request.form.keys())[0]
    responses.append(ans)
    return redirect(f'/questions/{q_number + 1}')