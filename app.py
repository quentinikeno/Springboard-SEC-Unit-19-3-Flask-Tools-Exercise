from flask import Flask, request, render_template, redirect, flash
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
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('index.html', title=title, instructions=instructions)
 
@app.route('/questions/<int:q_number>')
def show_question(q_number):
    """Show the current question."""
    num_responses = len(responses)

    #Redirect to thank you page if all questions are answered
    if(num_responses == len(satisfaction_survey.questions)):
        flash('You have already completed the survey.', 'warning')
        return redirect('/thank-you')

    #Check that the question number in URL is correct
    if(q_number != num_responses):
        #Redirect to correct question
        flash('You are trying to answer an invalid question.  Please answer the question below.', 'error')
        return redirect(f'/questions/{num_responses}')
    
    question = satisfaction_survey.questions[q_number]
    title = satisfaction_survey.title
    return render_template('question.html', title=title, question=question, q_number=q_number)

@app.route('/answers', methods=['POST'])
def submit_answer():
    """Add answer to responses list and redirect."""
    q_number = int(request.form['q_number'])
    ans = request.form.get('response')
    responses.append(ans)
    if(q_number + 1 == len(satisfaction_survey.questions)):
        #Redirect to thank you page if answered last question
        return redirect('/thank-you')
    return redirect(f'/questions/{q_number + 1}')

@app.route('/thank-you')
def show_thank_you():
    title = satisfaction_survey.title
    return render_template('thank_you.html', title=title)