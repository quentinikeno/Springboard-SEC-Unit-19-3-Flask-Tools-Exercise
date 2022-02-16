from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "my secret key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def index():
    """Show homepage to start survey."""
    return render_template('index.html', surveys=surveys.keys())

@app.route('/survey-select', methods=['POST'])
def pick_survey():
    #Store selected survey name (key in surveys dictionary) in session
    #Use this to access the appropriate survey
    session['survey'] =  request.form.get('surveys')
    return redirect('/start-page')

@app.route('/start-page')
def show_start_page():
    """Show homepage to start survey."""
    survey = surveys[session['survey']]
    title = survey.title
    instructions = survey.instructions
    return render_template('start_page.html', title=title, instructions=instructions)

@app.route('/init-survey', methods=['POST'])
def intialize_survey():
    #Store responses as a list in session
    session['responses'] = dict()
    return redirect('/questions/0')
 
@app.route('/questions/<int:q_number>')
def show_question(q_number):
    """Show the current question."""
    survey = surveys[session['survey']]
    num_responses = len(session['responses'])

    #Redirect to thank you page if all questions are answered
    if(num_responses == len(survey.questions)):
        flash('You have already completed the survey.', 'warning')
        return redirect('/thank-you')

    #Check that the question number in URL is correct
    if(q_number != num_responses):
        #Redirect to correct question
        flash('You are trying to answer an invalid question.  Please answer the question below.', 'error')
        return redirect(f'/questions/{num_responses}')
    
    question = survey.questions[q_number]
    title = survey.title
    return render_template('question.html', title=title, question=question, q_number=q_number)

@app.route('/answers', methods=['POST'])
def submit_answer():
    """Add answer to responses list and redirect."""
    survey = surveys[session['survey']]
    
    q_number = int(request.form['q_number'])
    ans = request.form.get('response')
    comment = request.form.get('comment', False)

    question_title = survey.questions[q_number].question

    #rebind responses name from session
    responses = session['responses']
    responses[question_title] = ans
    if comment:
        responses[f"{question_title}_comment"] = comment

    #Update responses in session
    session['responses'] = responses

    if(q_number + 1 == len(survey.questions)):
        #Redirect to thank you page if answered last question
        return redirect('/thank-you')

    return redirect(f'/questions/{q_number + 1}')

@app.route('/thank-you')
def show_thank_you():
    survey = surveys[session['survey']]
    title = survey.title
    return render_template('thank_you.html', title=title)