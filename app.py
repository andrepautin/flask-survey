from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey_instructions():
    return render_template("survey_start.html", survey=survey)


@app.route('/begin', methods=["POST"])
def show_survey_questions():

    session["responses"] = []

    return redirect("/questions/0")

@app.route('/questions/<int:id>')
def show_first_question(id):
    """display the current question that the user is at"""
    question = survey.questions[id]
    return render_template("question.html", question_num=id, question=question)

@app.route('/answer', methods=["POST"])
def answer_question():
    """get and save responses from user and redirect to the next question"""
    # get user response
    answer = request.form['answer']
    # add answer to the responses session
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
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


