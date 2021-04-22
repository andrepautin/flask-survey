from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def show_survey_instructions():
    return render_template("survey_start.html", survey=survey)


@app.route('/begin', methods=["POST"])
def show_survey_questions():
    return redirect("/questions/0")

@app.route('/questions/0')
def show_first_question():
    return render_template("question.html", question=survey.questions[0])
