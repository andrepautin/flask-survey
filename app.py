from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY_NAME = "responses"


@app.route('/')
def show_survey_instructions():
    """Show initial survey start page"""
    return render_template("survey_start.html", survey=survey)


@app.route('/begin', methods=["POST"])
def show_survey_questions():
    """routes to first question of survey"""
    session[RESPONSES_KEY_NAME] = []

    return redirect("/questions/0")


@app.route('/questions/<int:id>')
def show_question(id):
    """display the current question that the user is at"""

    responses = session[RESPONSES_KEY_NAME]
    # if there are no responses yet, go back to root page
    if responses is None:
        return redirect('/')
    # if user has answered all questions, return complete page
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    # if user is trying to access random question, reroute them to the
    # correct question.
    if len(responses) != id:
        flash("You were trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[id]
    return render_template("question.html", question_num=id, question=question)


@app.route('/answer', methods=["POST"])
def answer_question():
    """get and save responses from user and redirect to the next question"""
    # get user response
    answer = request.form['answer']
    # add answer to the responses session
    responses = session[RESPONSES_KEY_NAME]
    responses.append(answer)
    session[RESPONSES_KEY_NAME] = responses
    # checks if user has answered all the questions
    # if so, redirect to /complete
    if len(responses) == len(survey.questions):
        return redirect("/complete")

    # redirect to questions/id
    return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """user completed survey, shows completion page"""
    return render_template("completion.html")
